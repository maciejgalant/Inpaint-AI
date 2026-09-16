from pathlib import Path
from datetime import datetime
import logging

from qgis.PyQt.QtCore import Qt, QSettings, QUrl, QStandardPaths
from qgis.PyQt.QtGui import QAction, QIcon, QDesktopServices
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QMessageBox,
    QFileDialog,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from qgis.core import QgsProject, QgsRasterLayer

from .map_tool import InpaintPolygonTool
from .ui import CloudPanel
from .raster_io import render_crop, georeference_png_to_tiff
from .openai_client import OpenAICloudClient
from .settings_dialog import SettingsDialog
from .help_dialog import HelpDialog
from .settings import get_authcfg, get_consent, set_consent, get_language


PLUGIN_NAME = "Inpaint AI Cloud"
SETTINGS_PREFIX = "InpaintAICloud"
OUTPUT_DIR_KEY = f"{SETTINGS_PREFIX}/outputDir"
LOGGER = logging.getLogger(__name__)


class InpaintAIPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.plugin_dir = Path(__file__).resolve().parent

        self.action = None
        self.dock = None
        self.panel = None
        self.map_tool = None
        self.geometry = None
        self.extent = None
        self.client = None
        self.busy = False

        self.qsettings = QSettings()

        self.output_dir_edit = None
        self.choose_output_dir_button = None
        self.open_output_dir_button = None
        self.output_card = None

        self.run_dir = None
        self.input_png = None
        self.mask_png = None
        self.output_png = None
        self.output_tif = None

    def initGui(self):
        self.action = QAction(
            QIcon(str(self.plugin_dir / "icon.png")),
            PLUGIN_NAME,
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.show_panel)

        self.iface.addPluginToRasterMenu(
            PLUGIN_NAME,
            self.action
        )
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.client:
            try:
                self.client.cancel()
            except Exception:
                LOGGER.debug("OpenAI request cleanup failed during unload", exc_info=True)

        self._dispose_selection_tool()

        if self.dock:
            self.iface.removeDockWidget(self.dock)
            self.dock.deleteLater()
            self.dock = None

        if self.action:
            self.iface.removePluginRasterMenu(
                PLUGIN_NAME,
                self.action
            )
            self.iface.removeToolBarIcon(self.action)
            self.action = None

    def _t(self, key, **kwargs):
        if self.panel:
            return self.panel.text(key, **kwargs)
        return key

    def _current_lang(self):
        if self.panel:
            return self.panel.lang
        return get_language()

    def _dispose_selection_tool(self):
        if self.map_tool is None:
            return

        try:
            if self.canvas.mapTool() is self.map_tool:
                self.canvas.unsetMapTool(self.map_tool)
        except Exception:
            LOGGER.debug("Map tool could not be unset during disposal", exc_info=True)

        try:
            self.map_tool.dispose()
        except Exception:
            try:
                self.map_tool.clear()
            except Exception:
                LOGGER.debug("Fallback selection cleanup failed", exc_info=True)

        self.map_tool = None

        try:
            self.canvas.refresh()
        except Exception:
            LOGGER.debug("Map canvas refresh failed after selection disposal", exc_info=True)

    # ------------------------------------------------------------------
    # OUTPUT DIRECTORY
    # ------------------------------------------------------------------

    def _default_output_dir(self):
        project_file = QgsProject.instance().fileName()

        if project_file:
            base = Path(project_file).resolve().parent
        else:
            documents = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
            base = (
                Path(documents)
                if documents
                else Path.home() / "Documents"
            )

        return base / "InpaintAI_Output"

    def _saved_output_dir(self):
        saved = self.qsettings.value(
            OUTPUT_DIR_KEY,
            "",
            type=str
        ).strip()

        if saved:
            return Path(saved)

        return self._default_output_dir()

    def get_output_dir(self):
        if self.output_dir_edit is not None:
            text = self.output_dir_edit.text().strip()
            path = (
                Path(text)
                if text
                else self._saved_output_dir()
            )
        else:
            path = self._saved_output_dir()

        try:
            path.mkdir(
                parents=True,
                exist_ok=True
            )
        except Exception as exc:
            raise RuntimeError(
                f"Nie można utworzyć folderu zapisu:\n"
                f"{path}\n\n{exc}"
            )

        return path

    def save_output_dir_setting(self):
        if self.output_dir_edit is None:
            return

        text = self.output_dir_edit.text().strip()
        if not text:
            return

        path = Path(text)

        try:
            path.mkdir(
                parents=True,
                exist_ok=True
            )
        except Exception as exc:
            QMessageBox.warning(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                f"Nie można utworzyć folderu:\n"
                f"{path}\n\n{exc}"
            )
            return

        self.qsettings.setValue(
            OUTPUT_DIR_KEY,
            str(path)
        )

    def choose_output_dir(self):
        try:
            current = self.get_output_dir()
        except Exception:
            current = self._default_output_dir()

        lang = self._current_lang()

        selected = QFileDialog.getExistingDirectory(
            self.iface.mainWindow(),
            (
                "Wybierz folder zapisu wyników"
                if lang == "pl"
                else "Select output folder"
            ),
            str(current)
        )

        if not selected:
            return

        path = Path(selected)

        self.qsettings.setValue(
            OUTPUT_DIR_KEY,
            str(path)
        )

        if self.output_dir_edit is not None:
            self.output_dir_edit.setText(
                str(path)
            )

        if self.panel:
            self.panel.status.setText(
                (
                    f"Folder zapisu: {path}"
                    if lang == "pl"
                    else f"Output folder: {path}"
                )
            )

    def open_output_dir(self):
        try:
            path = self.get_output_dir()
        except Exception as exc:
            QMessageBox.warning(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                str(exc)
            )
            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(str(path))
        )

    def _build_run_paths(self):
        base_dir = self.get_output_dir()
        stamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        run_dir = (
            base_dir
            / f"InpaintAI_{stamp}"
        )

        run_dir.mkdir(
            parents=True,
            exist_ok=False
        )

        self.run_dir = run_dir
        self.input_png = run_dir / "input.png"
        self.mask_png = run_dir / "mask.png"
        self.output_png = run_dir / "result.png"
        self.output_tif = run_dir / "result.tif"

    def _ensure_output_controls(self):
        if (
            self.panel is None
            or self.output_card is not None
        ):
            return

        # In Alpha 4.4+ the main controls live inside a scrollable
        # content widget. Insert the output section there so it also
        # scrolls on small screens. Fall back to the panel layout for
        # older builds.
        if hasattr(self.panel, "scroll_content") and self.panel.scroll_content is not None:
            panel_layout = self.panel.scroll_content.layout()
        else:
            panel_layout = self.panel.layout()

        if panel_layout is None:
            return

        self.output_card = QFrame()
        self.output_card.setObjectName("Card")

        card_layout = QVBoxLayout(
            self.output_card
        )
        card_layout.setContentsMargins(
            11, 10, 11, 10
        )
        card_layout.setSpacing(7)

        self.output_title_label = QLabel()
        self.output_title_label.setObjectName(
            "StepTitle"
        )
        card_layout.addWidget(
            self.output_title_label
        )

        self.output_desc_label = QLabel()
        self.output_desc_label.setObjectName(
            "Muted"
        )
        self.output_desc_label.setWordWrap(True)
        card_layout.addWidget(
            self.output_desc_label
        )

        path_row = QHBoxLayout()
        path_row.setSpacing(6)

        self.output_dir_edit = QLineEdit(
            str(self._saved_output_dir())
        )
        self.output_dir_edit.editingFinished.connect(
            self.save_output_dir_setting
        )
        path_row.addWidget(
            self.output_dir_edit,
            1
        )

        self.choose_output_dir_button = QPushButton()
        self.choose_output_dir_button.clicked.connect(
            self.choose_output_dir
        )
        path_row.addWidget(
            self.choose_output_dir_button
        )

        self.open_output_dir_button = QPushButton()
        self.open_output_dir_button.clicked.connect(
            self.open_output_dir
        )
        path_row.addWidget(
            self.open_output_dir_button
        )

        card_layout.addLayout(
            path_row
        )

        insert_index = max(
            0,
            panel_layout.count() - 1
        )

        panel_layout.insertWidget(
            insert_index,
            self.output_card
        )

        self._refresh_output_controls_language()

    def _refresh_output_controls_language(self):
        if self.output_card is None:
            return

        lang = self._current_lang()

        self.output_title_label.setText(
            "ZAPIS"
            if lang == "pl"
            else "OUTPUT"
        )

        self.output_desc_label.setText(
            (
                "Wybierz folder, w którym mają być "
                "zapisywane pliki każdej generacji."
            )
            if lang == "pl"
            else
            (
                "Choose the folder where files from "
                "each generation will be saved."
            )
        )

        self.choose_output_dir_button.setText(
            "Wybierz…"
            if lang == "pl"
            else "Browse…"
        )

        self.open_output_dir_button.setText(
            "Otwórz"
            if lang == "pl"
            else "Open"
        )

    # ------------------------------------------------------------------
    # PANEL / DIALOGS
    # ------------------------------------------------------------------

    def show_panel(self):
        if self.dock is None:
            self.dock = QDockWidget(
                PLUGIN_NAME,
                self.iface.mainWindow()
            )

            self.panel = CloudPanel(
                self.plugin_dir
            )

            self.dock.setWidget(
                self.panel
            )

            self.iface.addDockWidget(
                Qt.DockWidgetArea.RightDockWidgetArea,
                self.dock
            )

            self.panel.select.clicked.connect(
                self.start_selection
            )
            self.panel.undo.clicked.connect(
                self.undo_selection
            )
            self.panel.generate.clicked.connect(
                self.generate_cloud
            )
            self.panel.cancel.clicked.connect(
                self.cancel
            )
            self.panel.settings_button.clicked.connect(
                self.open_settings
            )

            if hasattr(self.panel, "help_button"):
                self.panel.help_button.clicked.connect(
                    self.open_help
                )

            self.panel.consent.setChecked(
                get_consent()
            )
            self.panel.consent.toggled.connect(
                set_consent
            )

            self._ensure_output_controls()

        self.panel.update_openai_status()
        self._refresh_output_controls_language()

        self.dock.show()
        self.dock.raise_()

    def open_settings(self):
        previous_language = get_language()

        dlg = SettingsDialog(
            self.plugin_dir,
            self.iface.mainWindow()
        )

        if dlg.exec():
            current_language = get_language()

            if (
                self.panel
                and current_language != previous_language
            ):
                self.panel.set_language(
                    current_language
                )

            if self.panel:
                self.panel.update_openai_status()

            self._refresh_output_controls_language()

    def open_help(self):
        dlg = HelpDialog(
            self._current_lang(),
            self.iface.mainWindow()
        )
        dlg.exec()

    # ------------------------------------------------------------------
    # SELECTION
    # ------------------------------------------------------------------

    def start_selection(self):
        if self.busy:
            return

        self._dispose_selection_tool()

        self.geometry = None
        self.extent = None

        self.map_tool = InpaintPolygonTool(
            self.canvas,
            self.selection_finished
        )

        self.canvas.setMapTool(
            self.map_tool
        )

        self.panel.generate.setEnabled(
            False
        )

        self.panel.status.setText(
            self._t("drawing_help")
        )

    def selection_finished(self, geometry):
        self.geometry = geometry

        try:
            self.canvas.unsetMapTool(
                self.map_tool
            )
        except Exception:
            LOGGER.debug("Map tool could not be unset after selection", exc_info=True)

        self.panel.generate.setEnabled(
            True
        )

        self.panel.status.setText(
            self._t("area_ready")
        )

    def undo_selection(self):
        if self.busy:
            return

        self._dispose_selection_tool()

        self.geometry = None
        self.extent = None

        if self.panel:
            self.panel.generate.setEnabled(
                False
            )
            self.panel.progress.setValue(0)
            self.panel.progress.setFormat(
                "%p% — " + self._t("waiting")
            )
            self.panel.status.setText(
                self._t("ready_select")
            )

    # ------------------------------------------------------------------
    # GENERATION
    # ------------------------------------------------------------------

    def generate_cloud(self):
        if (
            self.geometry is None
            or self.busy
        ):
            return

        authcfg = get_authcfg()

        if not authcfg:
            QMessageBox.information(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                self._t("auth_required")
            )
            return

        if not self.panel.consent.isChecked():
            QMessageBox.information(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                self._t("consent_required")
            )
            return

        try:
            self.save_output_dir_setting()
            self._build_run_paths()
        except Exception as exc:
            QMessageBox.critical(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                f"Błąd folderu zapisu:\n{exc}"
            )
            return

        self.panel.progress.setValue(15)
        self.panel.progress.setFormat(
            "%p% — " + self._t("crop_mask")
        )
        self.panel.status.setText(
            self._t("preparing")
        )

        try:
            self.extent = render_crop(
                self.canvas,
                self.geometry,
                self.input_png,
                self.mask_png,
                resolution=1024,
                context=self.panel.context.value()
            )
        except Exception as exc:
            QMessageBox.critical(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                str(exc)
            )
            return

        prompt = self.panel.combined_prompt()

        if not prompt.strip():
            QMessageBox.information(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                self._t("prompt_empty")
            )
            return

        model_id = self.panel.current_model_id()
        quality = self.panel.quality.currentText()

        self.busy = True
        self.panel.set_busy(True)
        self.panel.generate.setEnabled(
            False
        )

        self.client = OpenAICloudClient(
            self.iface.mainWindow()
        )

        self.client.progress.connect(
            self.on_progress
        )
        self.client.finished.connect(
            self.on_api_finished
        )
        self.client.failed.connect(
            self.on_api_failed
        )

        try:
            self.client.edit_image(
                self.input_png,
                self.mask_png,
                prompt,
                authcfg,
                model_id,
                quality=quality,
                size="1024x1024"
            )
        except Exception as exc:
            self.finish_busy()

            QMessageBox.critical(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                str(exc)
            )

    def on_progress(
        self,
        value,
        text
    ):
        self.panel.progress.setValue(
            value
        )
        self.panel.progress.setFormat(
            f"%p% — {text}"
        )
        self.panel.status.setText(
            text
        )

    def on_api_finished(
        self,
        image_bytes,
        request_id
    ):
        try:
            self.output_png.write_bytes(
                image_bytes
            )

            crs = (
                self.canvas
                .mapSettings()
                .destinationCrs()
            )

            georeference_png_to_tiff(
                self.output_png,
                self.output_tif,
                self.extent,
                crs
            )

            layer_name = (
                "Inpaint AI — "
                + self.run_dir.name.replace(
                    "InpaintAI_",
                    ""
                )
            )

            layer = QgsRasterLayer(
                str(self.output_tif),
                layer_name
            )

            if not layer.isValid():
                raise RuntimeError(
                    self._t("geotiff_error")
                )

            QgsProject.instance().addMapLayer(
                layer
            )

            self.panel.progress.setValue(
                100
            )
            self.panel.progress.setFormat(
                "%p% — " + self._t("done")
            )

            if hasattr(
                self.panel,
                "register_successful_generation"
            ):
                self.panel.register_successful_generation()

            lang = self._current_lang()

            if lang == "pl":
                status = (
                    "Gotowe — wynik dodano do QGIS.\n"
                    f"Zapisano w: {self.run_dir}"
                )
            else:
                status = (
                    "Done — result added to QGIS.\n"
                    f"Saved to: {self.run_dir}"
                )

            if request_id:
                status += (
                    f"\nRequest ID: {request_id}"
                )

            self.panel.status.setText(
                status
            )

            self._dispose_selection_tool()

            self.geometry = None
            self.extent = None

        except Exception as exc:
            QMessageBox.critical(
                self.iface.mainWindow(),
                PLUGIN_NAME,
                self._t(
                    "save_error",
                    error=str(exc)
                )
            )

        finally:
            self.finish_busy(
                selection_exists=False
            )

    def on_api_failed(
        self,
        message
    ):
        self.finish_busy(
            selection_exists=True
        )

        self.panel.progress.setValue(
            0
        )
        self.panel.progress.setFormat(
            "%p% — " + self._t("error")
        )
        self.panel.status.setText(
            self._t("generation_failed")
        )

        QMessageBox.critical(
            self.iface.mainWindow(),
            PLUGIN_NAME,
            message
        )

    def finish_busy(
        self,
        selection_exists=None
    ):
        self.busy = False
        self.client = None

        self.panel.set_busy(
            False
        )

        self.panel.update_openai_status()

        if selection_exists is None:
            selection_exists = (
                self.geometry is not None
            )

        self.panel.generate.setEnabled(
            bool(selection_exists)
        )

    def cancel(self):
        if (
            self.client
            and self.busy
        ):
            self.client.cancel()

            self.panel.status.setText(
                self._t("cancelled")
            )
        else:
            self.undo_selection()

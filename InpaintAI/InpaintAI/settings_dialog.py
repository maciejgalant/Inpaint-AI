from pathlib import Path

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QFormLayout, QDialogButtonBox
)

from .auth_dialog import OpenAIAuthDialog
from .settings import (
    get_authcfg, get_language, set_language
)


class SettingsDialog(QDialog):
    def __init__(self, plugin_dir, parent=None):
        super().__init__(parent)
        self.plugin_dir = Path(plugin_dir)
        self.lang = get_language()

        self.setMinimumWidth(500)
        self.setWindowTitle(
            "Inpaint AI — Ustawienia"
            if self.lang == "pl"
            else "Inpaint AI — Settings"
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Header
        head = QHBoxLayout()
        logo = QLabel()
        pm = QPixmap(str(self.plugin_dir / "icon.png"))
        if not pm.isNull():
            logo.setPixmap(pm.scaled(
                54, 54,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        head.addWidget(logo)

        title = QLabel()
        title.setText(
            "<b>Inpaint AI Cloud</b><br>"
            + (
                "Ustawienia wtyczki i połączenia OpenAI"
                if self.lang == "pl"
                else
                "Plugin and OpenAI connection settings"
            )
        )
        head.addWidget(title, 1)
        layout.addLayout(head)

        # General
        general = QGroupBox(
            "Ogólne" if self.lang == "pl" else "General"
        )
        general_form = QFormLayout(general)

        self.language_combo = QComboBox()
        self.language_combo.addItem("Polski", "pl")
        self.language_combo.addItem("English", "en")
        idx = self.language_combo.findData(self.lang)
        if idx >= 0:
            self.language_combo.setCurrentIndex(idx)

        general_form.addRow(
            "Język interfejsu:"
            if self.lang == "pl"
            else "Interface language:",
            self.language_combo
        )
        layout.addWidget(general)

        # OpenAI
        openai = QGroupBox("OpenAI")
        openai_layout = QVBoxLayout(openai)

        self.auth_status = QLabel()
        self.auth_status.setWordWrap(True)
        openai_layout.addWidget(self.auth_status)

        self.configure_auth = QPushButton()
        self.configure_auth.setText(
            "Skonfiguruj połączenie OpenAI…"
            if self.lang == "pl"
            else "Configure OpenAI connection…"
        )
        self.configure_auth.clicked.connect(self.open_auth_dialog)
        openai_layout.addWidget(self.configure_auth)

        security = QLabel(
            (
                "Klucz API jest przechowywany przez QGIS Authentication Manager, "
                "a nie w kodzie ani ustawieniach wtyczki."
            )
            if self.lang == "pl"
            else
            (
                "The API key is stored by QGIS Authentication Manager, "
                "not in the plugin code or plain plugin settings."
            )
        )
        security.setWordWrap(True)
        openai_layout.addWidget(security)
        layout.addWidget(openai)

        # About / privacy
        about = QGroupBox(
            "Informacje i prywatność"
            if self.lang == "pl"
            else "About and privacy"
        )
        about_layout = QVBoxLayout(about)
        about_text = QLabel(
            (
                "Wtyczka wysyła do OpenAI wyłącznie przygotowany crop obrazu, "
                "maskę oraz treść polecenia potrzebne do wykonania edycji. "
                "Przed generowaniem wymagana jest zgoda użytkownika."
            )
            if self.lang == "pl"
            else
            (
                "The plugin sends OpenAI only the prepared image crop, mask "
                "and instruction required for the edit. User consent is required "
                "before generation."
            )
        )
        about_text.setWordWrap(True)
        about_layout.addWidget(about_text)
        layout.addWidget(about)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.update_auth_status()

    def update_auth_status(self):
        configured = bool(get_authcfg())
        if self.lang == "pl":
            text = (
                "● Połączenie skonfigurowane"
                if configured
                else "● Brak konfiguracji OpenAI"
            )
        else:
            text = (
                "● Connection configured"
                if configured
                else "● OpenAI is not configured"
            )
        self.auth_status.setText(text)

    def open_auth_dialog(self):
        dlg = OpenAIAuthDialog(self.lang, self)
        if dlg.exec():
            self.update_auth_status()

    def accept(self):
        new_lang = self.language_combo.currentData()
        if new_lang in ("pl", "en"):
            set_language(new_lang)
        super().accept()

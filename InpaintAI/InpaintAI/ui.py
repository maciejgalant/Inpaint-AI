from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton,
    QComboBox, QPlainTextEdit, QDoubleSpinBox, QCheckBox, QProgressBar,
    QFrame, QToolButton, QScrollArea
)

from .prompts import (
    MATCHING_MODES, preset_ids, preset_label, preset_suggestion,
    matching_label, build_edit_prompt
)
from .ui_texts import tr
from .settings import (
    get_language, get_matching_mode, set_matching_mode, get_authcfg
)


COST_TABLE_USD = {
    "gpt-image-2.5-sunburst": {
        "low": 0.006,
        "medium": 0.013,
        "high": 0.053,
        "xhigh": 0.094,
        "max": 0.211,
    },
    "gpt-image-2.5-flare": {
        "low": 0.006,
        "medium": 0.013,
        "high": 0.053,
        "xhigh": 0.094,
        "max": 0.211,
    },
}

STYLE = """
QWidget {
    font-size: 12px;
}
QFrame#HeaderCard, QFrame#Card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
}
QFrame#HeaderCard {
    background: rgba(255,255,255,0.06);
}
QLabel#Title {
    font-size: 17px;
    font-weight: 800;
}
QLabel#Subtitle, QLabel#Muted {
    color: #a8adb3;
}
QLabel#StepBadge {
    background: #67d54b;
    color: #112613;
    border: 1px solid #83ef67;
    border-radius: 15px;
    min-width: 30px;
    max-width: 30px;
    min-height: 30px;
    max-height: 30px;
    font-size: 13px;
    font-weight: 700;
    qproperty-alignment: AlignCenter;
}
QLabel#StepTitle {
    font-size: 13px;
    font-weight: 800;
}
QLabel#Connected {
    color: #64d98a;
    font-weight: 700;
}
QLabel#Disconnected {
    color: #e7b066;
    font-weight: 700;
}
QPushButton {
    min-height: 30px;
    border-radius: 6px;
    padding: 4px 10px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.06);
}
QPushButton:hover {
    background: rgba(255,255,255,0.10);
}
QPushButton#PrimaryAction {
    min-height: 36px;
    font-weight: 800;
    border: 1px solid #5fcb48;
    background: rgba(95,203,72,0.14);
}
QPushButton#Generate {
    min-height: 40px;
    font-size: 13px;
    font-weight: 800;
    border: 1px solid #5ecb47;
    background: rgba(95,203,72,0.12);
}
QPushButton#Settings {
    min-height: 30px;
    font-weight: 700;
}
QPushButton#Help {
    min-width: 32px;
    max-width: 32px;
    min-height: 30px;
    max-height: 30px;
    font-weight: 800;
}
QPushButton#Danger {
    color: #ffaaaa;
}
QComboBox, QDoubleSpinBox, QPlainTextEdit {
    border-radius: 5px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.04);
}
QPlainTextEdit {
    padding: 6px;
}
QToolButton#AdvancedToggle {
    border: none;
    padding: 5px 0px;
    font-weight: 700;
    color: #d9dde1;
}
QProgressBar {
    min-height: 20px;
    border-radius: 5px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.12);
}
QProgressBar::chunk {
    background-color: #61d649;
    border-radius: 4px;
}
QScrollArea {
    background: transparent;
    border: none;
}
QScrollBar:vertical {
    background: rgba(255,255,255,0.025);
    width: 10px;
    margin: 2px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: rgba(255,255,255,0.22);
    min-height: 30px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(255,255,255,0.34);
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


class CloudPanel(QWidget):
    def __init__(self, plugin_dir, parent=None):
        super().__init__(parent)
        self.plugin_dir = plugin_dir
        self.lang = get_language()
        self.prompt_mode = "positive"
        self.positive_text = ""
        self.negative_text = ""
        self._default_prompt_text = ""
        self.session_cost_usd = 0.0
        self.session_images = 0

        self.setStyleSheet(STYLE)
        self._build_ui()
        self.apply_language(first=True)
        self.update_openai_status()

    def text(self, key, **kwargs):
        return tr(self.lang, key, **kwargs)

    def _build_ui(self):
        # Scrollable content keeps the plugin usable on smaller screens and
        # short QGIS dock areas without compressing the controls excessively.
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_content = QWidget()
        layout = QVBoxLayout(self.scroll_content)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(9)

        header = QFrame()
        header.setObjectName("HeaderCard")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(10, 10, 10, 10)
        hl.setSpacing(10)

        self.logo = QLabel()
        pm = QPixmap(str(self.plugin_dir / "icon.png"))
        if not pm.isNull():
            self.logo.setPixmap(pm.scaled(
                58, 58,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        hl.addWidget(self.logo)

        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        self.title = QLabel()
        self.title.setObjectName("Title")
        self.subtitle = QLabel()
        self.subtitle.setObjectName("Subtitle")
        title_box.addWidget(self.title)
        title_box.addWidget(self.subtitle)
        hl.addLayout(title_box, 1)

        header_actions = QVBoxLayout()
        header_actions.setSpacing(5)
        self.openai_status = QLabel()
        self.openai_status.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        button_row = QHBoxLayout()
        button_row.setSpacing(6)
        self.help_button = QPushButton("?")
        self.help_button.setObjectName("Help")
        self.settings_button = QPushButton()
        self.settings_button.setObjectName("Settings")
        self.settings_button.setMinimumWidth(112)
        button_row.addWidget(self.help_button)
        button_row.addWidget(self.settings_button)
        header_actions.addWidget(self.openai_status)
        header_actions.addLayout(button_row)
        hl.addLayout(header_actions)

        layout.addWidget(header)

        area_card = QFrame()
        area_card.setObjectName("Card")
        area = QVBoxLayout(area_card)
        area.setContentsMargins(11, 10, 11, 10)
        area.setSpacing(8)

        area_head = QHBoxLayout()
        self.badge1 = QLabel("1")
        self.badge1.setObjectName("StepBadge")
        area_head.addWidget(self.badge1)
        area_text = QVBoxLayout()
        area_text.setSpacing(1)
        self.area_title = QLabel()
        self.area_title.setObjectName("StepTitle")
        self.area_desc = QLabel()
        self.area_desc.setObjectName("Muted")
        area_text.addWidget(self.area_title)
        area_text.addWidget(self.area_desc)
        area_head.addLayout(area_text, 1)
        area.addLayout(area_head)

        self.select = QPushButton()
        self.select.setObjectName("PrimaryAction")
        area.addWidget(self.select)

        row_area = QHBoxLayout()
        row_area.setSpacing(6)
        self.undo = QPushButton()
        self.cancel = QPushButton()
        self.cancel.setObjectName("Danger")
        row_area.addWidget(self.undo)
        row_area.addWidget(self.cancel)
        area.addLayout(row_area)
        layout.addWidget(area_card)

        prompt_card = QFrame()
        prompt_card.setObjectName("Card")
        pc = QVBoxLayout(prompt_card)
        pc.setContentsMargins(11, 10, 11, 10)
        pc.setSpacing(8)

        prompt_title_row = QHBoxLayout()
        self.badge2 = QLabel("2")
        self.badge2.setObjectName("StepBadge")
        prompt_title_row.addWidget(self.badge2)
        prompt_text = QVBoxLayout()
        prompt_text.setSpacing(1)
        self.what_title = QLabel()
        self.what_title.setObjectName("StepTitle")
        self.what_desc = QLabel()
        self.what_desc.setObjectName("Muted")
        prompt_text.addWidget(self.what_title)
        prompt_text.addWidget(self.what_desc)
        prompt_title_row.addLayout(prompt_text, 1)
        pc.addLayout(prompt_title_row)

        preset_row = QHBoxLayout()
        preset_row.setSpacing(8)
        self.type_label = QLabel()
        self.type_label.setMinimumWidth(60)
        self.preset = QComboBox()
        preset_row.addWidget(self.type_label)
        preset_row.addWidget(self.preset, 1)
        pc.addLayout(preset_row)

        prompt_head = QHBoxLayout()
        self.prompt_label = QLabel()
        self.prompt_label.setObjectName("Muted")
        prompt_head.addWidget(self.prompt_label)
        prompt_head.addStretch()
        self.restore = QPushButton()
        self.restore.setMaximumWidth(135)
        prompt_head.addWidget(self.restore)
        pc.addLayout(prompt_head)

        self.prompt = QPlainTextEdit()
        self.prompt.setMinimumHeight(104)
        self.prompt.setMaximumHeight(150)
        pc.addWidget(self.prompt)

        self.advanced_toggle = QToolButton()
        self.advanced_toggle.setObjectName("AdvancedToggle")
        self.advanced_toggle.setCheckable(True)
        self.advanced_toggle.setChecked(False)
        self.advanced_toggle.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextOnly
        )
        pc.addWidget(self.advanced_toggle)

        self.advanced_frame = QFrame()
        advanced = QFormLayout(self.advanced_frame)
        advanced.setContentsMargins(0, 2, 0, 0)
        advanced.setVerticalSpacing(7)

        self.model = QComboBox()
        self.model.addItem(
            "Sunburst — precise editing",
            "gpt-image-2.5-sunburst"
        )
        self.model.addItem(
            "Flare — fast generation",
            "gpt-image-2.5-flare"
        )
        self.model_label = QLabel()
        advanced.addRow(self.model_label, self.model)

        self.quality = QComboBox()
        self.quality.addItems(["low", "medium", "high", "xhigh", "max"])
        self.quality.setCurrentText("high")
        self.quality_label = QLabel()
        advanced.addRow(self.quality_label, self.quality)

        self.context = QDoubleSpinBox()
        self.context.setRange(1.05, 6.0)
        self.context.setValue(2.0)
        self.context.setSingleStep(0.25)
        self.context.setSuffix("×")
        self.context_label = QLabel()
        advanced.addRow(self.context_label, self.context)

        self.matching = QComboBox()
        self.matching_label_widget = QLabel()
        advanced.addRow(self.matching_label_widget, self.matching)

        self.switch_prompt = QPushButton()
        advanced.addRow("", self.switch_prompt)

        self.advanced_frame.setVisible(False)
        pc.addWidget(self.advanced_frame)
        layout.addWidget(prompt_card)

        gen_card = QFrame()
        gen_card.setObjectName("Card")
        gc = QVBoxLayout(gen_card)
        gc.setContentsMargins(11, 10, 11, 10)
        gc.setSpacing(8)

        gen_head = QHBoxLayout()
        self.badge3 = QLabel("3")
        self.badge3.setObjectName("StepBadge")
        gen_head.addWidget(self.badge3)
        gen_text = QVBoxLayout()
        gen_text.setSpacing(1)
        self.gen_title = QLabel()
        self.gen_title.setObjectName("StepTitle")
        self.gen_desc = QLabel()
        self.gen_desc.setObjectName("Muted")
        gen_text.addWidget(self.gen_title)
        gen_text.addWidget(self.gen_desc)
        gen_head.addLayout(gen_text, 1)
        gc.addLayout(gen_head)

        cost_row = QHBoxLayout()
        cost_row.setSpacing(12)
        self.cost_label = QLabel()
        self.cost_label.setObjectName("Muted")
        self.session_label = QLabel()
        self.session_label.setObjectName("Muted")
        cost_row.addWidget(self.cost_label)
        cost_row.addStretch()
        cost_row.addWidget(self.session_label)
        gc.addLayout(cost_row)

        self.cost_note = QLabel()
        self.cost_note.setObjectName("Muted")
        self.cost_note.setWordWrap(True)
        gc.addWidget(self.cost_note)

        self.consent = QCheckBox()
        gc.addWidget(self.consent)

        self.generate = QPushButton()
        self.generate.setObjectName("Generate")
        self.generate.setEnabled(False)
        gc.addWidget(self.generate)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        gc.addWidget(self.progress)
        layout.addWidget(gen_card)

        self.status = QLabel()
        self.status.setWordWrap(True)
        self.status.setObjectName("Muted")
        layout.addWidget(self.status)

        footer = QHBoxLayout()
        self.footer_openai = QLabel()
        footer.addWidget(self.footer_openai)
        footer.addStretch()
        self.footer_info = QLabel()
        self.footer_info.setObjectName("Muted")
        footer.addWidget(self.footer_info)
        layout.addLayout(footer)

        layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)
        outer_layout.addWidget(self.scroll_area)

        self.preset.currentIndexChanged.connect(self._preset_changed)
        self.switch_prompt.clicked.connect(self.toggle_prompt)
        self.restore.clicked.connect(self.restore_current_preset)
        self.advanced_toggle.toggled.connect(self._toggle_advanced)
        self.matching.currentIndexChanged.connect(self._matching_changed)
        self.model.currentIndexChanged.connect(self._model_changed)
        self.quality.currentIndexChanged.connect(self._cost_controls_changed)
        self.context.valueChanged.connect(self._update_footer)

    def _set_combo_by_data(self, combo, value):
        idx = combo.findData(value)
        if idx >= 0:
            combo.setCurrentIndex(idx)

    def _populate_presets(self, preserve_id=None):
        current_id = preserve_id or self.current_preset_id()
        self.preset.blockSignals(True)
        self.preset.clear()
        for preset_id in preset_ids():
            self.preset.addItem(
                preset_label(preset_id, self.lang),
                preset_id
            )
        self._set_combo_by_data(self.preset, current_id or "custom")
        self.preset.blockSignals(False)

    def _populate_matching(self, preserve_id=None):
        current_id = preserve_id or self.current_matching_mode()
        self.matching.blockSignals(True)
        self.matching.clear()
        for mode_id in MATCHING_MODES:
            self.matching.addItem(
                matching_label(mode_id, self.lang),
                mode_id
            )
        self._set_combo_by_data(self.matching, current_id or "strict")
        self.matching.blockSignals(False)

    def set_language(self, lang):
        if lang not in ("pl", "en") or lang == self.lang:
            return
        self.save_prompt()
        self.lang = lang
        self.apply_language(first=False)

    def apply_language(self, first=False):
        current_preset = self.current_preset_id() if self.preset.count() else "custom"
        current_match = self.current_matching_mode() if self.matching.count() else get_matching_mode()
        old_default = self._default_prompt_text
        current_prompt = self.prompt.toPlainText()

        self._populate_presets(current_preset)
        self._populate_matching(current_match)

        self.title.setText(self.text("plugin_name"))
        self.subtitle.setText(self.text("subtitle"))
        self.area_title.setText(self.text("area"))
        self.area_desc.setText(self.text("area_desc"))
        self.select.setText(self.text("select_area"))
        self.undo.setText(self.text("undo"))
        self.cancel.setText(self.text("cancel"))
        self.what_title.setText(self.text("what"))
        self.what_desc.setText(self.text("what_desc"))
        self.type_label.setText(self.text("type"))
        self.prompt_label.setText(self.text("command") if self.prompt_mode == "positive" else self.text("negative_command"))
        self.restore.setText(self.text("restore_preset"))
        self.model_label.setText(self.text("model") + ":")
        self.quality_label.setText(self.text("quality") + ":")
        self.context_label.setText(self.text("context") + ":")
        self.matching_label_widget.setText(self.text("matching") + ":")
        self.gen_title.setText(self.text("generation"))
        self.gen_desc.setText(self.text("generation_desc"))
        self.cost_note.setText(self.text("cost_note"))
        self.consent.setText(self.text("consent"))
        self.generate.setText(self.text("generate"))
        self.settings_button.setText("⚙ " + self.text("settings"))
        self.help_button.setToolTip(self.text("help"))
        self.advanced_toggle.setText(("▾  " if self.advanced_toggle.isChecked() else "▸  ") + self.text("advanced"))
        self.switch_prompt.setText(self.text("show_negative") if self.prompt_mode == "positive" else self.text("show_positive"))
        self.prompt.setPlaceholderText(self.text("placeholder"))

        if first:
            self.restore_current_preset()
            self.status.setText(self.text("ready_select"))
            self.progress.setValue(0)
            self.progress.setFormat("%p% — " + self.text("waiting"))
        else:
            new_default = preset_suggestion(current_preset, self.lang)
            if self.prompt_mode == "positive" and current_prompt == old_default:
                self.positive_text = new_default
                self.prompt.setPlainText(new_default)
            self._default_prompt_text = new_default

        self._update_matching_tip()
        self._update_cost_labels()
        self._update_footer()
        self.update_openai_status()

    def update_openai_status(self):
        configured = bool(get_authcfg())
        if configured:
            label = self.text("connected")
            object_name = "Connected"
        else:
            label = self.text("setup")
            object_name = "Disconnected"
        self.openai_status.setText(label)
        self.openai_status.setObjectName(object_name)
        self.openai_status.style().unpolish(self.openai_status)
        self.openai_status.style().polish(self.openai_status)

        self.footer_openai.setText(self.text("footer_connected") if configured else self.text("footer_setup"))
        self.footer_openai.setObjectName("Connected" if configured else "Disconnected")
        self.footer_openai.style().unpolish(self.footer_openai)
        self.footer_openai.style().polish(self.footer_openai)

    def _preset_changed(self):
        self.load_preset(self.current_preset_id())

    def _matching_changed(self):
        mode = self.current_matching_mode()
        set_matching_mode(mode)
        self._update_matching_tip()

    def _update_matching_tip(self):
        mode = self.current_matching_mode()
        tip_key = {
            "strict": "strict_tip",
            "balanced": "balanced_tip",
            "creative": "creative_tip",
        }.get(mode, "strict_tip")
        self.matching.setToolTip(self.text(tip_key))

    def _toggle_advanced(self, checked):
        self.advanced_frame.setVisible(checked)
        self.advanced_toggle.setText(("▾  " if checked else "▸  ") + self.text("advanced"))

    def _model_changed(self):
        self._update_cost_labels()
        self._update_footer()

    def _cost_controls_changed(self):
        self._update_cost_labels()
        self._update_footer()

    def current_preset_id(self):
        return self.preset.currentData() or "custom"

    def current_matching_mode(self):
        return self.matching.currentData() or "strict"

    def current_model_id(self):
        return self.model.currentData() or "gpt-image-2.5-sunburst"

    def estimate_unit_cost(self):
        model = self.current_model_id()
        quality = self.quality.currentText()
        return COST_TABLE_USD.get(model, {}).get(quality)

    def _format_usd(self, value):
        if value is None:
            return self.text("cost_unknown")
        if value < 0.01:
            return f"≈ ${value:.3f}"
        return f"≈ ${value:.2f}"

    def _update_cost_labels(self):
        unit = self.estimate_unit_cost()
        self.cost_label.setText(
            f"{self.text('estimated_cost')}: {self._format_usd(unit)} {self.text('cost_image_suffix')}"
        )
        session_text = self._format_usd(self.session_cost_usd) if self.session_images else self.text("cost_unknown")
        suffix = self.text("cost_session_suffix", count=self.session_images) if self.session_images else ""
        self.session_label.setText(
            f"{self.text('session_cost')}: {session_text}" + (f" ({suffix})" if suffix else "")
        )
        tooltip = self.text("cost_note")
        self.cost_label.setToolTip(tooltip)
        self.session_label.setToolTip(tooltip)

    def register_successful_generation(self):
        unit = self.estimate_unit_cost()
        if unit is not None:
            self.session_cost_usd += unit
        self.session_images += 1
        self._update_cost_labels()

    def save_prompt(self):
        if self.prompt_mode == "positive":
            self.positive_text = self.prompt.toPlainText()
        else:
            self.negative_text = self.prompt.toPlainText()

    def load_preset(self, preset_id):
        self.save_prompt()
        self.positive_text = preset_suggestion(preset_id, self.lang)
        self.negative_text = ""
        self._default_prompt_text = self.positive_text
        if self.prompt_mode == "positive":
            self.prompt.setPlainText(self.positive_text)
        else:
            self.prompt.setPlainText(self.negative_text)

    def restore_current_preset(self):
        self.load_preset(self.current_preset_id())

    def toggle_prompt(self):
        self.save_prompt()
        if self.prompt_mode == "positive":
            self.prompt_mode = "negative"
            self.prompt_label.setText(self.text("negative_command"))
            self.switch_prompt.setText(self.text("show_positive"))
            self.prompt.setPlainText(self.negative_text)
        else:
            self.prompt_mode = "positive"
            self.prompt_label.setText(self.text("command"))
            self.switch_prompt.setText(self.text("show_negative"))
            self.prompt.setPlainText(self.positive_text)

    def combined_prompt(self):
        self.save_prompt()
        return build_edit_prompt(
            self.current_preset_id(),
            self.positive_text,
            self.current_matching_mode(),
            self.negative_text
        )

    def _update_footer(self):
        model = "Sunburst" if "sunburst" in self.current_model_id() else "Flare"
        self.footer_info.setText(
            f"{model}  |  {self.quality.currentText()}  |  {self.context.value():.2f}×"
        )

    def set_busy(self, busy):
        self.select.setEnabled(not busy)
        self.undo.setEnabled(not busy)
        self.cancel.setEnabled(not busy)
        self.settings_button.setEnabled(not busy)
        self.help_button.setEnabled(not busy)
        self.model.setEnabled(not busy)
        self.quality.setEnabled(not busy)
        self.preset.setEnabled(not busy)
        self.matching.setEnabled(not busy)
        self.prompt.setReadOnly(busy)

from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from qgis.gui import QgsAuthConfigSelect

from .settings import get_authcfg, set_authcfg


AUTH_TEXT = {
    "pl": {
        "title": "OpenAI — uwierzytelnianie QGIS",
        "info": (
            "<b>Wybierz lub utwórz konfigurację typu „API Header”.</b><br><br>"
            "Nagłówek powinien mieć:<br>"
            "<code>Authorization</code> = <code>Bearer TWÓJ_KLUCZ_API</code><br><br>"
            "Klucz nie jest zapisywany w kodzie wtyczki. "
            "Przechowuje go QGIS Authentication Manager."
        ),
    },
    "en": {
        "title": "OpenAI — QGIS authentication",
        "info": (
            "<b>Select or create an “API Header” authentication configuration.</b><br><br>"
            "The header must contain:<br>"
            "<code>Authorization</code> = <code>Bearer YOUR_API_KEY</code><br><br>"
            "The key is not stored in the plugin code. "
            "It is stored by QGIS Authentication Manager."
        ),
    },
}


class OpenAIAuthDialog(QDialog):
    def __init__(self, lang="pl", parent=None):
        super().__init__(parent)
        self.lang = lang if lang in AUTH_TEXT else "en"
        txt = AUTH_TEXT[self.lang]

        self.setWindowTitle(txt["title"])
        self.resize(640, 430)

        layout = QVBoxLayout(self)

        info = QLabel(txt["info"])
        info.setWordWrap(True)
        layout.addWidget(info)

        self.selector = QgsAuthConfigSelect(self)
        saved = get_authcfg()
        if saved:
            self.selector.setConfigId(saved)
        layout.addWidget(self.selector, 1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        set_authcfg(self.selector.configId())
        super().accept()

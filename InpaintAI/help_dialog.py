from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox

from .ui_texts import tr


class HelpDialog(QDialog):
    def __init__(self, lang="en", parent=None):
        super().__init__(parent)
        self.lang = lang if lang in ("pl", "en") else "en"
        self.setWindowTitle(tr(self.lang, "help_title"))
        self.setMinimumSize(620, 500)

        layout = QVBoxLayout(self)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(tr(self.lang, "help_html"))
        layout.addWidget(browser)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

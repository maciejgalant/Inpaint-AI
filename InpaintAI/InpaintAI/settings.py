from qgis.PyQt.QtCore import QSettings
from .ui_texts import default_language

PREFIX = "InpaintAICloud"

def get_authcfg():
    return QSettings().value(f"{PREFIX}/authcfg", "", type=str)

def set_authcfg(value):
    QSettings().setValue(f"{PREFIX}/authcfg", value or "")

def get_consent():
    return QSettings().value(f"{PREFIX}/cloudConsent", False, type=bool)

def set_consent(value):
    QSettings().setValue(f"{PREFIX}/cloudConsent", bool(value))

def get_language():
    value = QSettings().value(f"{PREFIX}/language", "", type=str)
    return value if value in ("pl", "en") else default_language()

def set_language(value):
    if value in ("pl", "en"):
        QSettings().setValue(f"{PREFIX}/language", value)

def get_matching_mode():
    value = QSettings().value(f"{PREFIX}/matchingMode", "strict", type=str)
    return value if value in ("strict", "balanced", "creative") else "strict"

def set_matching_mode(value):
    if value in ("strict", "balanced", "creative"):
        QSettings().setValue(f"{PREFIX}/matchingMode", value)

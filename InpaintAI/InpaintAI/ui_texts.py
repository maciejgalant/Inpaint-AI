from qgis.PyQt.QtCore import QLocale


TEXTS = {
    "pl": {
        "plugin_name": "Inpaint AI Cloud",
        "subtitle": "Generatywna edycja ortofotomap",
        "language": "Język",
        "openai": "OpenAI",
        "settings": "Ustawienia",
        "help": "Pomoc",
        "area": "OBSZAR",
        "area_desc": "Zaznacz obszar, który chcesz zmienić",
        "select_area": "Zaznacz obszar na mapie",
        "undo": "Cofnij zaznaczenie",
        "cancel": "Anuluj",
        "what": "CO WYGENEROWAĆ?",
        "what_desc": "Wybierz preset lub wpisz własne polecenie",
        "type": "Typ",
        "command": "Polecenie",
        "restore_preset": "Przywróć preset",
        "advanced": "Opcje zaawansowane",
        "model": "Model",
        "quality": "Jakość",
        "context": "Kontekst",
        "matching": "Dopasowanie",
        "strict": "Ścisłe",
        "balanced": "Zrównoważone",
        "creative": "Kreatywne",
        "show_negative": "Pokaż ograniczenia dodatkowe",
        "show_positive": "Pokaż polecenie główne",
        "negative_command": "Ograniczenia dodatkowe",
        "generation": "GENEROWANIE",
        "generation_desc": "Ustaw opcje i wygeneruj obraz",
        "estimated_cost": "Szacowany koszt",
        "session_cost": "Koszt sesji",
        "cost_note": "Orientacyjnie dla 1 obrazu 1024×1024",
        "consent": "Zgadzam się na przesłanie cropu i maski do OpenAI.",
        "generate": "GENERUJ",
        "ready_select": "Gotowe — zaznacz obszar.",
        "drawing_help": "Rysowanie: LPM dodaje wierzchołki, PPM kończy poligon.",
        "area_ready": "Obszar gotowy. Możesz rozpocząć generowanie.",
        "waiting": "oczekiwanie",
        "crop_mask": "crop i maska",
        "preparing": "Przygotowanie danych…",
        "prompt_empty": "Polecenie nie może być puste.",
        "done": "gotowe",
        "done_result": "Gotowe — wynik dodano do QGIS.",
        "error": "błąd",
        "generation_failed": "Generowanie nie powiodło się.",
        "cancelled": "Anulowano żądanie.",
        "auth_selected": "Wybrano konfigurację QGIS authcfg: {authcfg}",
        "auth_missing": "Nie wybrano konfiguracji uwierzytelniania.",
        "auth_required": "Najpierw skonfiguruj OpenAI i wybierz konfigurację QGIS Authentication typu API Header.",
        "consent_required": "Zaznacz zgodę na przesłanie cropu i maski do OpenAI.",
        "geotiff_error": "GeoTIFF został zapisany, ale QGIS nie może go otworzyć.",
        "save_error": "Obraz został wygenerowany, ale wystąpił błąd podczas zapisu/georeferencji:\n{error}",
        "custom_prompt": "Własny prompt",
        "placeholder": "Np. Stwórz tutaj realistyczny parking miejski z drogą dojazdową.",
        "strict_tip": "Najmocniej dopasowuje kolor, ekspozycję, teksturę, cienie i charakter ortofotomapy.",
        "balanced_tip": "Zachowuje zgodność z ortofotomapą, ale pozwala modelowi na umiarkowaną rekonstrukcję.",
        "creative_tip": "Pozwala na większą swobodę przy zachowaniu perspektywy lotniczej i fotorealizmu.",
        "connected": "● OpenAI — połączono",
        "setup": "● OpenAI — konfiguracja",
        "footer_connected": "● OpenAI",
        "footer_setup": "● OpenAI — brak konfiguracji",
        "cost_unknown": "≈ —",
        "cost_image_suffix": "/ obraz",
        "cost_session_suffix": "{count} obraz(y)",
        "help_title": "Pomoc — Inpaint AI Cloud",
        "help_button": "?",
        "help_html": """
        <h3>Inpaint AI Cloud — szybka instrukcja</h3>
        <p><b>Autor / wykonawca:</b> Maciej Galant</p>
        <p><b>Przeznaczenie:</b> generatywna edycja ortofotomap w QGIS z użyciem OpenAI.</p>
        <ol>
          <li><b>Ustawienia:</b> skonfiguruj OpenAI API w oknie Ustawienia.</li>
          <li><b>Obszar:</b> kliknij <i>Zaznacz obszar na mapie</i>, narysuj poligon<br>— LPM dodaje punkt, PPM kończy.</li>
          <li><b>Opis:</b> wybierz preset albo wpisz własne polecenie.</li>
          <li><b>Zaawansowane:</b> wybierz model, jakość, kontekst i tryb dopasowania.</li>
          <li><b>Generowanie:</b> zaznacz zgodę i kliknij <i>GENERUJ</i>.</li>
        </ol>
        <p><b>Ważne:</b> wtyczka automatycznie dodaje ukryte instrukcje poprawiające dopasowanie do ortofotomapy: kolor, ekspozycję, cienie, teksturę, skalę i charakter zobrazowania.</p>
        <p><b>Szacowany koszt</b> jest orientacyjny i dotyczy 1 obrazu 1024×1024. Rzeczywisty koszt API może się nieznacznie różnić.</p>
        <p><b>Dane wysyłane do OpenAI:</b> crop obrazu, maska i treść polecenia — dopiero po zaznaczeniu zgody użytkownika.</p>
        <p><b>Wskazówka:</b> gdy wynik słabo wtapia się w tło, użyj trybu <i>Ścisłe</i>, zwiększ kontekst lub skróć polecenie.</p>
        """,
    },
    "en": {
        "plugin_name": "Inpaint AI Cloud",
        "subtitle": "Generative orthophoto editing",
        "language": "Language",
        "openai": "OpenAI",
        "settings": "Settings",
        "help": "Help",
        "area": "AREA",
        "area_desc": "Select the area you want to modify",
        "select_area": "Select area on map",
        "undo": "Undo selection",
        "cancel": "Cancel",
        "what": "WHAT TO GENERATE?",
        "what_desc": "Choose a preset or enter your own instruction",
        "type": "Type",
        "command": "Instruction",
        "restore_preset": "Restore preset",
        "advanced": "Advanced options",
        "model": "Model",
        "quality": "Quality",
        "context": "Context",
        "matching": "Matching",
        "strict": "Strict",
        "balanced": "Balanced",
        "creative": "Creative",
        "show_negative": "Show additional constraints",
        "show_positive": "Show main instruction",
        "negative_command": "Additional constraints",
        "generation": "GENERATION",
        "generation_desc": "Set options and generate the image",
        "estimated_cost": "Estimated cost",
        "session_cost": "Session cost",
        "cost_note": "Approximate for 1 image at 1024×1024",
        "consent": "I agree to send the crop and mask to OpenAI.",
        "generate": "GENERATE",
        "ready_select": "Ready — select an area.",
        "drawing_help": "Drawing: LMB adds vertices, RMB finishes the polygon.",
        "area_ready": "Area ready. You can start generation.",
        "waiting": "waiting",
        "crop_mask": "crop and mask",
        "preparing": "Preparing data…",
        "prompt_empty": "The instruction cannot be empty.",
        "done": "done",
        "done_result": "Done — result added to QGIS.",
        "error": "error",
        "generation_failed": "Generation failed.",
        "cancelled": "Request cancelled.",
        "auth_selected": "Selected QGIS authcfg: {authcfg}",
        "auth_missing": "No authentication configuration selected.",
        "auth_required": "Configure OpenAI first and select a QGIS Authentication API Header configuration.",
        "consent_required": "Accept sending the crop and mask to OpenAI.",
        "geotiff_error": "GeoTIFF was saved, but QGIS cannot open it.",
        "save_error": "The image was generated, but an error occurred while saving/georeferencing:\n{error}",
        "custom_prompt": "Custom prompt",
        "placeholder": "E.g. Create a realistic urban parking area with an access road.",
        "strict_tip": "Strongest matching of color, exposure, texture, shadows and orthophoto character.",
        "balanced_tip": "Preserves orthophoto consistency while allowing moderate reconstruction.",
        "creative_tip": "Allows more freedom while preserving aerial perspective and photorealism.",
        "connected": "● OpenAI — connected",
        "setup": "● OpenAI — setup",
        "footer_connected": "● OpenAI",
        "footer_setup": "● OpenAI — not configured",
        "cost_unknown": "≈ —",
        "cost_image_suffix": "/ image",
        "cost_session_suffix": "{count} image(s)",
        "help_title": "Help — Inpaint AI Cloud",
        "help_button": "?",
        "help_html": """
        <h3>Inpaint AI Cloud — Quick guide</h3>
        <p><b>Author / developer:</b> Maciej Galant</p>
        <p><b>Purpose:</b> generative orthophoto editing in QGIS using OpenAI.</p>
        <ol>
          <li><b>Settings:</b> configure OpenAI API in the Settings window.</li>
          <li><b>Area:</b> click <i>Select area on map</i> and draw a polygon — LMB adds a point, RMB finishes.</li>
          <li><b>Description:</b> choose a preset or enter your own instruction.</li>
          <li><b>Advanced:</b> choose the model, quality, context and matching mode.</li>
          <li><b>Generation:</b> accept consent and click <i>GENERATE</i>.</li>
        </ol>
        <p><b>Important:</b> the plugin automatically adds hidden orthophoto-oriented instructions to improve matching of color, exposure, shadows, texture, scale and source image character.</p>
        <p><b>Estimated cost</b> is approximate and refers to one 1024×1024 image. Actual API cost may vary slightly.</p>
        <p><b>Data sent to OpenAI:</b> image crop, mask and prompt — only after the user gives consent.</p>
        <p><b>Tip:</b> if the result blends poorly, use <i>Strict</i>, increase context or shorten the instruction.</p>
        """,
    },
}


def default_language():
    return "pl" if QLocale.system().name().lower().startswith("pl") else "en"


def tr(lang, key, **kwargs):
    lang = lang if lang in TEXTS else "en"
    value = TEXTS[lang].get(key, TEXTS["en"].get(key, key))
    if kwargs:
        try:
            return value.format(**kwargs)
        except Exception:
            return value
    return value

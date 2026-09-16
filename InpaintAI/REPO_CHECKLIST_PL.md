# Inpaint AI Cloud — przygotowanie do QGIS Plugin Repository

Stan: 1.0.0-rc1 / experimental, z poprawioną obsługą wyjątków zgłoszonych przez walidację QGIS.

Commit dla tej poprawki: `Fix silent exception handling flagged by QGIS plugin validation`.

## Repozytorium

- GitHub: https://github.com/maciejgalant/Inpaint-AI
- Issues: https://github.com/maciejgalant/Inpaint-AI/issues
- Autor: Maciej Galant
- E-mail publikacyjny: magal.pl@wp.pl

## Już spełnione

- kod źródłowy w Pythonie,
- brak własnych binariów,
- pakiet znacznie poniżej 20 MB,
- komunikacja sieciowa przez `QgsNetworkAccessManager`,
- klucz API poza kodem wtyczki — QGIS Authentication Manager,
- `README.md`,
- `LICENSE`,
- instrukcja PL i EN,
- informacja o prywatności,
- QGIS 4.x zadeklarowany w metadata,
- plugin oznaczony jako `experimental=True`,
- `homepage`, `repository`, `tracker`, `email` i `tags` uzupełnione,
- brak `__pycache__` w ZIP.

## Do zrobienia przed publikacją

1. Wysłać przygotowany kod do publicznego repozytorium GitHub.
2. Sprawdzić publiczny dostęp do README oraz zakładki Issues.
3. Ustalić numer pierwszej wersji publicznej.
4. Zdecydować, czy pierwsza wersja pozostaje `experimental=True`.
5. Przetestować co najmniej:
   - Windows + QGIS 4,
   - Linux + QGIS 4, jeśli dostępny,
   - projekt z CRS metrycznym,
   - raster lokalny,
   - warstwy usługowe WMS/XYZ,
   - folder zapisu użytkownika,
   - jakości `low`, `high`, `max`.
6. Sprawdzić zachowanie przy:
   - braku internetu,
   - złym API key,
   - braku środków API,
   - anulowaniu żądania,
   - zamknięciu QGIS w trakcie generowania.
7. Uruchomić `scripts/validate_plugin.py`.
8. Zbudować `dist/InpaintAI.zip` przez `scripts/build_plugin_zip.py`.
9. Zainstalować i przetestować dokładnie ten ZIP.
10. Utworzyć odpowiadający wersji tag / GitHub Release.
11. Przesłać przetestowany ZIP do QGIS Plugin Repository.

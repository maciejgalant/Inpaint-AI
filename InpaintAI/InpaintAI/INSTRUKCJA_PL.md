# Inpaint AI Cloud — instrukcja użytkownika

## 1. Do czego służy wtyczka

Inpaint AI Cloud służy do generatywnej edycji ortofotomap bezpośrednio w QGIS.
Użytkownik zaznacza poligon na mapie, opisuje oczekiwaną zmianę, a wtyczka:
1. przygotowuje crop obrazu i maskę,
2. wysyła je do usługi OpenAI Image Edit,
3. odbiera wygenerowany obraz,
4. georeferencjonuje wynik,
5. dodaje wynik jako warstwę rastrową do projektu QGIS.

Wtyczka jest wyspecjalizowana w edycji ortofotomap. Do polecenia użytkownika automatycznie
dodawany jest ukryty prompt techniczny, który wymusza dopasowanie kolorystyki, ekspozycji,
tekstury, cieni, skali i charakteru zobrazowania do otoczenia.

## 2. Wymagania

- QGIS 4.x,
- dostęp do internetu,
- konto OpenAI API z aktywnym rozliczaniem,
- klucz OpenAI API,
- skonfigurowany QGIS Authentication Manager.

ChatGPT Plus/Pro i OpenAI API są rozliczane oddzielnie.

## 3. Pierwsza konfiguracja OpenAI

1. Utwórz klucz API w panelu OpenAI Platform.
2. W Inpaint AI kliknij **Ustawienia**.
3. W sekcji OpenAI wybierz **Skonfiguruj połączenie OpenAI…**.
4. Utwórz lub wybierz konfigurację QGIS typu **API Header**.
5. Ustaw nagłówek:
   - nazwa: `Authorization`
   - wartość: `Bearer TWÓJ_KLUCZ_API`
6. Zapisz konfigurację.

Klucz API nie jest zapisywany w kodzie wtyczki. Przechowuje go QGIS Authentication Manager.

Nigdy nie wklejaj klucza API do promptu ani nie publikuj zrzutu ekranu zawierającego klucz.

## 4. Podstawowy workflow

### Krok 1 — Obszar
Kliknij **Zaznacz obszar na mapie**.

- LPM — dodawanie kolejnych punktów poligonu,
- PPM — zakończenie poligonu.

Zaznaczenie pozostaje widoczne do momentu:
- wygenerowania wyniku,
- kliknięcia **Cofnij zaznaczenie**,
- kliknięcia **Anuluj**.

### Krok 2 — Co wygenerować?
Wybierz preset, np.:
- Parking,
- Droga / ulica asfaltowa,
- Obiekt sportowy,
- Plac zabaw,
- Zieleń miejska,
- Las / zadrzewienie,
- Pole uprawne,
- Usuń obiekt i odtwórz teren.

Możesz zmienić sugerowane polecenie na własne.

Nie trzeba wpisywać za każdym razem informacji typu:
„dopasuj kolorystykę”, „widok z góry”, „zachowaj styl ortofotomapy”.
Wtyczka dodaje te wymagania automatycznie.

### Krok 3 — Generowanie
Zaznacz zgodę na przesłanie cropu i maski do OpenAI i kliknij **GENERUJ**.

Po zakończeniu wynik jest automatycznie:
- zapisywany jako georeferencjonowany GeoTIFF,
- dodawany do bieżącego projektu QGIS.

## 5. Opcje zaawansowane

### Model
**Sunburst** — tryb preferowany do dokładniejszej edycji i inpaintingu.

**Flare** — szybszy wariant do prostszych testów.

### Jakość
Wyższa jakość może zwiększać czas generowania i koszt.

Do testów zalecane:
- `medium`,
- `high`.

### Kontekst
Określa, jak duży obszar wokół zaznaczenia jest przekazywany modelowi jako wzorzec.

Domyślnie: `2.0×`.

Większy kontekst może pomóc w dopasowaniu:
- dróg,
- zabudowy,
- roślinności,
- kolorystyki,
- kierunku cieni.

### Dopasowanie

**Ścisłe** — priorytetem jest wtopienie wyniku w źródłową ortofotomapę.

**Zrównoważone** — kompromis między dopasowaniem i swobodą rekonstrukcji.

**Kreatywne** — model otrzymuje większą swobodę, ale nadal zachowuje perspektywę lotniczą i realizm.

Do typowej pracy na ortofotomapach zalecane jest **Ścisłe**.

## 6. Język

Wtyczka obsługuje:
- Polski,
- English.

Język zmienia się w oknie **Ustawienia**.
Wybrany język jest zapamiętywany.

Prompt techniczny ortofotomapy pozostaje wewnętrznie zoptymalizowany dla modelu,
niezależnie od języka interfejsu.

## 7. Dane wysyłane do OpenAI

Przy generowaniu wtyczka przesyła:
- crop obrazu widocznego w QGIS,
- maskę zaznaczenia,
- końcowe polecenie tekstowe,
- ustawienia modelu i jakości niezbędne do wykonania żądania.

Wtyczka nie zapisuje klucza API w swoim kodzie.

Przed generowaniem użytkownik musi wyrazić zgodę na przesłanie cropu i maski.

## 8. Pliki tymczasowe

Crop, maska i wynik roboczy są tworzone w systemowym katalogu tymczasowym
w podfolderze `InpaintAICloud`.

Warstwa wynikowa jest następnie otwierana w QGIS jako GeoTIFF.

## 9. Typowe problemy

### HTTP 401
Najczęściej oznacza brak poprawnego nagłówka Authorization.
Sprawdź konfigurację API Header w QGIS Authentication Manager.

### Wynik nie pasuje kolorystycznie
Spróbuj:
- trybu **Ścisłe**,
- większego kontekstu,
- krótszego i bardziej jednoznacznego polecenia,
- presetu najlepiej odpowiadającego danemu obiektowi.

### Zaznaczenie pozostaje na mapie
Użyj **Cofnij zaznaczenie** albo rozpocznij nowe zaznaczenie.
Od wersji Alpha 4.1 zaznaczenie jest dodatkowo usuwane z canvasu po poprawnym zakończeniu generowania.

## 10. Ważne

Wygenerowany materiał należy traktować jako materiał syntetyczny.
Nie powinien być przedstawiany jako oryginalne zobrazowanie pomiarowe lub archiwalne bez jasnego oznaczenia.


## 8a. Folder zapisu

W sekcji **ZAPIS** można wskazać katalog bazowy wyników. Wtyczka zapamiętuje wybraną ścieżkę. Każda generacja otrzymuje osobny podfolder z datą i czasem, zawierający `input.png`, `mask.png`, `result.png` oraz georeferencjonowany `result.tif`. Jeśli użytkownik nie wskaże folderu, domyślnie używany jest `InpaintAI_Output` w folderze projektu QGIS, a dla niezapisanego projektu — folder Dokumenty.

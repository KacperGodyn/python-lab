# Fast Translate CLI

`fast-translate` to proste i szybkie narzędzie wiersza poleceń (CLI) służące do tłumaczenia tekstów oraz plików tekstowych. Program korzysta z lokalnej instancji silnika **LibreTranslate**, uruchamianej automatycznie w kontenerze Docker za pomocą Docker Compose.

Dzięki temu Twoje dane nie są przesyłane do zewnętrznych usług komercyjnych (takich jak Google Translate czy DeepL), co gwarantuje pełną prywatność.

---

## Spis treści
- [Funkcje](#funkcje)
- [Wymagania wstępne](#wymagania-wstępne)
- [Instalacja](#instalacja)
- [Użycie i przykłady](#użycie-i-przykłady)
- [Struktura projektu](#struktura-projektu)
- [Historia zapytań](#historii-zapytań)

---

## Funkcje

- **Automatyczne uruchomienie serwera translatora**: Przy pierwszym uruchomieniu narzędzie weryfikuje obecność Dockera i uruchamia lokalną instancję LibreTranslate w tle (na porcie `5000`).
- **Tłumaczenie tekstu**: Tłumaczenie pojedynczych zdań/fraz podanych bezpośrednio w parametrze.
- **Tłumaczenie plików**: Tłumaczenie zawartości plików `.txt` i automatyczny zapis przetłumaczonej wersji pod nazwą `<nazwa>_translated_<język>.txt`.
- **Wykrywanie języka**: Rozpoznawanie języka podanego tekstu wraz z określeniem poziomu pewności (confidence).
- **Alternatywne tłumaczenia**: Wyświetlanie alternatywnych wersji tłumaczeń (opcja `-alt`).
- **Lista języków**: Wyświetlanie obsługiwanych języków docelowych.
- **Historia zapytań**: Automatyczne zapisywanie każdego wykonanego polecenia i jego rezultatu do pliku `history.json`.

---

## Wymagania wstępne

Aby móc korzystać z aplikacji, na komputerze muszą być zainstalowane:
1. **Python 3.8+**
2. **Docker Desktop** (wraz z włączoną obsługą `docker compose`). Narzędzie automatycznie zarządza kontenerem LibreTranslate.

---

## Instalacja

Możesz zainstalować projekt lokalnie w trybie edytowalnym (deweloperskim), aby polecenie `fast-translate` było dostępne globalnie w Twoim systemie:

1. Otwórz terminal w katalogu głównym projektu (tam, gdzie znajduje się plik `pyproject.toml`).
2. Uruchom polecenie:
   ```bash
   pip install -e .
   ```

Po pomyślnej instalacji możesz wywołać narzędzie bezpośrednio za pomocą polecenia `fast-translate`.

---

## Użycie i przykłady

### Wyświetlenie pomocy
Aby zobaczyć wszystkie dostępne opcje i parametry, użyj:
```bash
fast-translate --help
```

Wygeneruje to następujący komunikat pomocy CLI:
```text
usage: fast-translate [-h] [-t TEXT] [-f FILE] [-ls] [-src SOURCE]
                      [-tg TARGET] [-alt ALTERNATIVE] [-d DETECT]

Szybki translator CLI

options:
  -h, --help            show this help message and exit
  -t, --text TEXT       Tekst, który chcesz przetłumaczyć
  -f, --file FILE       Plik, którego zawartość chcesz przetłumaczyć (.txt)
  -ls, --list           Wyswietla liste dostepnych jezykow
  -src, --source SOURCE
                        Język źródłowy
  -tg, --target TARGET  Język docelowy
  -alt, --alternative ALTERNATIVE
                        Wyświetla dodatkowo alternatywne tłumaczenia (liczba)
  -d, --detect DETECT   Wykrywa język tekstu
```


### 1. Tłumaczenie tekstu
Domyślnie język źródłowy jest wykrywany automatycznie (`auto`), a docelowy to angielski (`en`).

```bash
# Tłumaczenie z automatyczną detekcją na język angielski (domyślnie)
fast-translate -t "Dzień dobry, jak się masz?"

# Tłumaczenie z polskiego (pl) na hiszpański (es)
fast-translate -t "Dzień dobry, jak się masz?" -src pl -tg es
```

### 2. Tłumaczenie pliku
Tłumaczenie zawartości pliku `.txt`. Wynik zostanie zapisany w nowym pliku o nazwie z sufiksem docelowego języka.

```bash
fast-translate -f plik.txt -src en -tg pl
# Wynik zostanie zapisany np. w pliku: plik_translated_pl.txt
```

### 3. Alternatywne tłumaczenia
Możesz zażądać wyświetlenia alternatywnych wersji tłumaczenia:

```bash
fast-translate -t "Hello" -alt 3 -tg pl
```

### 4. Wykrywanie języka
Wykrywanie języka wskazanego tekstu bez dokonywania tłumaczenia:

```bash
fast-translate -d "Bonjour tout le monde"
# Wynik: Język wykryty: fr (pewność: 100.0%)
```

### 5. Lista dostępnych języków
Pokazuje obsługiwane języki (zależne od konfiguracji kontenera LibreTranslate):

```bash
fast-translate -ls
```

---

## Struktura projektu

```text
fast-translate/
├── docker-compose.yml       # Konfiguracja kontenera LibreTranslate
├── pyproject.toml           # Metadane i konfiguracja instalacji pakietu Python
├── history.json             # Historia wywołań (tworzona automatycznie)
├── fast_translate/
│   ├── __init__.py
│   └── main.py              # Główny kod źródłowy aplikacji CLI
└── test.py                  # Skrypt testowy
```

---

## Historia zapytań

Każda udana oraz nieudana operacja jest rejestrowana w pliku `history.json` w bieżącym katalogu roboczym. Przykładowy wpis w historii wygląda następująco:

```json
{
    "timestamp": "2026-07-11 18:00:00",
    "command": "fast-translate -t Hello -tg pl",
    "arguments": {
        "text": "Hello",
        "source": "auto",
        "target": "pl"
    },
    "result": {
        "translated_text": "Cześć"
    }
}
```

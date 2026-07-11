import sys
import pytest
import functools
import time
from fast_translate.main import run

def timer(func):
    """Mierzy czas wykonania funkcji i drukuje wynik."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        print(f"[indywidualny czas testu] {func.__name__} -> {elapsed:.2f}s")
        return result
    return wrapper


@pytest.fixture(autouse=True)
def cleanup_sys_argv():
    original_argv = sys.argv.copy()
    yield
    sys.argv = original_argv

@timer
def test_no_arguments(capsys):
    sys.argv = ["fast-translate"]
    with capsys.disabled():
        print("\nTest bez argumentów:")
    with pytest.raises(SystemExit) as exc_info:
        run()
    assert exc_info.value.code == 1

@timer
def test_list_languages(capsys):
    sys.argv = ["fast-translate", "-ls"]
    run()
    captured = capsys.readouterr()
    with capsys.disabled():
        print("\nTest dostępnych języków:")
        print(captured.out.strip())
    assert "Dostępne języki tłumaczenia:" in captured.out

@timer
def test_translation_pl_to_en_with_alternatives(capsys):
    sys.argv = ["fast-translate", "-t", "Czesc!", "-src", "pl", "-tg", "en", "-alt", "3"]
    run()
    captured = capsys.readouterr()
    with capsys.disabled():
        print("\nTest tłumaczenia PL na EN z trzema alternatywnymi tłumaczeniami:")
        print(captured.out.strip())
    assert "Alternatywne tłumaczenia:" in captured.out

@timer
def test_auto_translation(capsys):
    sys.argv = ["fast-translate", "-t", "Jak się masz?"]
    run()
    captured = capsys.readouterr()
    with capsys.disabled():
        print("\nTest automatycznego tłumaczenia \"Jak się masz?\":")
        print(captured.out.strip())
    assert len(captured.out.strip()) > 0

@timer
def test_language_detection(capsys):
    sys.argv = ["fast-translate", "-d", "Hello"]
    run()
    captured = capsys.readouterr()
    with capsys.disabled():
        print("\nTest wykrywania języka: \"Hello\":")
        print(captured.out.strip())
        assert "Język wykryty:" in captured.out.strip()

@timer
def test_file(capsys):
    sys.argv = ["fast-translate", "-f", ".\\test_text_en.txt", "-tg", "es"]
    run()
    captured = capsys.readouterr()
    with capsys.disabled():
        print("\nTest tłumaczenia pliku z EN na ES (test_text_en.txt -> test_text_en_translated_es.txt):")
        print(captured.out.strip())
        assert "Przetłumaczony plik zapisano jako:" in captured.out.strip()

@pytest.mark.xfail(reason="W pustych plikach nie ma nic do przetłumaczenia")
def test_empty_file():
    sys.argv = ["fast-translate", "-f", ".\\fast-translate\\test_text_empty.txt"]
    with pytest.raises(SystemExit) as exc_info:
        assert exc_info.value.code == 1

@pytest.mark.xfail(reason="Plik musi mieć rozszerzenie (.txt)")
def test_bad_ext_file():
    sys.argv = ["fast-translate", "-f", ".\\fast-translate\\test_text_empty.csv"]
    with pytest.raises(SystemExit) as exc_info:
        assert exc_info.value.code == 1

if __name__ == "__main__":
    pytest.main(["-s", __file__])
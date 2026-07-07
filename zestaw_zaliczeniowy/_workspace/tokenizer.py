
import re

class Tokenizer:
    """Konfigurowany tokenizator: HTML strip + case + min length filter."""
    def __init__(self, lower: bool = True, strip_html: bool = True, min_length: int = 1):
        # TODO: zapisz parametry jako atrybuty self.*
        pass

    def tokenize(self, text: str) -> list[str]:
        # 1. jesli self.strip_html: usun znaczniki regex r"<[^>]+>"
        # 2. jesli self.lower: text -> lowercase
        # 3. tokeny = re.findall(r"\w+", text)  (UWAGA: musi lapac polskie litery -> uzyj re.UNICODE)
        # 4. zwroc [t for t in tokeny if len(t) >= self.min_length]
        # TODO
        return []

    def vocab(self, texts: list[str]) -> set[str]:
        # TODO: unia tokenow ze wszystkich tekstow
        return set()

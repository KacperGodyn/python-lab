
import re

class Tokenizer:
    """Konfigurowany tokenizator: HTML strip + case + min length filter."""
    def __init__(self, lower: bool = True, strip_html: bool = True, min_length: int = 1):
        self.lower = lower
        self.strip_html = strip_html
        self.min_length = min_length

    def tokenize(self, text: str) -> list[str]:
        text = re.sub(r"<[^>]+>", "", text) if self.strip_html else text
        tokeny = re.findall(r"\w+", text, flags=re.UNICODE)

        return [t.lower() if self.lower else t for t in tokeny if len(t) >= self.min_length]

    def vocab(self, texts: list[str]) -> set[str]:
        return {s for t in texts for s in self.tokenize(t)}

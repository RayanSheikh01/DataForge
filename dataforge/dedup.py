"""Lexical near-duplicate filter via MinHash/LSH."""

from datasketch import MinHash, MinHashLSH


def _shingles(text: str, n: int = 3) -> set[str]:
    """Word n-grams used for MinHash signatures."""
    raise NotImplementedError


class Deduper:
    """Lexical near-dup via MinHash/LSH over word n-grams. mode 'off' disables."""

    def __init__(self, mode: str = "lexical", threshold: float = 0.85):
        self.mode = mode
        self.threshold = threshold

    def is_duplicate(self, text: str) -> bool:
        """True if text is near-duplicate of something already added."""
        raise NotImplementedError

    def add(self, text: str) -> None:
        """Index text so future calls compare against it."""
        raise NotImplementedError

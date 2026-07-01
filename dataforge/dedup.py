"""Lexical near-duplicate filter via MinHash/LSH."""

from datasketch import MinHash, MinHashLSH

_NUM_PERM = 128


def _shingles(text: str, n: int = 3) -> set[str]:
    """Word n-grams used for MinHash signatures."""
    words = text.split()
    return set(" ".join(words[i : i + n]) for i in range(len(words) - n + 1))


class Deduper:
    """Lexical near-dup via MinHash/LSH over word n-grams. mode 'off' disables.

    `is_duplicate` is pure (query only). Call `add` explicitly to index a kept text.
    """

    def __init__(self, mode: str = "lexical", threshold: float = 0.85):
        self.mode = mode
        self.threshold = threshold
        self.lsh = MinHashLSH(threshold=threshold, num_perm=_NUM_PERM)
        self._id_counter = 0

    def _minhash(self, text: str) -> MinHash:
        m = MinHash(num_perm=_NUM_PERM)
        for shingle in _shingles(text):
            m.update(shingle.encode("utf8"))
        return m

    def is_duplicate(self, text: str) -> bool:
        """True if text is near-duplicate of something already added. No side effects."""
        if self.mode == "off":
            return False
        return len(self.lsh.query(self._minhash(text))) > 0

    def add(self, text: str) -> None:
        """Index text so future is_duplicate calls compare against it."""
        if self.mode == "off":
            return
        self.lsh.insert(str(self._id_counter), self._minhash(text))
        self._id_counter += 1

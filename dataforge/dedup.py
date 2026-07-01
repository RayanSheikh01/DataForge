"""Lexical near-duplicate filter via MinHash/LSH."""

from datasketch import MinHash, MinHashLSH


def _shingles(text: str, n: int = 3) -> set[str]:
    """Word n-grams used for MinHash signatures."""
    words = text.split()
    return set(" ".join(words[i : i + n]) for i in range(len(words) - n + 1))


class Deduper:
    """Lexical near-dup via MinHash/LSH over word n-grams. mode 'off' disables."""

    def __init__(self, mode: str = "lexical", threshold: float = 0.85):
        self.mode = mode
        self.threshold = threshold

    def is_duplicate(self, text: str) -> bool:
        """True if text is near-duplicate of something already added."""
        if self.mode == "off":
            return False
        shingles = _shingles(text)
        m = MinHash(num_perm=128)
        for shingle in shingles:
            m.update(shingle.encode("utf8"))
        if not hasattr(self, "lsh"):
            self.lsh = MinHashLSH(threshold=self.threshold, num_perm=128)
            self._id_counter = 0
        # check for duplicates
        for key in self.lsh.query(m):
            return True
        # add to index
        self.lsh.insert(str(self._id_counter), m)
        self._id_counter += 1
        return False
        
    def add(self, text: str) -> None:
        """Index text so future calls compare against it."""
        if self.mode == "off":
            return
        shingles = _shingles(text)
        m = MinHash(num_perm=128)
        for shingle in shingles:
            m.update(shingle.encode("utf8"))
        if not hasattr(self, "lsh"):
            self.lsh = MinHashLSH(threshold=self.threshold, num_perm=128)
            self._id_counter = 0
        self.lsh.insert(str(self._id_counter), m)
        self._id_counter += 1
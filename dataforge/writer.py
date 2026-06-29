"""Output writer: append-only JSONL (resumable) + HF dataset export."""

import json

from datasets import Dataset


class Writer:
    def __init__(self, out_dir: str):
        """Ensure out_dir exists; set data.jsonl path."""
        raise NotImplementedError

    def append(self, record: dict) -> None:
        """Append one record as a JSON line (flush)."""
        raise NotImplementedError

    def count_existing(self) -> int:
        """Number of records already in data.jsonl (0 if absent)."""
        raise NotImplementedError

    def used_seed_combos(self) -> set[tuple]:
        """Seed combos already produced, for resume exclude set."""
        raise NotImplementedError


def export_dataset(out_dir: str, push_to_hub: bool = False, repo_id: str | None = None):
    """Read data.jsonl -> datasets.Dataset -> save_to_disk(out_dir/hf_dataset).
    Optionally push_to_hub."""
    raise NotImplementedError

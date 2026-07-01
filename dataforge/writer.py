"""Output writer: append-only JSONL (resumable) + HF dataset export."""

import json

from datasets import Dataset


class Writer:
    def __init__(self, out_dir: str):
        """Ensure out_dir exists; set data.jsonl path."""
        self.out_dir = out_dir
        self.jsonl_path = f"{out_dir}/data.jsonl"
        
        
    def append(self, record: dict) -> None:
        """Append one record as a JSON line (flush)."""
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            
    def count_existing(self) -> int:
        """Number of records already in data.jsonl (0 if absent)."""
        try:
            with open(self.jsonl_path, "r", encoding="utf-8") as f:
                return sum(1 for _ in f)
        except FileNotFoundError:
            return 0

    def used_seed_combos(self) -> set[tuple]:
        """Seed combos already produced, for resume exclude set."""
        combos = set()
        try:
            with open(self.jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    seed_combo = tuple(record.get("seed_combo", []))
                    combos.add(seed_combo)
        except FileNotFoundError:
            pass
        return combos


def export_dataset(out_dir: str, push_to_hub: bool = False, repo_id: str | None = None):
    """Read data.jsonl -> datasets.Dataset -> save_to_disk(out_dir/hf_dataset).
    Optionally push_to_hub."""
    jsonl_path = f"{out_dir}/data.jsonl"
    hf_dataset_dir = f"{out_dir}/hf_dataset"
    dataset = Dataset.from_json(jsonl_path)
    dataset.save_to_disk(hf_dataset_dir)
    if push_to_hub:
        if repo_id is None:
            raise ValueError("repo_id must be provided when push_to_hub is True")
        dataset.push_to_hub(repo_id)

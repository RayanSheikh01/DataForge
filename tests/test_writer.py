"""Tests for dataforge.writer."""

import pytest


def test_append_and_count(tmp_path):
    """Two appends -> 2 JSONL lines -> count_existing()==2."""
    from dataforge.writer import Writer

    writer = Writer(out_dir=tmp_path)
    writer.append({"a": 1})
    writer.append({"b": 2})
    assert writer.count_existing() == 2


def test_resume_does_not_truncate(tmp_path):
    """Reopening Writer and appending keeps prior records."""
    from dataforge.writer import Writer

    writer1 = Writer(out_dir=tmp_path)
    writer1.append({"a": 1})
    writer1.append({"b": 2})
    assert writer1.count_existing() == 2
    
    writer2 = Writer(out_dir=tmp_path)
    writer2.append({"c": 3})
    assert writer2.count_existing() == 3


def test_export_loadable(tmp_path):
    """export_dataset -> datasets.load_from_disk returns expected columns."""
    from dataforge.writer import Writer, export_dataset
    from datasets import load_from_disk

    writer = Writer(out_dir=tmp_path)
    writer.append({"prompt": "Q1", "response": "A1"})
    writer.append({"prompt": "Q2", "response": "A2"})
    export_dataset(out_dir=tmp_path)
    dataset = load_from_disk(f"{tmp_path}/hf_dataset")
    assert set(dataset.column_names) == {"prompt", "response"}

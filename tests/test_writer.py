"""Tests for dataforge.writer."""

import pytest


@pytest.mark.skip(reason="TODO: implement Writer")
def test_append_and_count(tmp_path):
    """Two appends -> 2 JSONL lines -> count_existing()==2."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO: implement Writer")
def test_resume_does_not_truncate(tmp_path):
    """Reopening Writer and appending keeps prior records."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO: implement export_dataset")
def test_export_loadable(tmp_path):
    """export_dataset -> datasets.load_from_disk returns expected columns."""
    raise NotImplementedError

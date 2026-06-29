"""Integration test for dataforge.pipeline.Pipeline (uses FakeLLM)."""

import pytest

from tests.fakes import FakeLLM


@pytest.mark.skip(reason="TODO: implement Pipeline.run")
def test_full_loop_accept_retry_discard_dedup(tmp_path):
    """Scripted FakeLLM: sample1 passes first try; sample2 fails twice then passes
    (attempts==3); sample3 always fails (discarded); a dup is rejected.
    Assert RunStats counts and final JSONL line count."""
    raise NotImplementedError

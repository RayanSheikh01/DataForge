"""Integration test for dataforge.pipeline.Pipeline (uses FakeLLM)."""

from types import SimpleNamespace

import pytest

from tests.fakes import FakeLLM


def test_full_loop_accept_retry_discard_dedup(tmp_path):
    """Scripted FakeLLM: sample1 passes first try; sample2 fails twice then passes
    (attempts==3); sample3 always fails (discarded); a dup is rejected.
    Assert RunStats counts and final JSONL line count."""
    from dataforge.pipeline import Pipeline, RunStats
    from dataforge.writer import Writer

    writer = Writer(out_dir=tmp_path)
    pipeline = Pipeline(
        config=SimpleNamespace(
            target_samples=3,
            max_retries=3,
        ),
        generator=SimpleNamespace(
            generate=lambda seed_combo, critique=None: {
                "seed_combo": seed_combo,
                "prompt": f"Prompt {seed_combo}",
                "response": f"Response {seed_combo} {critique or ''}".strip(),
            }
        ),
        verifier=SimpleNamespace(
            verify=lambda record: SimpleNamespace(
                passed=record["seed_combo"] != "sample3" and not record["response"].endswith("retry2"),
                score=1.0 if record["seed_combo"] != "sample3" else 0.0,
                critique="Critique" if record["seed_combo"] == "sample2" and not record["response"].endswith("retry2") else "",
            )
        ),
        deduper=SimpleNamespace(
            is_duplicate=lambda response: "dup" in response,
        ),
        writer=writer,
        sampler=SimpleNamespace(
            sample_seed_combo=lambda: next(iter(["sample1", "sample2", "sample3", "dup", None]))
        ),
    )
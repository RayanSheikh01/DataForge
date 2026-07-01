"""Integration test for dataforge.pipeline.Pipeline (fake components)."""

import json
from types import SimpleNamespace

from dataforge.generator import Candidate
from dataforge.pipeline import Pipeline
from dataforge.verifier import Verdict
from dataforge.writer import Writer


def test_full_loop_accept_retry_discard_dedup(tmp_path):
    """s1 passes first try; s2 fails once then passes (attempts==2);
    s3 always fails (discarded); dup collides with s1's response (rejected);
    seeds then exhaust. Assert RunStats + JSONL contents."""

    def generate(seed, critique=None):
        sid = seed["id"]
        if sid == "dup":
            resp = "resp-s1"                      # collides with accepted s1
        else:
            resp = f"resp-{sid}" + ("-fixed" if critique else "")
        return Candidate(prompt=f"p-{sid}", response=resp)

    def verify(candidate):
        r = candidate.response
        if r.startswith("resp-s3"):
            return Verdict(passed=False, score=0, critique="bad")
        if r == "resp-s2":                        # first attempt, no critique yet
            return Verdict(passed=False, score=0, critique="add detail")
        return Verdict(passed=True, score=10, critique="")

    seen: set[str] = set()
    seeds = iter([{"id": "s1"}, {"id": "s2"}, {"id": "s3"}, {"id": "dup"}])

    writer = Writer(out_dir=tmp_path)
    pipeline = Pipeline(
        config=SimpleNamespace(target_samples=3, max_retries=3, score_threshold=7),
        generator=SimpleNamespace(generate=generate),
        verifier=SimpleNamespace(verify=verify),
        deduper=SimpleNamespace(
            is_duplicate=lambda t: t in seen,
            add=lambda t: seen.add(t),
        ),
        writer=writer,
        sampler=SimpleNamespace(next=lambda: next(seeds)),
    )

    stats = pipeline.run()

    assert stats.accepted == 2       # s1, s2
    assert stats.discarded == 1      # s3
    assert stats.duplicates == 1     # dup
    assert writer.count_existing() == 2

    records = [json.loads(l) for l in open(writer.jsonl_path, encoding="utf-8")]
    by_id = {r["seed_meta"]["id"]: r for r in records}
    assert by_id["s1"]["attempts"] == 1
    assert by_id["s2"]["attempts"] == 2   # one retry after critique

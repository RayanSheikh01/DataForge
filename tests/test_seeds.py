"""Tests for dataforge.seeds.SeedSampler."""

import pytest


def test_yields_unique_combos():
    """next() returns each topic*persona combo once; remaining counts down."""
    from dataforge.seeds import SeedSampler

    seeds = {"topic": ["t1", "t2"], "persona": ["p1", "p2"]}
    sampler = SeedSampler(seeds=seeds, seed=42)

    combos = []
    while sampler.remaining > 0:
        combos.append(sampler.next())

    assert len(combos) == 4
    assert all(c in [{"topic": t, "persona": p} for t in ["t1", "t2"] for p in ["p1", "p2"]] for c in combos)


def test_exhaustion_raises():
    """After all combos consumed, next() raises."""
    from dataforge.seeds import SeedSampler

    seeds = {"topic": ["t1"], "persona": ["p1"]}
    sampler = SeedSampler(seeds=seeds)

    assert sampler.remaining == 1
    sampler.next()
    assert sampler.remaining == 0

    with pytest.raises(StopIteration):
        sampler.next()


def test_exclude_skips_used_combos():
    """Combos in exclude= are not returned (resume support)."""
    from dataforge.seeds import SeedSampler

    seeds = {"topic": ["t1", "t2"], "persona": ["p1", "p2"]}
    exclude = {("t1", "p1"), ("t2", "p2")}
    sampler = SeedSampler(seeds=seeds, exclude=exclude, seed=42)

    combos = []
    while sampler.remaining > 0:
        combos.append(sampler.next())

    assert len(combos) == 2
    assert all(c in [{"topic": t, "persona": p} for t in ["t1", "t2"] for p in ["p1", "p2"]] for c in combos)
    assert all((c["topic"], c["persona"]) not in exclude for c in combos)

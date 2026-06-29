"""Tests for dataforge.seeds.SeedSampler."""

import pytest


@pytest.mark.skip(reason="TODO: implement SeedSampler")
def test_yields_unique_combos():
    """next() returns each topic*persona combo once; remaining counts down."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO: implement SeedSampler")
def test_exhaustion_raises():
    """After all combos consumed, next() raises."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO: implement SeedSampler")
def test_exclude_skips_used_combos():
    """Combos in exclude= are not returned (resume support)."""
    raise NotImplementedError

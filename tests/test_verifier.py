"""Tests for dataforge.verifier.Verifier (uses FakeLLM)."""

import pytest

from tests.fakes import FakeLLM


@pytest.mark.skip(reason="TODO: implement Verifier.verify")
def test_parses_verdict():
    """Verdict JSON -> Verdict(passed, score, critique)."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO: implement Verifier.verify")
def test_malformed_verdict_is_conservative_reject():
    """Unparseable output -> passed=False, low score, no crash."""
    raise NotImplementedError

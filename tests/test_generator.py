"""Tests for dataforge.generator.Generator (uses FakeLLM)."""

import pytest

from tests.fakes import FakeLLM


@pytest.mark.skip(reason="TODO: implement Generator.generate")
def test_renders_seed_and_parses_candidate():
    """Seed values appear in sent prompt; JSON output parses to Candidate."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO: implement Generator.generate")
def test_malformed_output_raises_parse_error():
    """Non-JSON model output raises ParseError."""
    raise NotImplementedError

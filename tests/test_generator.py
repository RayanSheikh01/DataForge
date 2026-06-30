"""Tests for dataforge.generator.Generator (uses FakeLLM)."""

from dataforge.generator import Generator

import pytest

from tests.fakes import FakeLLM


def test_renders_seed_and_parses_candidate():
    """Seed values appear in sent prompt; JSON output parses to Candidate."""
    template = "Hello {topic} {persona}. Critique: {critique}"
    llm = FakeLLM(
        responses=[
            "PROMPT: Hello t1 p1. Critique: Good\nRESPONSE: Response text"
        ]
    )
    gen = Generator(llm=llm, template_str=template)
    seed = {"topic": "t1", "persona": "p1"}
    critique = "Good"
    candidate = gen.generate(seed=seed, critique=critique)

    assert candidate.prompt == "Hello t1 p1. Critique: Good"
    assert candidate.response == "Response text"
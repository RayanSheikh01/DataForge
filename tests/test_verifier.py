"""Tests for dataforge.verifier.Verifier (uses FakeLLM)."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from dataforge.verifier import Verifier
from tests.fakes import FakeLLM

VERIFY_TEMPLATE = Path(__file__).parent.parent / "templates" / "verify.j2"


def test_parses_verdict():
    """Verdict JSON -> Verdict(passed, score, critique)."""
    template_str = VERIFY_TEMPLATE.read_text()
    response = json.dumps({'passed': True, 'score': 0.8, 'critique': 'Good job!'})
    verifier = Verifier(llm=FakeLLM(responses=[response]), template_str=template_str)
    candidate = SimpleNamespace(prompt='What is 2+2?', response='4')
    verdict = verifier.verify(candidate)
    assert verdict.passed is True
    assert verdict.score == 0.8
    assert verdict.critique == 'Good job!'
    



def test_malformed_verdict_is_conservative_reject():
    """Unparseable output -> passed=False, low score, no crash."""
    template_str = VERIFY_TEMPLATE.read_text()
    response = "This is not JSON"
    verifier = Verifier(llm=FakeLLM(responses=[response]), template_str=template_str)
    candidate = SimpleNamespace(prompt='What is 2+2?', response='4')
    verdict = verifier.verify(candidate)
    assert verdict.passed is False
    assert verdict.score == 0
    assert verdict.critique == 'Unparseable verdict'

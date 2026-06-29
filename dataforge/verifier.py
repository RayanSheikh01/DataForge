"""Verifier: render verify template, call LLM, parse a Verdict."""

from dataclasses import dataclass


@dataclass
class Verdict:
    passed: bool
    score: int
    critique: str


class Verifier:
    def __init__(self, llm, template_str: str):
        self.llm = llm
        self.template_str = template_str

    def verify(self, candidate) -> Verdict:
        """Render verify template with candidate, call llm, parse verdict JSON.
        On unparseable output return conservative reject."""
        raise NotImplementedError

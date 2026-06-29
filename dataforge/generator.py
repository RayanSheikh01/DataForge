"""Generator: render gen template, call LLM, parse a Candidate pair."""

from dataclasses import dataclass


@dataclass
class Candidate:
    prompt: str
    response: str


class ParseError(Exception):
    ...


class Generator:
    def __init__(self, llm, template_str: str):
        self.llm = llm
        self.template_str = template_str

    def generate(self, seed: dict, critique: str | None = None) -> Candidate:
        """Render template with seed (+ optional critique), call llm,
        parse model output into Candidate. Raise ParseError if unparseable."""
        raise NotImplementedError

"""Verifier: render verify template, call LLM, parse a Verdict."""

from dataclasses import dataclass
from json import JSONDecodeError


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
        template = self.template_str.format(**vars(candidate))
        response = self.llm.chat(messages=[{"role": "user", "content": template}])
        # parse json
        try:
            import json

            data = json.loads(response)
            return Verdict(
                passed=data["passed"],
                score=data["score"],
                critique=data["critique"],
            )
        except (JSONDecodeError, KeyError):
            return Verdict(passed=False, score=0, critique="Unparseable verdict")
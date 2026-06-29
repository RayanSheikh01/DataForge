"""Offline deterministic LLM double for tests."""


class FakeLLM:
    """Returns canned responses. `responses` is a list[str] consumed in order,
    or a callable(messages) -> str for dynamic behavior. Records all calls."""

    def __init__(self, responses):
        self.responses = responses
        self.calls = []
        self._i = 0

    def chat(self, messages: list[dict], temperature: float = 0.8) -> str:
        self.calls.append(messages)
        if callable(self.responses):
            return self.responses(messages)
        resp = self.responses[self._i]
        self._i += 1
        return resp

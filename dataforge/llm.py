"""Ollama OpenAI-compatible chat client with retry/backoff."""

from typing import Protocol


class LLMClient(Protocol):
    def chat(self, messages: list[dict], temperature: float = 0.8) -> str: ...


class LLM:
    """Ollama OpenAI-compatible client. POST {base_url}/chat/completions."""

    def __init__(self, model: str, base_url: str, max_attempts: int = 3):
        self.model = model
        self.base_url = base_url
        self.max_attempts = max_attempts

    def chat(self, messages: list[dict], temperature: float = 0.8) -> str:
        """Call endpoint; retry w/ exponential backoff on conn/timeout.
        Raise after max_attempts. Return assistant message content."""
        raise NotImplementedError

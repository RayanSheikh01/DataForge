"""Ollama OpenAI-compatible chat client with retry/backoff."""

import time
from typing import Optional, Protocol

import httpx


class LLMClient(Protocol):
    def chat(self, messages: list[dict], temperature: float = 0.8) -> str: ...


class LLM:
    """Ollama OpenAI-compatible client. POST {base_url}/chat/completions."""

    def __init__(
        self,
        model: str,
        base_url: str,
        max_attempts: int = 3,
        client: Optional[httpx.Client] = None,
    ):
        self.model = model
        self.base_url = base_url
        self.max_attempts = max_attempts
        self._client = client or httpx.Client()

    def chat(self, messages: list[dict], temperature: float = 0.8) -> str:
        """Call endpoint; retry w/ exponential backoff on conn/timeout.
        Raise after max_attempts. Return assistant message content."""
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        for attempt in range(1, self.max_attempts + 1):
            try:
                response = self._client.post(url, json=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.max_attempts:
                    raise
                time.sleep(2 ** (attempt - 1))

        raise RuntimeError("unreachable: max_attempts must be >= 1")

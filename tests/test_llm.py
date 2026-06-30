"""Tests for dataforge.llm — retry/backoff via httpx.MockTransport."""

import httpx
import pytest

from dataforge.llm import LLM


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_retries_then_succeeds(monkeypatch):
    """Transport fails twice then 200 -> chat returns content after 3 attempts."""
    monkeypatch.setattr("dataforge.llm.time.sleep", lambda _: None)

    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ConnectError("Connection Error", request=request)
        if calls["n"] == 2:
            raise httpx.TimeoutException("Timeout", request=request)
        return httpx.Response(
            200, json={"choices": [{"message": {"content": "Hello"}}]}
        )

    llm = LLM(model="m", base_url="http://x", max_attempts=3, client=_client(handler))
    result = llm.chat(messages=[{"role": "user", "content": "Hi"}])

    assert result == "Hello"
    assert calls["n"] == 3


def test_raises_after_max_attempts(monkeypatch):
    """Persistent failure raises after max_attempts."""
    monkeypatch.setattr("dataforge.llm.time.sleep", lambda _: None)

    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        raise httpx.ConnectError("Connection Error", request=request)

    llm = LLM(model="m", base_url="http://x", max_attempts=3, client=_client(handler))
    with pytest.raises(httpx.ConnectError):
        llm.chat(messages=[{"role": "user", "content": "Hi"}])

    assert calls["n"] == 3

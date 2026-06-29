"""Tests for dataforge.llm — retry/backoff via httpx.MockTransport."""

import pytest


@pytest.mark.skip(reason="TODO: implement LLM.chat")
def test_retries_then_succeeds():
    """Transport fails twice then 200 -> chat returns content after 3 attempts."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO: implement LLM.chat")
def test_raises_after_max_attempts():
    """Persistent failure raises after max_attempts."""
    raise NotImplementedError

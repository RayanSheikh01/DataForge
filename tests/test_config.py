"""Tests for dataforge.config — write these first, watch them fail."""

import pytest

# from dataforge.config import load_config
# from pydantic import ValidationError


@pytest.mark.skip(reason="TODO: implement load_config")
def test_loads_valid_yaml(tmp_path):
    """A well-formed YAML parses into Config with expected fields."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO: implement load_config")
def test_rejects_bad_config(tmp_path):
    """Missing required field / out-of-range threshold raises ValidationError."""
    raise NotImplementedError

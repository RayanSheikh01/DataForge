"""Tests for dataforge.config — write these first, watch them fail."""

import pytest
from pydantic import ValidationError

from dataforge.config import load_config

"""load a temp YAML, assert fields parse; assert bad
config (missing `task`, threshold out of range) raises `ValidationError`."""


def test_loads_valid_yaml(tmp_path):
    # load a temp YAML, assert fields parse
    file = tmp_path / "config.yaml"
    file.write_text("""
task: "my_task"
model:
  generator: "my_generator"
  verifier: "my_verifier"
target_samples: 100
score_threshold: 5
seeds:
  my_seed:
    - "seed1"
    - "seed2"
generator_template: "gen_template"
verifier_template: "ver_template"
output:
  dir: "output_dir"
""")
    file_path = str(file)
    config = load_config(file_path)
    assert config.task == "my_task"
    assert config.model.generator == "my_generator"
    assert config.model.verifier == "my_verifier"
    assert config.target_samples == 100
    assert config.score_threshold == 5
    assert config.seeds["my_seed"] == ["seed1", "seed2"]
    assert config.generator_template == "gen_template"
    assert config.verifier_template == "ver_template"
    assert config.output.dir == "output_dir"


def test_rejects_bad_config(tmp_path):
    """Missing required field / out-of-range threshold raises ValidationError."""
    file = tmp_path / "bad_config.yaml"
    file.write_text("""
model:
  generator: "my_generator"
  verifier: "my_verifier"
target_samples: 100
score_threshold: 15  # out of range
seeds:
  my_seed:
    - "seed1"
generator_template: "gen_template"
verifier_template: "ver_template"
output:
  dir: "output_dir"
""")
    file_path = str(file)
    with pytest.raises(ValidationError):  # Replace Exception with ValidationError when pydantic is available
        load_config(file_path)

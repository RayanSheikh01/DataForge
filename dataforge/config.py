"""Task configuration: load + validate YAML into a typed Config."""

from pydantic import BaseModel, Field


class ModelCfg(BaseModel):
    generator: str
    verifier: str
    base_url: str = "http://localhost:11434/v1"


class DedupCfg(BaseModel):
    mode: str = "lexical"          # lexical | embedding | off
    threshold: float = 0.85


class OutputCfg(BaseModel):
    dir: str
    push_to_hub: bool = False


class Config(BaseModel):
    task: str
    model: ModelCfg
    target_samples: int = Field(gt=0)
    max_retries: int = Field(ge=0, default=3)
    score_threshold: int = Field(ge=1, le=10)
    dedup: DedupCfg = DedupCfg()
    seeds: dict[str, list[str]]
    generator_template: str
    verifier_template: str
    output: OutputCfg


def load_config(path: str) -> Config:
    """Read YAML file, return validated Config. Raises ValidationError on bad input."""
    import yaml
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return Config(**data)

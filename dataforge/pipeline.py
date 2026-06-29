"""Pipeline orchestrator: generate -> verify -> retry-with-critique -> emit/discard."""

from dataclasses import dataclass


@dataclass
class RunStats:
    accepted: int
    discarded: int
    duplicates: int


class Pipeline:
    def __init__(self, config, generator, verifier, deduper, writer, sampler):
        self.config = config
        self.generator = generator
        self.verifier = verifier
        self.deduper = deduper
        self.writer = writer
        self.sampler = sampler

    def run(self) -> RunStats:
        """Loop until accepted == target_samples or seeds exhausted.
        Per sample: generate -> verify -> retry-with-critique (max_retries) ->
        dedup check -> append/accept or discard. See design.md 'Pipeline loop'."""
        raise NotImplementedError


def build_pipeline(config) -> Pipeline:
    """Wire real LLM-backed generator/verifier/deduper/writer/sampler from config.
    Reads template files, applies resume exclude set from writer.used_seed_combos()."""
    raise NotImplementedError

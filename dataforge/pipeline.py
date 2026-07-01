"""Pipeline orchestrator: generate -> verify -> retry-with-critique -> emit/discard."""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


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

    def _accepted(self, verdict) -> bool:
        return verdict.passed and verdict.score >= self.config.score_threshold

    def _produce(self, seed):
        """Generate + verify with retry-on-critique. Return (candidate, verdict, attempts)."""
        max_attempts = max(1, self.config.max_retries)
        critique = None
        candidate = verdict = None
        for attempt in range(1, max_attempts + 1):
            candidate = self.generator.generate(seed, critique=critique)
            verdict = self.verifier.verify(candidate)
            if self._accepted(verdict):
                return candidate, verdict, attempt
            critique = verdict.critique
        return candidate, verdict, max_attempts

    def _record(self, seed, candidate, verdict, attempts) -> dict:
        model_cfg = getattr(self.config, "model", None)
        return {
            "prompt": candidate.prompt,
            "response": candidate.response,
            "seed_meta": seed,
            "seed_combo": list(seed.values()),
            "verifier_score": verdict.score,
            "attempts": attempts,
            "model": getattr(model_cfg, "generator", None),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def run(self) -> RunStats:
        """Loop until accepted == target_samples or seeds exhausted.
        Per sample: generate -> verify -> retry-with-critique (max_retries) ->
        dedup check -> append/accept or discard. See design.md 'Pipeline loop'."""
        accepted = self.writer.count_existing()  # resume: existing records count
        stats = RunStats(accepted=accepted, discarded=0, duplicates=0)

        while accepted < self.config.target_samples:
            try:
                seed = self.sampler.next()
            except StopIteration:
                break  # seed space exhausted

            candidate, verdict, attempts = self._produce(seed)
            assert candidate is not None and verdict is not None  # _produce runs >=1 attempt

            if not self._accepted(verdict):
                stats.discarded += 1
                continue

            if self.deduper.is_duplicate(candidate.response):
                stats.duplicates += 1
                continue

            self.writer.append(self._record(seed, candidate, verdict, attempts))
            self.deduper.add(candidate.response)
            accepted += 1
            stats.accepted = accepted

        return stats


def build_pipeline(config) -> Pipeline:
    """Wire real LLM-backed generator/verifier/deduper/writer/sampler from config.
    Reads template files, applies resume exclude set from writer.used_seed_combos()."""
    from .dedup import Deduper
    from .generator import Generator
    from .llm import LLM
    from .seeds import SeedSampler
    from .verifier import Verifier
    from .writer import Writer

    gen_llm = LLM(model=config.model.generator, base_url=config.model.base_url)
    ver_llm = LLM(model=config.model.verifier, base_url=config.model.base_url)

    gen_template = Path(config.generator_template).read_text(encoding="utf-8")
    ver_template = Path(config.verifier_template).read_text(encoding="utf-8")

    writer = Writer(out_dir=config.output.dir)
    sampler = SeedSampler(seeds=config.seeds, exclude=writer.used_seed_combos())

    return Pipeline(
        config=config,
        generator=Generator(llm=gen_llm, template_str=gen_template),
        verifier=Verifier(llm=ver_llm, template_str=ver_template),
        deduper=Deduper(mode=config.dedup.mode, threshold=config.dedup.threshold),
        writer=writer,
        sampler=sampler,
    )

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
        while self.writer.count_existing() < self.config.target_samples:
            seed_combo = self.sampler.sample_seed_combo()
            if seed_combo is None:
                break  # exhausted
            record = self.generator.generate(seed_combo)
            verdict = self.verifier.verify(record)
            if not verdict.passed:
                for _ in range(self.config.max_retries):
                    record = self.generator.generate(seed_combo, critique=verdict.critique)
                    verdict = self.verifier.verify(record)
                    if verdict.passed:
                        break
            if verdict.passed and not self.deduper.is_duplicate(record["response"]):
                self.writer.append(record)
            else:
                # discard
                pass

def build_pipeline(config) -> Pipeline:
    """Wire real LLM-backed generator/verifier/deduper/writer/sampler from config.
    Reads template files, applies resume exclude set from writer.used_seed_combos()."""
    
    llm = config.llm_class(**config.llm_kwargs)
    
    pipeline = Pipeline(
        config=config,
        generator=config.generator_class(llm=llm, template_path=config.generator_template_path),
        verifier=config.verifier_class(llm=llm, template_path=config.verifier_template_path),
        deduper=config.deduper_class(mode=config.deduper_mode, threshold=config.deduper_threshold),
        writer=config.writer_class(out_dir=config.out_dir),
        sampler=config.sampler_class(seed_combos=config.seed_combos, exclude_set=config.writer_class(out_dir=config.out_dir).used_seed_combos()),
    )
    
    return pipeline
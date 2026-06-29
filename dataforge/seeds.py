"""Seed combination sampler for generation diversity."""

import itertools
import random


class SeedSampler:
    """Samples unique combinations across seed dimensions."""

    def __init__(
        self,
        seeds: dict[str, list[str]],
        exclude: set[tuple] | None = None,
        seed: int | None = None,
    ):
        """Build full combo space (itertools.product), drop excluded, shuffle."""
        raise NotImplementedError

    @property
    def remaining(self) -> int:
        raise NotImplementedError

    def next(self) -> dict:
        """Return next unused combo as {dimension: value}. Raise when exhausted."""
        raise NotImplementedError

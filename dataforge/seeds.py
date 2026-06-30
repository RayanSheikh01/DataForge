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
        self._seeds = seeds
        self._exclude = exclude or set()
        self._combos = list(
            filter(
                lambda c: c not in self._exclude,
                itertools.product(*self._seeds.values()),
            )
        )
        if seed is not None:
            random.seed(seed)
        random.shuffle(self._combos)
        self._index = 0

    @property
    def remaining(self) -> int:
        """Return number of unused combos remaining."""
        return len(self._combos) - self._index

    def next(self) -> dict:
        """Return next unused combo as {dimension: value}. Raise when exhausted."""
        if self._index >= len(self._combos):
            raise StopIteration("No more unique combinations available.")
        combo = self._combos[self._index]
        self._index += 1
        return dict(zip(self._seeds.keys(), combo))

"""Tests for dataforge.dedup.Deduper."""

import pytest

from dataforge.dedup import Deduper


def test_flags_exact_and_near_duplicates():
    """Added text + a minor edit are duplicates; unrelated text is not."""
    dedup = Deduper(mode="lexical", threshold=0.85)
    # Long enough that a single-token edit is a small fraction of the 3-gram shingles.
    text1 = (
        "The quick brown fox jumps over the lazy dog while the sun sets slowly "
        "behind the tall green hills near the quiet river bank today."
    )
    text2 = text1                       # exact duplicate
    text3 = text1[:-1] + "!"            # minor edit: trailing '.' -> '!'
    text4 = "A completely different sentence about something else entirely."
    dedup.add(text1)
    assert dedup.is_duplicate(text2) is True
    assert dedup.is_duplicate(text3) is True
    assert dedup.is_duplicate(text4) is False

def test_mode_off_never_flags():
    """mode='off' returns False for everything."""
    dedup = Deduper(mode="off", threshold=0.85)
    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "The quick brown fox jumps over the lazy dog."
    assert not dedup.is_duplicate(text1)
    assert not dedup.is_duplicate(text2)


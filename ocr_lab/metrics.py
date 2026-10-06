from __future__ import annotations

import re
from collections.abc import Sequence
from typing import TypeVar


Item = TypeVar("Item")


def normalize_text(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", value.lower()).split())


def sequence_distance(expected: Sequence[Item], actual: Sequence[Item]) -> int:
    previous = list(range(len(actual) + 1))
    for row, expected_char in enumerate(expected, start=1):
        current = [row]
        for column, actual_char in enumerate(actual, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (expected_char != actual_char),
                )
            )
        previous = current
    return previous[-1]


def edit_distance(expected: str, actual: str) -> int:
    return sequence_distance(expected, actual)


def evaluate(expected: str, actual: str) -> dict[str, float | int | str]:
    expected_normalized = normalize_text(expected)
    actual_normalized = normalize_text(actual)
    character_errors = edit_distance(expected_normalized, actual_normalized)
    expected_words = expected_normalized.split()
    actual_words = actual_normalized.split()
    word_errors = sequence_distance(expected_words, actual_words)
    return {
        "expected": expected_normalized,
        "actual": actual_normalized,
        "character_errors": character_errors,
        "character_error_rate": round(character_errors / max(1, len(expected_normalized)), 4),
        "word_errors": word_errors,
        "exact_match": expected_normalized == actual_normalized,
    }

import re
from typing import Set


def _preprocess(text: str) -> Set[str]:
    return set(re.findall(r'\b\w+\b', text.lower()))


def compute_similarity_score(source_text: str, reference_text: str) -> float:
    source_tokens = _preprocess(source_text)
    reference_tokens = _preprocess(reference_text)

    if not source_tokens or not reference_tokens:
        return 0.0

    intersection = source_tokens & reference_tokens
    union = source_tokens | reference_tokens

    return len(intersection) / len(union)

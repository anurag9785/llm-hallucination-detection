
from backend.semantic_matcher import find_similar_evidence


def test_semantic_matching():
    evidence = [
        "Earth revolves around the Sun.",
        "Water has the chemical formula H2O.",
        "Mars is known as the Red Planet."
    ]

    results = find_similar_evidence(
        "The Earth moves around our Sun.",
        evidence
    )

    assert len(results) > 0
    assert results[0]["fact"] == "Earth revolves around the Sun."

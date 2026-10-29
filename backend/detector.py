
import re

from backend.semantic_matcher import find_similar_evidence


EVIDENCE = [
    {
        "fact": "Earth revolves around the Sun.",
        "keywords": ["earth", "revolves", "sun"],
    },
    {
        "fact": "The Sun is a star at the center of the Solar System.",
        "keywords": ["sun", "star"],
    },
    {
        "fact": "The Sun is a star.",
        "keywords": ["sun", "star"],
    },
    {
        "fact": "Earth is a planet in the Solar System.",
        "keywords": ["earth", "planet", "solar system"],
    },
    {
        "fact": "Water has the chemical formula H2O.",
        "keywords": ["water", "h2o"],
    },
    {
        "fact": "Mars is known as the Red Planet.",
        "keywords": ["mars", "red planet"],
    },
    {
        "fact": "Jupiter is the largest planet in the Solar System.",
        "keywords": ["jupiter", "largest planet"],
    },
]


def extract_claims(answer: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", answer.strip())
    return [part.strip() for part in parts if part.strip()]


def retrieve_evidence(claim: str) -> list[dict]:
    normalized_claim = re.sub(
        r"[.!?]+$", "", claim.lower().strip()
    )

    matches = []

    for item in EVIDENCE:
        if all(
            keyword.lower() in normalized_claim
            for keyword in item["keywords"]
        ):
            matches.append(item)

    return matches


def analyze_claim(claim: str) -> dict:
    normalized = claim.lower().strip()
    normalized = re.sub(r"[.!?]+$", "", normalized)

    contradiction_pairs = [
        ("the sun is a star", ["the sun is not a star"]),
        (
            "earth revolves around the sun",
            ["earth does not revolve around the sun"],
        ),
        (
            "water has the chemical formula h2o",
            ["water has the chemical formula co2"],
        ),
    ]

    for fact, contradictions in contradiction_pairs:
        if normalized in contradictions:
            return {
                "claim": claim,
                "label": "Contradicted",
                "evidence": fact,
                "explanation": (
                    "This claim conflicts with a fact in the demo rules. "
                    "Verify it against reliable sources."
                ),
                "confidence": "Rule-based contradiction",
            }

    matches = retrieve_evidence(claim)

    for item in matches:
        fact_normalized = item["fact"].lower().rstrip(".")

        if normalized == fact_normalized:
            return {
                "claim": claim,
                "label": "Supported",
                "evidence": item["fact"],
                "explanation": (
                    "The claim exactly matches a fact "
                    "in the demo evidence base."
                ),
                "confidence": "High (exact demo fact match)",
            }

    evidence_facts = [item["fact"] for item in EVIDENCE]

    semantic_matches = find_similar_evidence(
        claim,
        evidence_facts,
        threshold=0.60,
    )

    if semantic_matches:
        best_match = semantic_matches[0]

        return {
            "claim": claim,
            "label": "Not Enough Evidence",
            "evidence": best_match["fact"],
            "explanation": (
                "Semantically similar evidence was found, "
                "but similarity alone cannot verify factual accuracy."
            ),
            "confidence": "Semantic match (not verified)",
            "similarity": best_match["similarity"],
        }

    return {
        "claim": claim,
        "label": "Not Enough Evidence",
        "evidence": None,
        "explanation": (
            "No matching evidence was found in the demo evidence base. "
            "This does not mean the claim is false."
        ),
        "confidence": "Unverified",
    }


def analyze_answer(answer: str) -> dict:
    claims = extract_claims(answer)
    results = [analyze_claim(claim) for claim in claims]

    uncertain = sum(
        result["label"] == "Not Enough Evidence"
        for result in results
    )

    risk_score = (
        round(100 * uncertain / len(results)) if results else 0
    )

    return {
        "claims": results,
        "total_claims": len(results),
        "uncertain_claims": uncertain,
        "risk_score": risk_score,
        "note": (
            "Demo score based on uncertain claims; "
            "it is not a validated hallucination probability."
        ),
    }



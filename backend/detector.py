import re

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
        keywords = item["keywords"]

        if all(
            keyword.lower() in normalized_claim
            for keyword in keywords
        ):
            matches.append(item)

    return matches


def analyze_claim(claim: str) -> dict:
    normalized = claim.lower().strip()
    normalized = re.sub(r"[.!?]+$", "", normalized)

    # Step 1: Check known contradictions first
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

    # Step 2: Retrieve evidence using keywords
    matches = retrieve_evidence(claim)

    # Step 3: Confirm an exact match before marking Supported
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

    # Step 4: Evidence found, but exact verification is unavailable
    return {
        "claim": claim,
        "label": "Not Enough Evidence",
        "evidence": matches[0]["fact"] if matches else None,
        "explanation": (
            "Matching evidence was retrieved, but the claim "
            "did not exactly match it. Further verification is needed."
            if matches
            else
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
            "Demo score based on missing exact matches; "
            "it is not a validated hallucination probability."
        ),
    }
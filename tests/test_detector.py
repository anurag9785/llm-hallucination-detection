from backend.detector import analyze_claim, analyze_answer
from backend.detector import analyze_answer


def test_supported_claim():
    result = analyze_answer("Earth revolves around the Sun.")

    assert result["total_claims"] == 1
    assert result["claims"][0]["label"] == "Supported"


def test_contradicted_claim():
    result = analyze_answer("The Sun is not a star.")

    assert result["claims"][0]["label"] == "Contradicted"


def test_unknown_claim():
    result = analyze_answer("Jupiter has 100 moons.")

    assert result["claims"][0]["label"] == "Not Enough Evidence"


def test_lowercase_supported_claim():
    result = analyze_answer("the sun is a star")

    assert result["claims"][0]["label"] == "Supported"


def test_multiple_claims():
    answer = (
        "Earth revolves around the Sun. "
        "The Sun is not a star. "
        "Jupiter has 100 moons."
    )

    result = analyze_answer(answer)

    assert result["total_claims"] == 3
    assert result["claims"][0]["label"] == "Supported"
    assert result["claims"][1]["label"] == "Contradicted"
    assert result["claims"][2]["label"] == "Not Enough Evidence"


def test_risk_score():
    answer = (
        "Earth revolves around the Sun. "
        "Jupiter has 100 moons."
    )

    result = analyze_answer(answer)

    assert result["uncertain_claims"] == 1
    assert result["risk_score"] == 50


def test_empty_answer():
    result = analyze_answer("")

    assert result["total_claims"] == 0
    assert result["claims"] == []
    assert result["risk_score"] == 0


def test_unknown_claim_is_not_marked_false():
    result = analyze_answer("A fictional planet orbits a blue star.")

    assert result["claims"][0]["label"] == "Not Enough Evidence"
    assert result["claims"][0]["evidence"] is None
def test_semantic_match_is_not_marked_supported():
    result = analyze_claim(
        "The Earth moves around our Sun."
    )

    assert result["label"] == "Not Enough Evidence"
    assert result["similarity"] > 0
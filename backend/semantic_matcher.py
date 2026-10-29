
from sentence_transformers import SentenceTransformer, util

# Model will load only when needed
_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return _model


def find_similar_evidence(
    claim: str,
    evidence_facts: list[str],
    threshold: float = 0.60
):
    if not claim.strip() or not evidence_facts:
        return []

    model = get_model()

    embeddings = model.encode(
        [claim] + evidence_facts,
        convert_to_tensor=True
    )

    scores = util.cos_sim(
        embeddings[0],
        embeddings[1:]
    )[0]

    matches = []

    for fact, score in zip(evidence_facts, scores):
        similarity = float(score)

        if similarity >= threshold:
            matches.append({
                "fact": fact,
                "similarity": round(similarity, 3)
            })

    matches.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return matches

"""DRVGA-inspired demonstration layer.

This is a transparent heuristic, not a trained reinforcement-learning agent.
Do not describe it as experimentally validated DRVGA.
"""

def assess_credibility(text: str, nlp_result: dict) -> dict:
    normalized = text.lower()
    # Lightweight indicators only; these are not proof of misinformation.
    sensational_phrases = [
        "share now", "forward immediately", "government is hiding",
        "miracle cure", "guarantees instant", "click this link",
        "no evidence", "secret report",
    ]
    indicator_hits = [phrase for phrase in sensational_phrases if phrase in normalized]
    language_signal = max(0.0, 1.0 - min(len(indicator_hits) * 0.12, 0.6))

    model_authentic = nlp_result["authentic_probability"]
    # Simple weighted score for demonstration purposes.
    score = 100.0 * (0.85 * model_authentic + 0.15 * language_signal)
    score = round(max(0.0, min(score, 100.0)), 2)

    explanation = []
    explanation.append(
        f"NLP model authentic probability: {model_authentic:.1%}."
    )
    if indicator_hits:
        explanation.append(
            "Potentially sensational wording detected: " + ", ".join(indicator_hits) + "."
        )
    else:
        explanation.append("No configured sensational-phrase indicator was triggered.")
    explanation.append(
        "These indicators are only signals; verify important claims with reliable sources."
    )

    return {
        "credibility_score": score,
        "language_indicator_hits": indicator_hits,
        "explanation": " ".join(explanation),
    }

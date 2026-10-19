
"""Tier 3: combine Tier 1 and Tier 2 risk scores into a trust score."""

import math


TIER1_WEIGHT = 0.60
TIER2_WEIGHT = 0.40


def calculate_trust_score(tier1_risk: float, tier2_risk: float) -> float:
    """Return an estimated trust score between 0.0 and 1.0.

    Both inputs must be normalized risk scores:
        0.0 = no detected risk
        1.0 = maximum detected risk

    Higher trust scores indicate lower estimated hallucination risk.
    """
    risks = {
        "tier1_risk": tier1_risk,
        "tier2_risk": tier2_risk,
    }

    for name, value in risks.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number.")

        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite.")

        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0.0 and 1.0.")

    combined_risk = (
        TIER1_WEIGHT * tier1_risk
        + TIER2_WEIGHT * tier2_risk
    )

    trust_score = 1.0 - combined_risk

    # Keep the result within the documented range.
    return round(trust_score, 6)

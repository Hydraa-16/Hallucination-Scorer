
# Tier 3: Trust Score Calculation

## 1. Purpose

Tier 3 combines the risk estimates from Tier 1 (claim-grounding analysis) and Tier 2 (semantic disagreement analysis) into a single trust score.

The score is an estimate of answer reliability, not a calibrated probability that the answer is correct.

## 2. Input Definitions

- `tier1_risk`: Normalized claim-grounding risk from Tier 1.
- `tier2_risk`: Normalized semantic-disagreement risk from Tier 2.

Both inputs must be finite numeric values in the range [0.0, 1.0].

A value of 0.0 represents no detected risk, while 1.0 represents maximum detected risk.

## 3. Weights

- Tier 1 weight: 0.60
- Tier 2 weight: 0.40

Tier 1 receives the larger initial weight because it directly evaluates claims against retrieved evidence. Tier 2 provides complementary evidence by measuring disagreement across sampled answers.

These weights are provisional baseline choices and have not been empirically calibrated.

## 4. Formula

Combined risk:

R = (0.60 × tier1_risk) + (0.40 × tier2_risk)

Trust score:

trust_score = 1.0 - R

The resulting trust score lies in [0.0, 1.0]. Higher values indicate lower estimated hallucination risk.

## 5. Validation

The implementation rejects:
- Values outside [0.0, 1.0].
- Non-finite values, including NaN and infinity.
- Non-numeric values and booleans.

Missing tier outputs must be handled explicitly by the integration layer rather than silently replaced with zero.

## 6. Example

Given:
- tier1_risk = 0.50
- tier2_risk = 0.25

Combined risk = (0.60 × 0.50) + (0.40 × 0.25) = 0.40

Trust score = 1.0 - 0.40 = 0.60

## 7. Limitations

- The weights are initial design assumptions, not empirically validated parameters.
- Tier 1 and Tier 2 can make errors.
- Semantic disagreement does not necessarily indicate hallucination.
- Retrieval quality affects claim-grounding assessments.
- The score must not be interpreted as ground truth or a calibrated probability of correctness.

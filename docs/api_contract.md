
# Hallucination Scoring Middleware — API Contract

## 1. Purpose

This document defines the interface between the reference chat application and the hallucination-scoring middleware.

The middleware receives the user's query, retrieved evidence, and generated answer from the host application. It does not perform retrieval or generate the answer itself.

## 2. Request

The host application sends a JSON object containing the following fields.

| Field | Type | Description |
|---|---|---|
| `query` | string | The user's original question |
| `retrieved_chunks` | array of strings | Evidence chunks retrieved from the fixed project corpus |
| `generated_answer` | string | The answer produced by the host application's RAG pipeline |

Example:

```json
{
  "query": "What event marked the beginning of World War I?",
  "retrieved_chunks": [
    "The assassination of Archduke Franz Ferdinand in June 1914 triggered the July Crisis."
  ],
  "generated_answer": "World War I began in 1914 following the assassination of Archduke Franz Ferdinand."
}
```

The example is illustrative; the retrieved chunks supplied at runtime must come from the actual retrieval pipeline.

## 3. Response

The middleware returns a JSON object containing the trust score and claims flagged for review.

| Field | Type | Description |
|---|---|---|
| `trust_score` | number | Estimated trust score in the range [0.0, 1.0], where higher values indicate lower estimated hallucination risk |
| `flagged_claims` | array | Claims identified for further review by the scoring pipeline |

Example:

```json
{
  "trust_score": 0.82,
  "flagged_claims": [
    "An example claim requiring verification."
  ]
}
```

The example score is illustrative and is not a measured result.

## 4. Scoring Semantics

Tier 3 combines the normalized risk estimates from Tier 1 and Tier 2:

R = (0.60 × tier1_risk) + (0.40 × tier2_risk)

trust_score = 1.0 - R

Both tier risk values must be finite numbers in [0.0, 1.0]. The weights are provisional baseline choices and may be revised after evaluation.

The trust score is an estimate, not a calibrated probability that the answer is correct.

## 5. Validation and Errors

The backend implementation should reject malformed requests, missing required fields, incorrect field types, and invalid values.

The implementation team must agree on exact HTTP status codes and error-response structure before integration. Invalid or unavailable tier results must not silently be treated as zero risk.

## 6. Scope and Constraints

- The middleware is called explicitly by the host application.
- The request includes `query`, `retrieved_chunks`, and `generated_answer`.
- The reference application uses the project's fixed, pre-ingested corpus.
- Models must run locally using free, open-weight resources.
- The trust score is a risk indicator and must not be presented as ground truth.

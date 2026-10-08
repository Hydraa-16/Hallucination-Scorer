# Hallucination Scoring Project

**MIC AIML Build Cycle · Team 5 · VIT Chennai**

A hallucination-risk scoring middleware with a reference chat
application. The middleware evaluates generated answers against
retrieved content and returns a trust score together with claims that
are not supported by the retrieved content.

## Project Overview

RAG systems can still produce hallucinated or unsupported information
even when retrieval is used. This project builds a reusable
middleware/SDK that receives:

``` text
{query, retrieved\\\_chunks, generated\\\_answer}
```

and returns:

``` text
{trust\\\_score, flagged\\\_claims}
```

The middleware is the core technical deliverable. A reference chat
application demonstrates the complete system end to end.

The reference application is deliberately grounded on a pre-ingested
corpus of curated Wikipedia articles covering Indian history and the
World Wars. It is not an open-domain assistant.

## System Architecture

The system follows this flow:

``` text
Pre-ingested Wikipedia Corpus
            ↓
       RAG Retrieval
            ↓
        LLM Answer
            ↓
    Scoring Middleware
            ↓
     ┌──────┴──────┐
     ↓             ↓
  Tier 1          Tier 2
    NLI       Semantic Entropy
     └──────┬──────┘
            ↓
         Tier 3
   Weighted Combination
            ↓
       Trust Score
            +
      Flagged Claims
            ↓
         Chat UI
```

The scoring middleware is implemented using Python and FastAPI.

## Core Components

### Tier 1 --- Claim Decomposition + NLI

Tier 1:

1. Uses a local open-weight LLM through Ollama to split a generated
answer into atomic claims.
2. Checks each claim against retrieved chunks using DeBERTa-v3-MNLI.
3. Returns supported/unsupported claims together with NLI scores.

Claim decomposition is a known imperfect step, particularly for compound
sentences, implicit references, and numeric claims.

### Tier 2 --- Semantic Entropy

Tier 2:

1. Generates multiple answers for the same query using a local
open-weight LLM.
2. Creates embeddings using sentence-transformers.
3. Clusters semantically similar answers.
4. Calculates an entropy/disagreement signal.

The baseline uses a reduced sample count to control runtime.

### Tier 3 --- Trust Score

The baseline Tier 3 combines the Tier 1 and Tier 2 outputs using a
weighted-average rule.

Full isotonic/Platt calibration is deferred as stretch work.

The resulting trust score is a risk/trust estimate and must not be
treated as ground truth.

## Reference Chat Application

The project includes a chat-style reference application over a
pre-ingested Wikipedia corpus.

The corpus consists of approximately 15--25 curated articles at the
intersection of Indian history and the World Wars.

Corpus setup:

``` text
Wikipedia API
     ↓
Clean / strip markup
     ↓
Chunk
     ↓
Embed
     ↓
FAISS / Chroma vector index
```

During a chat:

``` text
User message
     ↓
Retriever
     ↓
Retrieved chunks
     ↓
Local LLM
     ↓
Generated answer
     ↓
Scoring Middleware
```

The chat UI displays the answer together with its trust score and
flagged unsupported claims.

No user document upload is required by the baseline application.

## Demo RAG Pipeline

The project contains exactly one team-owned demo RAG pipeline.

The pipeline produces:

``` text
query
retrieved\\\_chunks
generated\\\_answer
```

and sends these to the scoring middleware.

External RAG integration remains outside the project scope.

## API Contract

### Request

``` json
{
  "query": "string",
  "retrieved\\\_chunks": \\\[
    "string"
  ],
  "generated\\\_answer": "string"
}
```

### Response

``` json
{
  "trust\\\_score": 0.0,
  "flagged\\\_claims": \\\[]
}
```

The exact request/response schema is maintained as part of the API
contract documentation.

## Technology Stack

Layer                  Technology / Component

\---

Core scoring service   Python + FastAPI
NLI                    HuggingFace Transformers + DeBERTa-v3-MNLI
Claim decomposition    Local open-weight LLM via Ollama
Semantic entropy       Local open-weight LLM + sentence-transformers
Trust score            Weighted-average combination
Corpus                 Wikipedia API
Vector store           FAISS or Chroma
Demo RAG               LangChain or LlamaIndex + local components
Evaluation             Python + HaluEval + scikit-learn
Chat UI                Streamlit or lightweight React
Deployment             Docker Compose locally / free-tier host if applicable

All models are intended to run locally using free/open-weight resources.

## Repository Structure

``` text
hallucination-scoring-middleware/
│
├── middleware/
│   ├── tier1/
│   ├── tier2/
│   └── tier3/
│
├── rag/
│   ├── ingestion/
│   └── retrieval/
│
├── chat\\\_app/
│
├── evaluation/
│
├── tests/
│
├── docs/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Team Ownership

### Shaikh Adnan Ahmad

**Architecture, API Contract \& Tier 3**

* Define the overall scoring methodology and system architecture.
* Define and maintain the API contract.
* Choose the NLI model and semantic-entropy methodology.
* Own the Tier 3 baseline weighted-combination trust score.
* Lead stretch calibration work if time allows.
* Review ML/NLP implementations and AI-generated code.
* Maintain the technical roadmap and make final technical decisions.

### Siddharth Jain

**Backend, Integration \& Demo Infrastructure**

* Build the FastAPI project skeleton and scoring endpoint.
* Define interfaces between Tier 1, Tier 2, Tier 3, the RAG pipeline,
and chat UI.
* Set up local model loading and configuration.
* Provide backend/infra support for the chat application.
* Integrate completed modules and resolve integration blockers.
* Run final end-to-end systems ahead of reviews.

### Joel Vinu Koshy + Ansh Kumar Singh

**Tier 1 --- Claim Decomposition + NLI**

* Learn atomic claim decomposition and NLI basics.
* Set up the local open-weight LLM through Ollama.
* Build the claim-splitting module.
* Run DeBERTa-v3-MNLI locally for entailment checking.
* Return supported/unsupported claims with NLI scores.
* Create supported, unsupported, partially supported, and
irrelevant-context test cases.

### Krish Kanyal + Kummetha Chenna Pranav Reddy

**Tier 2 --- Semantic Entropy**

* Read and understand the selected semantic-entropy paper together.
* Set up a local open-weight LLM for repeated sampling.
* Generate multiple answers using the reduced sample count.
* Create sentence-transformers embeddings and cluster semantically
similar answers.
* Calculate the entropy/disagreement signal.
* Test consistent versus inconsistent answers.

### Riona Lisanne Jefrin + Shridula V

**Demo Application --- RAG Pipeline, Corpus \& Chat UI**

* Source approximately 15--25 curated Wikipedia articles at the
intersection of Indian history and the World Wars.
* Build the Wikipedia API ingestion script.
* Clean markup, references and infoboxes.
* Chunk and build a FAISS or Chroma vector index.
* Build the demo RAG pipeline.
* Output query, retrieved chunks and generated answer in the
middleware format.
* Build the Streamlit chat UI with multi-turn conversation, trust
score and flagged-claim display.
* Handle basic no-retrieval and empty-response failure modes without
crashing the demo.

Dataset curation for evaluation, documentation, and bug tracking are
shared responsibilities across the team and are coordinated by the
Project Heads.

## Development Workflow

The `main` branch contains the integrated project.

Development should take place on feature branches:

``` text
main
 ├── feature/tier1
 ├── feature/tier2
 ├── feature/tier3
 ├── feature/backend
 └── feature/demo-app
```

Changes should be pushed to the relevant feature branch and merged into
`main` through a pull request after review.

## Development Setup

### Requirements

* Python
* Git
* Ollama
* A locally runnable open-weight LLM
* Dependencies listed in `requirements.txt`

### Environment

Copy `.env.example` to `.env` and adjust local configuration if
required.

The `.env` file must not be committed.

### Install dependencies

``` bash
pip install -r requirements.txt
```

Further setup instructions will be added as the individual modules are
implemented.

## Build Cycle

### Phase 1 --- Foundation \& Proof of Concept

**6 October -- 30 October 2026**

Focus:

* Finalize scope and architecture.
* Set up repositories and environments.
* Source and begin the corpus pipeline.
* Start individual modules.
* Deliver a working prototype / vertical slice.

### Phase 2 --- Core System Build

**4 November -- 19 December 2026**

Focus:

* Implement core modules.
* Integrate components.
* Get real data flowing through the system.
* Initial evaluation and testing.
* Deliver a working MVP.

### Phase 3 --- Integration \& Hardening

**25 December 2026 -- 24 January 2027**

Focus:

* Improve performance and handling.
* Add more datasets/scenarios.
* Evaluation, benchmarking and testing.
* UI/UX and documentation.
* Prepare the final demo.

### Phase 4 --- Finalization

**25 January -- 30 January 2027**

Focus:

* Bug fixes and final testing.
* Documentation and deployment.
* Demo preparation and rehearsal.
* Final report and presentation.
* Feature freeze.

## Review 1 Target

**Review 1: 31 October -- 3 November 2026**

The target is proof that the individual components are real and working,
rather than a completed end-to-end system.

Team 5 must show:

* Finalized API contract.
* FastAPI skeleton running.
* Tier 1 prototype working on toy examples.
* Wikipedia corpus sourced.
* Ingestion underway.
* At least one manual/hardcoded query returning real retrieved chunks.

The Review 1 baseline is a single query that can be manually traced
through corpus retrieval and a real Tier 1 entailment check using the
shared API contract.

## Evaluation

The baseline evaluation uses HaluEval and reports an AUROC score
together with a simplified calibration check.

TruthfulQA and full isotonic/Platt calibration are stretch additions if
time allows.

## Known Limitations

The system is a hallucination-risk scoring layer, not a guarantee of
factual correctness.

Known limitations include:

* Claim decomposition can fail on complex or implicit statements.
* NLI models are imperfect and can disagree with other evaluators.
* Semantic entropy requires multiple LLM samples and therefore adds
latency.
* Retrieval quality directly affects scoring accuracy.
* The Tier 3 weighted-average score is a baseline rather than a fully
calibrated probability.
* The trust score must not be interpreted as ground truth.

## Scope Boundary

The project is a hallucination-risk layer with a reference chat
application.

The baseline does not include:

* General-purpose open-domain chat.
* External RAG integrations.
* Required user document uploads.
* Full isotonic/Platt calibration.
* TruthfulQA as a required evaluation dataset.
* Multiple demo RAG pipelines.

Stretch items may only be included where explicitly designated in the
project specification.

## Project Team

**MIC AIML Build Cycle --- Team 5**  
**VIT Chennai**

* Shaikh Adnan Ahmad
* Siddharth Jain
* Joel Vinu Koshy
* Ansh Kumar Singh
* Krish Kanyal
* Kummetha Chenna Pranav Reddy
* Riona Lisanne Jefrin
* Shridula V




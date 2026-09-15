# Course Guide

This course teaches RAG through one fictional high-security finance scenario:
an internal assistant for Northline Trust Company.

The notebooks are intentionally small. Each one proves one production concern,
then the next notebook adds another layer.

## What You Build

```text
staff question + role
    -> parse mixed internal files
    -> chunk with metadata
    -> embed locally
    -> search with vectors + BM25
    -> rerank current policy above stale policy
    -> filter by role and classification
    -> redact synthetic PII
    -> ask an OpenAI-compatible LLM for cited JSON
    -> abstain when citations or access are missing
```

## Learning Path

1. `01-what-is-rag.ipynb`: What RAG is and why private policy breaks plain LLM Q&A.
2. `02-grounding.ipynb`: Manual RAG by pasting one policy into the prompt.
3. `03-embeddings.ipynb`: Semantic similarity for paraphrases.
4. `04-chunking.ipynb`: Chunks plus metadata.
5. `05-mixed-sources.ipynb`: Ingest markdown, PDF, CSV, TSX, HTML, JSON, YAML.
6. `06-hybrid-search.ipynb`: Combine dense retrieval and BM25 for IDs and codes.
7. `07-stale-documents.ipynb`: Prefer current controls over superseded policy.
8. `08-access-control.ipynb`: Filter Restricted and MNPI before generation.
9. `09-pii-and-injection.ipynb`: Redact synthetic PII and ignore hostile documents.
10. `10-end-to-end.ipynb`: Run real desk questions through the full pipeline.

## Why These Scenarios Matter

- Policy answers must be grounded in current internal evidence.
- Exact identifiers (`SEV-1`, `WB-8841`) need lexical search, not vectors alone.
- Access control belongs in retrieval, not in a hopeful instruction to the model.
- Prompt-injection text inside documents must be treated as data.
- PII must be removed before the model call.
- Citations should be checked against retrieved chunks so the answer can abstain.

## Model Choice

The tutorial uses xAI by default:

```text
XAI_API_KEY=...
XAI_BASE_URL=https://api.x.ai/v1
XAI_MODEL=grok-4.6
```

Any OpenAI-compatible chat model can be used instead:

```text
LLM_API_KEY=...
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

Embeddings run locally with FastEmbed.

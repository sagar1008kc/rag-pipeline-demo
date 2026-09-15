# RAG Pipeline Tutorials A-Z

Notebook course for building a production-style RAG pipeline over fictional
internal finance knowledge: policy, PII, MNPI walls, stale documents, prompt
injection, and role-based access control. The running scenario uses a
fictional private bank named Northline Trust Company.

There is no UI or web service. The whole course runs in Jupyter.

All names, accounts, phone numbers, vendors, issuers, and watch-book entries in
`data/` are synthetic.

## What You Learn

- What RAG is and why plain LLM Q&A fails on private knowledge.
- How to ingest mixed internal sources: markdown, PDF, CSV, TSX, HTML, JSON,
  and YAML.
- How dense embeddings and BM25 solve different retrieval problems.
- Why high-security RAG needs ACL filtering before generation.
- How to redact PII before the LLM call.
- How to prefer current policy over superseded documents.
- How to verify citations and abstain when evidence is missing.

## Pipeline

```
question + role
    → hybrid retrieve (vectors + BM25)
    → ACL (drop what the role cannot see)
    → redact PII
    → generate from evidence only
    → keep real citations, else abstain
```

## Course

| # | File | Scenario |
| - | ---- | -------- |
| 1 | [01-what-is-rag.ipynb](notebooks/01-what-is-rag.ipynb) | What RAG is; LLM fails without your files |
| 2 | [02-grounding.ipynb](notebooks/02-grounding.ipynb) | Same question with the file in the prompt |
| 3 | [03-embeddings.ipynb](notebooks/03-embeddings.ipynb) | Meaning vs keywords |
| 4 | [04-chunking.ipynb](notebooks/04-chunking.ipynb) | Split files; keep metadata |
| 5 | [05-mixed-sources.ipynb](notebooks/05-mixed-sources.ipynb) | md, pdf, csv, tsx, html, json, yaml |
| 6 | [06-hybrid-search.ipynb](notebooks/06-hybrid-search.ipynb) | IDs need BM25; paraphrases need vectors |
| 7 | [07-stale-documents.ipynb](notebooks/07-stale-documents.ipynb) | Superseded policy must lose |
| 8 | [08-access-control.ipynb](notebooks/08-access-control.ipynb) | Restricted vs MNPI by role |
| 9 | [09-pii-and-injection.ipynb](notebooks/09-pii-and-injection.ipynb) | Redact identifiers; ignore hostile docs |
| 10 | [10-end-to-end.ipynb](notebooks/10-end-to-end.ipynb) | Desk questions through the full loop |

Read [COURSE.md](COURSE.md) for the learning path and architecture.

## Setup

Python 3.11+ is recommended. Embeddings run locally. Generation needs an LLM key.

This tutorial uses **xAI Grok**:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # paste XAI_API_KEY
jupyter lab notebooks/01-what-is-rag.ipynb
```

Any other OpenAI-compatible model works. In `.env`:

```
LLM_API_KEY=...
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

If `LLM_*` is unset, the code reads `XAI_API_KEY` / `XAI_BASE_URL` / `XAI_MODEL`.

Corpus details: [data/README.md](data/README.md). More setup notes:
[SETUP.md](SETUP.md). Security notes: [SECURITY.md](SECURITY.md).

## Repository Contents

```text
data/       synthetic mixed-format knowledge corpus
lib/        ingest, retrieval, security, and LLM helpers
notebooks/ 10 runnable lessons
scripts/   notebook and PDF generators
```

## License

MIT. Demo content is fictional and is not legal, compliance, or security advice.

# Setup

Python 3.11+ is recommended.

Embeddings run locally. Generation cells need an LLM key. This tutorial uses
xAI (`XAI_API_KEY` from https://console.x.ai), but any OpenAI-compatible
provider works via `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
jupyter lab notebooks/01-what-is-rag.ipynb
```

Run notebooks **01 → 10** in order (Shift+Enter).

Embeddings use local FastEmbed, so notebooks 03–08 work without a key.
Generation cells print a skip message if no key is set.

## Kernel

In Cursor or Jupyter, choose the `.venv` Python kernel for the notebook. If a
cell cannot import `_course` or `lib.pipeline`, restart the kernel and run from
the first cell.

## LLM Configuration

Default xAI settings:

```text
XAI_API_KEY=xai-...
XAI_BASE_URL=https://api.x.ai/v1
XAI_MODEL=grok-4.6
```

Provider-neutral settings override `XAI_*`:

```text
LLM_API_KEY=...
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

If you see `Incorrect API key provided`, create a new key, update `.env`,
restart the kernel, and run the notebook again.

Rebuild the two runbook PDFs (optional; they are already in `data/runbooks/`):

```bash
python scripts/generate_pdfs.py
```

Regenerate clean notebooks from source:

```bash
python scripts/write_notebooks.py
```

"""Shared bootstrap for Northline RAG notebooks."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.llm import complete, has_llm, model_name

HAS_LLM = has_llm()
MODEL = model_name()


def skip_if_no_key(action: str) -> bool:
    if HAS_LLM:
        return False
    print(f"No LLM key — skipping {action}. Set XAI_API_KEY (this tutorial) or LLM_API_KEY.")
    return True


def llm(user: str, system: str | None = None, temperature: float = 0.0) -> str:
    return complete(user, system=system, temperature=temperature)


print("course: RAG Tutorials A-Z")
print("llm   :", HAS_LLM, "| model:", MODEL)

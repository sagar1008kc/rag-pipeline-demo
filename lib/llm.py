"""OpenAI-compatible chat client.

This tutorial uses xAI (XAI_API_KEY + https://api.x.ai/v1). Any other
OpenAI-compatible host works: set LLM_API_KEY, LLM_BASE_URL, LLM_MODEL.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

from lib.paths import ROOT

load_dotenv(ROOT / ".env", override=False)


def _first(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return default


def api_key() -> str:
    return _first("LLM_API_KEY", "XAI_API_KEY", "OPENAI_API_KEY")


def base_url() -> str:
    explicit = _first("LLM_BASE_URL", "XAI_BASE_URL", "OPENAI_BASE_URL")
    if explicit:
        return explicit
    if os.getenv("OPENAI_API_KEY") and not os.getenv("XAI_API_KEY"):
        return "https://api.openai.com/v1"
    return "https://api.x.ai/v1"


def model_name() -> str:
    explicit = _first("LLM_MODEL", "XAI_MODEL", "OPENAI_MODEL")
    if explicit:
        return explicit
    if "openai.com" in base_url():
        return "gpt-4o-mini"
    return "grok-4.6"


def has_llm() -> bool:
    key = api_key()
    return bool(key) and "your-key-here" not in key.lower()


def _is_bad_key(exc: BaseException) -> bool:
    text = str(exc).lower()
    return any(
        token in text
        for token in (
            "incorrect api key",
            "invalid api key",
            "invalid_api_key",
            "unauthorized",
            "authentication",
        )
    )


def _key_error(exc: BaseException) -> RuntimeError:
    host = base_url()
    return RuntimeError(
        f"LLM rejected the API key ({host}). For this tutorial put a valid "
        "XAI_API_KEY in .env from https://console.x.ai — then Restart Kernel "
        "and Run All. To use another provider, set LLM_API_KEY, LLM_BASE_URL, "
        f"and LLM_MODEL. Original error: {exc}"
    )


_client = None


def client():
    from openai import OpenAI

    global _client
    if _client is None:
        if not has_llm():
            raise RuntimeError(
                "Set XAI_API_KEY in .env for this tutorial, or LLM_API_KEY + "
                "LLM_BASE_URL + LLM_MODEL for any OpenAI-compatible provider."
            )
        _client = OpenAI(api_key=api_key(), base_url=base_url())
    return _client


def complete(user: str, system: str | None = None, temperature: float = 0.0) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    try:
        response = client().responses.create(
            model=model_name(), input=messages, temperature=temperature, store=False
        )
        text = getattr(response, "output_text", None)
        if text:
            return text
    except Exception as exc:
        if _is_bad_key(exc):
            raise _key_error(exc) from exc
    try:
        response = client().chat.completions.create(
            model=model_name(), messages=messages, temperature=temperature
        )
    except Exception as exc:
        if _is_bad_key(exc):
            raise _key_error(exc) from exc
        raise
    return response.choices[0].message.content or ""

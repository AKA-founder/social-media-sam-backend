from __future__ import annotations
from typing import Any
import os

class _NotConfigured:
    """Raises a helpful error if LLM is used without config."""
    def __init__(self, reason: str) -> None:
        self.reason = reason
    def __getattr__(self, name: str) -> Any:  # only raised if called
        raise RuntimeError(f"OpenAI LLM is not configured: {self.reason}")

def get_llm(*_: Any, **__: Any):
    """Return an OpenAI client or a guarded stub."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return _NotConfigured("Missing OPENAI_API_KEY env var")
    try:
        from openai import OpenAI  # SDK v1.x
        return OpenAI(api_key=api_key)
    except Exception as exc:
        return _NotConfigured(str(exc))


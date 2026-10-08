from __future__ import annotations
import json, os
from pathlib import Path
from typing import Any

class LLMUnavailable(RuntimeError): pass

class LLMProvider:
    name="base"
    def complete_json(self, task: str, system: str, payload: dict) -> dict:
        raise NotImplementedError
    def available(self) -> bool: return False

def load_provider(project_root: str|Path, config: dict|None=None) -> LLMProvider:
    """Factory. Falls back to Mock only when the real provider is not configured;
    the engine records provider_used so tests/users can see which path ran."""
    root=Path(project_root)
    cfg={}
    p=root/"config/model.json"
    if p.exists():
        try: cfg=json.loads(p.read_text(encoding="utf-8"))
        except Exception: cfg={}
    if config: cfg={**cfg, **config}
    provider_name=os.environ.get("LOVE_AGENT_LLM_PROVIDER") or cfg.get("provider","mock")
    if provider_name=="openai_compatible":
        from .openai_compatible import OpenAICompatibleProvider
        prov=OpenAICompatibleProvider(
            base_url=os.environ.get("LOVE_AGENT_BASE_URL") or cfg.get("base_url",""),
            model=os.environ.get("LOVE_AGENT_MODEL") or cfg.get("model",""),
            api_key_env=cfg.get("api_key_env","LOVE_AGENT_API_KEY"),
            temperature=float(cfg.get("temperature",0.3)))
        if prov.available(): return prov
        from .mock import MockLLMProvider
        m=MockLLMProvider(); m.fallback_reason="openai_compatible selected but base_url/model/api_key env incomplete; using mock"
        return m
    from .mock import MockLLMProvider
    return MockLLMProvider()

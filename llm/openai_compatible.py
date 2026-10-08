from __future__ import annotations
import json, os, urllib.request, urllib.error
from .provider import LLMProvider, LLMUnavailable

class OpenAICompatibleProvider(LLMProvider):
    """Real OpenAI-compatible chat/completions provider (DeepSeek/OpenAI/etc).
    Reads the key from the environment variable named in config; never stores it."""
    name="openai_compatible"
    def __init__(self, base_url: str, model: str, api_key_env: str="LOVE_AGENT_API_KEY", temperature: float=0.3, timeout: float=60):
        self.base_url=(base_url or "").rstrip("/"); self.model=model or ""; self.api_key_env=api_key_env; self.temperature=temperature; self.timeout=timeout
        self.calls=[]
    def available(self) -> bool:
        return bool(self.base_url and self.model and os.environ.get(self.api_key_env))
    def complete_json(self, task: str, system: str, payload: dict) -> dict:
        if not self.available():
            raise LLMUnavailable(f"real LLM not configured: need base_url, model and env {self.api_key_env}")
        body={"model":self.model,"temperature":self.temperature,
              "messages":[{"role":"system","content":system},{"role":"user","content":json.dumps({"task":task,"payload":payload},ensure_ascii=False)}],
              "response_format":{"type":"json_object"}}
        req=urllib.request.Request(self.base_url+"/chat/completions", data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type":"application/json","Authorization":"Bearer "+os.environ[self.api_key_env]})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r: data=json.loads(r.read().decode("utf-8"))
        except Exception as e:
            raise LLMUnavailable(f"LLM request failed: {e}") from e
        self.calls.append({"task":task,"system":system[:200]})
        try: content=data["choices"][0]["message"]["content"]
        except Exception as e: raise LLMUnavailable(f"unexpected LLM response shape: {e}") from e
        try: return json.loads(content)
        except Exception as e: raise LLMUnavailable(f"LLM did not return strict JSON for task {task}: {e}") from e

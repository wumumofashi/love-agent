from __future__ import annotations
import json
from pathlib import Path

class PhraseBank:
    """Tier C common-phrase bank. A hit means the reply text does not need an
    LLM generation call; the bank candidates still go through simulate+critic.
    Scoring = entry base + stage match + trigger match (exact beats substring).
    Only entries whose intent matches the strategist's reply_intent qualify."""
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.entries: list[dict] = []
        if self.path.exists():
            try:
                self.entries = json.loads(self.path.read_text(encoding="utf-8")).get("entries", [])
            except Exception:
                self.entries = []
    def match(self, intent: str, stage: str, content: str, limit: int = 3) -> list[dict]:
        hits = []
        for e in self.entries:
            if e.get("intent") != intent:
                continue
            score = float(e.get("base", 0.55))
            stages = e.get("stages") or []
            score += 0.12 if (stages and stage in stages) else 0.06
            trig = 0.0
            for t in e.get("triggers", []):
                if content == t:
                    trig = max(trig, 0.25)
                elif t and t in content:
                    trig = max(trig, 0.15)
            if trig == 0.0:
                continue  # an intent label alone is not a phrase-bank hit
            score = round(min(0.95, score + trig), 3)
            exact_hit = any(content == t for t in e.get("triggers", []))
            hits.append({"id": e.get("id", ""), "label": "常用语句库", "text": e["text"],
                         "intent": intent, "source": "phrase_bank", "bank_score": score, "exact": exact_hit})
        hits.sort(key=lambda h: (h["bank_score"], h.get("exact", False)), reverse=True)
        return hits[:limit]

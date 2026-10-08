from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

class PersonMemoryStore:
    """Per-person long-term memory. Tier D data, highest priority, never overwrite facts with guesses."""
    FILES=["profile.json","preferences.json","relationship.json","important_events.json","conversation_summary.json"]
    def __init__(self, root: str|Path):
        self.root=Path(root)
    def person_dir(self, person_id: str) -> Path:
        return self.root/"people"/person_id
    def ensure(self, person_id: str, seed: dict|None=None):
        d=self.person_dir(person_id); d.mkdir(parents=True, exist_ok=True)
        defaults={
            "profile.json":{"person_id":person_id,"name":"","basic_info":{},"personality":[],"values":[],"work":"","family":""},
            "preferences.json":{"likes":[],"dislikes":[],"chat_style":"","triggers":[],"effective_replies":[],"negative_replies":[]},
            "relationship.json":{"stage":"认识","stage_confidence":0.3,"dynamics":{},"commitments":[],"boundaries":[]},
            "important_events.json":{"events":[]},
            "conversation_summary.json":{"summary":"","recent_topics":[],"last_updated":""},
        }
        if seed:
            defaults["profile.json"].update(seed.get("profile",{}))
            defaults["relationship.json"].update(seed.get("relationship",{}))
            defaults["preferences.json"].update(seed.get("preferences",{}))
        for name, data in defaults.items():
            p=d/name
            if not p.exists(): p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    def load(self, person_id: str) -> dict:
        self.ensure(person_id)
        out={}
        for name in self.FILES:
            try: out[name[:-5]]=json.loads((self.person_dir(person_id)/name).read_text(encoding="utf-8"))
            except Exception: out[name[:-5]]={}
        return out
    def record_turn(self, person_id: str, incoming: str, final_reply: str, observed_facts: list[str]):
        self.ensure(person_id)
        d=self.person_dir(person_id)
        # conversation summary: append bounded facts only
        p=d/"conversation_summary.json"
        data=json.loads(p.read_text(encoding="utf-8"))
        data.setdefault("recent_topics",[])
        if incoming: data["recent_topics"]=(data["recent_topics"]+[incoming[:80]])[-20:]
        data["last_updated"]=datetime.now().isoformat(timespec="seconds")
        p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
        evp=d/"important_events.json"; ev=json.loads(evp.read_text(encoding="utf-8"))
        for f in observed_facts[:3]:
            ev.setdefault("events",[]).append({"time":data["last_updated"],"fact":f,"source":"observed_message"})
        ev["events"]=ev.get("events",[])[-200:]
        evp.write_text(json.dumps(ev,ensure_ascii=False,indent=2),encoding="utf-8")
        return {"person_id":person_id,"recorded_facts":observed_facts[:3],"summary_updated":True}

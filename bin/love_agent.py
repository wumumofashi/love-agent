#!/usr/bin/env python3
"""love-agent CLI: run the unified relationship pipeline on one message.

Usage:
  love_agent.py --content "嗯" --stage 暧昧 --mode autopilot
  echo '{"content":"今天好累","relationship_stage":"暧昧","mode":"confirm"}' | love_agent.py --json -
"""
import argparse, json, sys
from pathlib import Path
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))
from love_agent.engine import LoveAgentEngine

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", default="")
    ap.add_argument("--stage", default="")
    ap.add_argument("--mode", default="suggest", choices=["suggest","confirm","autopilot"])
    ap.add_argument("--person-id", default="person_001")
    ap.add_argument("--kind", default="text")
    ap.add_argument("--json", default="", help="JSON object string, or - for stdin")
    ap.add_argument("--persona", default="", help="the customer's own persona/style, e.g. '幽默、直接、不卑不亢'")
    ap.add_argument("--import-history", default="", help="path to a chat-history .txt/.json to import into this person's memory")
    ap.add_argument("--set-stage", default="", help="set relationship stage for this person (used when there is no chat history)")
    a = ap.parse_args()
    # ---- customer onboarding commands (WeChat skill setup) ----
    person_dir = SKILL_DIR/"memory/people"/a.person_id
    if a.set_stage:
        person_dir.mkdir(parents=True, exist_ok=True)
        rel_p = person_dir/"relationship.json"
        rel = json.loads(rel_p.read_text(encoding="utf-8")) if rel_p.exists() else {}
        rel.update({"stage": a.set_stage, "stage_confidence": 0.5, "stage_source": "user_declared_no_history"})
        rel_p.write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"ok": True, "person_id": a.person_id, "stage_set": a.set_stage}, ensure_ascii=False)); return 0
    if a.import_history:
        src = Path(a.import_history); text = src.read_text(encoding="utf-8", errors="ignore")
        turns = []
        if src.suffix == ".json":
            data = json.loads(text)
            items = data if isinstance(data, list) else data.get("messages", [])
            for m in items:
                if isinstance(m, dict): turns.append(f"{m.get('speaker','?')}: {m.get('content','')}")
        else:
            for line in text.splitlines():
                line = line.strip()
                if line: turns.append(line)
        person_dir.mkdir(parents=True, exist_ok=True)
        (person_dir/"imported_history.json").write_text(json.dumps({"person_id": a.person_id, "turns": turns}, ensure_ascii=False, indent=2), encoding="utf-8")
        recent = "\n".join(turns[-30:])
        (person_dir/"conversation_summary.json").write_text(json.dumps({"recent_context_from_import": recent, "turn_count": len(turns)}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"ok": True, "person_id": a.person_id, "imported_turns": len(turns), "memory_dir": str(person_dir)}, ensure_ascii=False)); return 0
    if a.json:
        raw = json.loads(sys.stdin.read() if a.json == "-" else a.json)
    else:
        raw = {"content": a.content, "kind": a.kind, "mode": a.mode, "person_id": a.person_id}
        if a.persona: raw["user_persona"] = a.persona
        if a.stage: raw["relationship_stage"] = a.stage
    out = LoveAgentEngine(SKILL_DIR).process(raw)
    keys = ["relationship_stage","stage_confidence","observed_facts","possible_interpretations","recommended_strategy","reply_intent","final_reply","confidence","send_decision","decision_reason"]
    print(json.dumps({k: out.get(k) for k in keys}, ensure_ascii=False, indent=2))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())

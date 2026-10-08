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
    a = ap.parse_args()
    if a.json:
        raw = json.loads(sys.stdin.read() if a.json == "-" else a.json)
    else:
        raw = {"content": a.content, "kind": a.kind, "mode": a.mode, "person_id": a.person_id}
        if a.stage: raw["relationship_stage"] = a.stage
    out = LoveAgentEngine(SKILL_DIR).process(raw)
    keys = ["relationship_stage","stage_confidence","observed_facts","possible_interpretations","recommended_strategy","reply_intent","final_reply","confidence","send_decision","decision_reason"]
    print(json.dumps({k: out.get(k) for k in keys}, ensure_ascii=False, indent=2))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())

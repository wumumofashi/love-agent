#!/usr/bin/env python3
"""Install the love-agent plugin into a CowAgent checkout.

Usage:
  python install.py --cowagent D:\\CowAgent --chat "对方备注名" \
      --person-id person_001 --mode confirm --persona "幽默、直接、不卑不亢" --stage 暧昧

Copies plugin/love_agent/ into <cowagent>/plugins/love_agent/ and writes a
config.json with love_agent_home pointing at this skill's location.
"""
from __future__ import annotations
import argparse, json, shutil, sys
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cowagent", required=True, help="path to the CowAgent checkout")
    ap.add_argument("--chat", required=True, help="counterpart nickname/remark in WeChat")
    ap.add_argument("--person-id", default="person_001")
    ap.add_argument("--mode", default="confirm", choices=["suggest", "confirm", "autopilot"])
    ap.add_argument("--persona", default="")
    ap.add_argument("--stage", default="")
    ap.add_argument("--outbox", default="love_agent_outbox.jsonl")
    a = ap.parse_args()

    cow = Path(a.cowagent)
    if not (cow / "plugins").is_dir() or not (cow / "app.py").exists():
        print(f"error: {cow} does not look like a CowAgent checkout (plugins/ + app.py not found)", file=sys.stderr)
        return 2
    skill_home = Path(__file__).resolve().parents[2]
    src = skill_home / "integrations" / "cowagent" / "plugin" / "love_agent"
    dst = cow / "plugins" / "love_agent"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
    cfg = {
        "love_agent_home": str(skill_home),
        "outbox": str(cow / a.outbox),
        "chats": {a.chat: {"mode": a.mode, "person_id": a.person_id, "persona": a.persona, "stage": a.stage}},
    }
    (dst / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"installed: {dst}")
    print(f"config: chat={a.chat} person_id={a.person_id} mode={a.mode}")
    print("next: in CowAgent config.json set \"channel_type\": \"weixin\", log in, then start CowAgent.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

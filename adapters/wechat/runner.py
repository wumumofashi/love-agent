#!/usr/bin/env python3
"""love-agent WeChat runner (run this on the customer's Windows machine).

Flow per new message from the chosen chat:
  wxauto listen -> love-agent engine (10-step chain / host rules) -> decision:
  - suggest mode:   never sends; suggestion is appended to outbox for the customer
  - confirm mode:   never sends; suggestion appended to outbox, customer sends manually
  - autopilot mode: sends ONLY when engine says auto_send (confidence/risk gates pass
                    and the topic is not sensitive: breakup/money/suicide/etc.)

Safety: real sending requires --live. Without it everything is dry-run.
Messages are processed strictly one at a time (serial).

Usage (Windows, WeChat logged in):
  pip install wxauto            # WeChat 3.x  (wxauto4 for WeChat 4.x)
  python adapters/wechat/runner.py --chat "对方备注名" --person-id person_001 ^
      --mode confirm --persona "幽默、直接、不卑不亢" --outbox outbox.jsonl
  # add --live only when the customer has chosen autopilot and accepts auto-send
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from love_agent.engine import LoveAgentEngine
from adapters.wechat.wxauto_adapter import WxAutoWeChatAdapter

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chat", required=True, help="WeChat chat name/remark of the counterpart")
    ap.add_argument("--person-id", default="person_001")
    ap.add_argument("--mode", default="confirm", choices=["suggest", "confirm", "autopilot"])
    ap.add_argument("--persona", default="", help="the customer's own persona/voice")
    ap.add_argument("--stage", default="")
    ap.add_argument("--interval", type=float, default=2.0, help="listen poll seconds (wxauto listen is event-based; this is the loop tick)")
    ap.add_argument("--outbox", default="outbox.jsonl", help="suggestions/decisions log (jsonl), relative to cwd")
    ap.add_argument("--live", action="store_true", help="actually send in autopilot when the engine decision is auto_send")
    a = ap.parse_args()

    engine = LoveAgentEngine(ROOT)
    adapter = WxAutoWeChatAdapter()
    outbox = Path(a.outbox)
    seen: set[str] = set()
    print(f"[love-agent] listening to '{a.chat}' as {a.person_id}, mode={a.mode}, live={a.live}. Ctrl+C to stop.")
    while True:
        try:
            for raw in adapter.listen(a.chat):
                msg = adapter.receive(raw, contact_id=a.person_id, contact_name=a.chat)
                key = f"{msg.contact_id}|{msg.content}"
                if not msg.content or key in seen:
                    continue
                seen.add(key)
                raw_in = {"content": msg.content, "kind": msg.kind, "person_id": a.person_id,
                          "mode": a.mode, "record_memory": True}
                if a.stage: raw_in["relationship_stage"] = a.stage
                if a.persona: raw_in["user_persona"] = a.persona
                out = engine.process(raw_in)
                record = {"chat": a.chat, "person_id": a.person_id, "incoming": msg.content,
                          "final_reply": out.get("final_reply", ""), "send_decision": out.get("send_decision"),
                          "decision_reason": out.get("decision_reason", ""), "stage": out.get("relationship_stage"),
                          "confidence": out.get("confidence")}
                should = bool(out.get("should_send")) and out.get("send_decision") == "auto_send"
                if should and a.mode == "autopilot":
                    rec = adapter.send(a.chat, out["final_reply"], dry_run=not a.live)
                    record["sent"] = rec["sent"]; record["dry_run"] = rec["dry_run"]
                else:
                    record["sent"] = False
                with outbox.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                print(json.dumps(record, ensure_ascii=False))
        except KeyboardInterrupt:
            print("[love-agent] stopped."); return 0
        except Exception as e:
            print(f"[love-agent] loop error (will retry): {e}")
        time.sleep(a.interval)

if __name__ == "__main__":
    raise SystemExit(main())

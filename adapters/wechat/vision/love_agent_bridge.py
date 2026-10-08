"""love-agent bridge for the vendored vision WeChat transport.

The upstream vision bot (see NOTICE.md) calls generate_ai_reply(sender, text)
and sends the returned string. This bridge replaces that brain call with the
love-agent engine and enforces the customer modes:

  suggest / confirm -> engine runs, suggestion is written to the outbox,
                       returns None so the transport sends NOTHING.
  autopilot         -> returns final_reply only when the engine decision is
                       auto_send (confidence/risk gates passed, topic not
                       sensitive); otherwise outbox + None.
  live flag         -> even in autopilot, real sending requires loveagent.live
                       to be true in the bot config; default false (dry-run).

Config (the bot's wechat_config json, "loveagent" section):
  {
    "loveagent": {
      "live": false,
      "outbox": "love_agent_outbox.jsonl",
      "chats": {
        "对方备注名": {"person_id": "person_001", "mode": "confirm",
                       "persona": "幽默、直接、不卑不亢", "stage": "暧昧"}
      }
    }
  }
Whitelist friends without a chats entry default to mode=confirm,
person_id=person_001.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

_ENGINE = None
_ENGINE_HOME = None


def _engine(cfg: dict):
    global _ENGINE, _ENGINE_HOME
    home = cfg.get("love_agent_home") or os.environ.get("LOVE_AGENT_HOME") or str(Path(__file__).resolve().parents[3])
    if _ENGINE is None or _ENGINE_HOME != home:
        if home not in sys.path:
            sys.path.insert(0, home)
        from love_agent.engine import LoveAgentEngine
        _ENGINE = LoveAgentEngine(home)
        _ENGINE_HOME = home
    return _ENGINE


def _append_outbox(cfg: dict, record: dict) -> None:
    try:
        p = Path(cfg.get("outbox", "love_agent_outbox.jsonl"))
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


def decide_reply(sender: str, message_content: str, love_cfg: dict) -> str | None:
    """Return the exact text to send, or None to send nothing."""
    chats = love_cfg.get("chats", {}) if isinstance(love_cfg, dict) else {}
    cfg = chats.get(sender, {}) if isinstance(chats, dict) else {}
    mode = cfg.get("mode", "confirm")
    payload = {
        "content": message_content,
        "kind": "text",
        "person_id": cfg.get("person_id", "person_001"),
        "mode": mode,
        "record_memory": True,
    }
    if cfg.get("stage"):
        payload["relationship_stage"] = cfg["stage"]
    if cfg.get("persona"):
        payload["user_persona"] = cfg["persona"]
    out = _engine(love_cfg).process(payload)
    record = {
        "chat": sender,
        "person_id": payload["person_id"],
        "incoming": message_content,
        "final_reply": out.get("final_reply", ""),
        "send_decision": out.get("send_decision"),
        "decision_reason": out.get("decision_reason", ""),
        "stage": out.get("relationship_stage"),
        "confidence": out.get("confidence"),
        "mode": mode,
    }
    should = bool(out.get("should_send")) and out.get("send_decision") == "auto_send"
    live = bool(love_cfg.get("live", False))
    if mode == "autopilot" and should and record["final_reply"] and live:
        record["sent"] = True
        _append_outbox(love_cfg, record)
        return record["final_reply"]
    record["sent"] = False
    record["blocked_reason"] = (
        "mode is not autopilot" if mode != "autopilot"
        else "live flag off (dry-run)" if not live
        else f"decision={record['send_decision']}"
    )
    _append_outbox(love_cfg, record)
    return None

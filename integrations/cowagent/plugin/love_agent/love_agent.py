# encoding:utf-8
"""love-agent plugin for CowAgent (zhayujie/CowAgent, actively maintained).

Routes configured WeChat (weixin channel) chats through the love-agent engine:
  suggest/confirm -> nothing is sent to the counterpart; the suggestion is
                     written to the outbox file for the customer to read/send.
  autopilot       -> only engine decision auto_send is passed back as the reply;
                     sensitive topics (breakup/money/suicide/...) never auto-send.
Unconfigured chats are left to CowAgent's default brain untouched.

Config (config.json next to this file, see config.json.template):
  love_agent_home : path of the love-agent skill (or env LOVE_AGENT_HOME)
  outbox          : jsonl path for suggestions/decisions
  chats           : { "counterpart nickname": {"person_id": "...", "mode": "confirm",
                                               "persona": "...", "stage": "暧昧"} }
"""
import json
import os
import sys

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *


@plugins.register(
    name="LoveAgent",
    desire_priority=950,
    hidden=False,
    desc="恋爱军师：把指定微信聊天交给 love-agent 引擎（三模式+敏感话题拦截）",
    version="1.0.0",
    author="wumumofashi",
)
class LoveAgent(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.config = super().load_config() or self._load_config_template()
            self.chats = self.config.get("chats", {})
            self.outbox = self.config.get("outbox", "love_agent_outbox.jsonl")
            home = self.config.get("love_agent_home") or os.environ.get("LOVE_AGENT_HOME", "")
            if not home:
                raise RuntimeError("love_agent_home not set (config or LOVE_AGENT_HOME env)")
            if home not in sys.path:
                sys.path.insert(0, home)
            from love_agent.engine import LoveAgentEngine
            self.engine = LoveAgentEngine(home)
            self._seen = set()
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            logger.info(f"[LoveAgent] inited, chats={list(self.chats.keys())}, home={home}")
        except Exception as e:
            logger.error(f"[LoveAgent] init failed: {e}")
            raise

    def _load_config_template(self):
        try:
            p = os.path.join(os.path.dirname(__file__), "config.json.template")
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _append_outbox(self, record):
        try:
            with open(self.outbox, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"[LoveAgent] outbox write failed: {e}")

    def on_handle_context(self, e_context: EventContext):
        context = e_context["context"]
        if context.type != ContextType.TEXT:
            return
        msg = context.get("msg")
        chat = getattr(msg, "other_user_nickname", "") or getattr(msg, "from_user_nickname", "")
        cfg = self.chats.get(chat)
        if cfg is None or getattr(msg, "is_group", False):
            return  # not a configured 1:1 chat: leave to CowAgent default brain
        content = (context.content or "").strip()
        if not content:
            return
        msg_id = str(getattr(msg, "msg_id", "") or f"{chat}:{content}")
        if msg_id in self._seen:
            e_context.action = EventAction.BREAK_PASS
            return
        self._seen.add(msg_id)
        if len(self._seen) > 5000:
            self._seen = set(list(self._seen)[-2000:])

        mode = cfg.get("mode", "confirm")
        payload = {
            "content": content,
            "kind": "text",
            "person_id": cfg.get("person_id", "person_001"),
            "mode": mode,
            "record_memory": True,
        }
        if cfg.get("stage"):
            payload["relationship_stage"] = cfg["stage"]
        if cfg.get("persona"):
            payload["user_persona"] = cfg["persona"]
        out = self.engine.process(payload)

        record = {
            "chat": chat,
            "person_id": payload["person_id"],
            "incoming": content,
            "final_reply": out.get("final_reply", ""),
            "send_decision": out.get("send_decision"),
            "decision_reason": out.get("decision_reason", ""),
            "stage": out.get("relationship_stage"),
            "confidence": out.get("confidence"),
            "mode": mode,
        }
        should = bool(out.get("should_send")) and out.get("send_decision") == "auto_send"
        if mode == "autopilot" and should and record["final_reply"]:
            reply = Reply(ReplyType.TEXT, record["final_reply"])
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK  # hand final_reply to CowAgent to send
            record["sent"] = True
            logger.info(f"[LoveAgent] AUTO-SEND to {chat}: {record['final_reply']}")
        else:
            # suggest/confirm, or autopilot that did not pass the gates:
            # never send anything to the counterpart.
            e_context.action = EventAction.BREAK_PASS
            record["sent"] = False
            logger.info(
                f"[LoveAgent] suggestion for {chat} (mode={mode}, decision={record['send_decision']}): {record['final_reply']}"
            )
        self._append_outbox(record)

    def get_help_text(self, **kwargs):
        return "LoveAgent：指定微信聊天由 love-agent 引擎处理（建议/确认/自动三模式，敏感话题永不自动发送）。配置见 plugins/love_agent/config.json。"

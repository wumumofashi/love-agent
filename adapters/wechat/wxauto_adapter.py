"""WxAuto adapter: the chosen production WeChat transport for love-agent.

Why wxauto (surveyed 2026-10-09):
- cluic/wxauto: ~7.4k GitHub stars, Apache-2.0, actively maintained; works on
  the official Windows WeChat client (no web-protocol, no DB decryption).
- Alternatives rejected: Wechaty (23k stars) needs puppets (padlocal) that are
  paid/fragile for personal accounts; CowAgent (47k stars, ex chatgpt-on-wechat)
  is a whole competing agent framework, not a transport layer; LearnLove (kept
  in adapter.py) requires DB decryption and is heavier to deploy per customer.

This adapter is Windows-only at runtime (wxauto drives the WeChat UI). On any
other platform constructing it raises a clear error instead of faking success.
"""
from __future__ import annotations
import platform
from .adapter import WeChatMessage

class WxAutoWeChatAdapter:
    def __init__(self, wx=None):
        if wx is None:
            if platform.system() != "Windows":
                raise RuntimeError("WxAutoWeChatAdapter requires Windows with the WeChat client logged in (wxauto drives the UI).")
            try:
                from wxauto import WeChat  # type: ignore
            except Exception as e:
                raise RuntimeError("wxauto is not installed. On the Windows customer machine run: pip install wxauto (WeChat 3.x) or wxauto4 (WeChat 4.x).") from e
            wx = WeChat()
        self.wx = wx
        self.sent = []

    @staticmethod
    def _field(msg, name, default=""):
        if isinstance(msg, dict):
            return msg.get(name, default)
        return getattr(msg, name, default)

    def receive(self, msg, contact_id: str = "", contact_name: str = "") -> WeChatMessage:
        sender = self._field(msg, "sender", "")
        content = self._field(msg, "content", "")
        mtype = str(self._field(msg, "type", "text")).lower()
        kind = "text" if mtype in ("text", "friend", "self", "") else mtype
        return WeChatMessage(
            message_id=str(self._field(msg, "id", "") or hash((sender, content))),
            contact_id=contact_id or sender,
            contact_name=contact_name or sender,
            kind=kind, content=content,
            metadata={"transport": "wxauto", "raw_type": mtype},
        )

    def listen(self, chat_name: str):
        """Register a chat for listening; returns raw new messages from it."""
        try:
            self.wx.AddListenChat(chat_name)
        except Exception:
            pass
        msgs = self.wx.GetListenMessage(chat_name)
        return msgs or []

    def send(self, contact_id: str, text: str, dry_run: bool = True) -> dict:
        rec = {"contact_id": contact_id, "text": text, "dry_run": dry_run, "sent": False, "transport": "wxauto"}
        if dry_run:
            self.sent.append(rec); return rec
        self.wx.ChatWith(contact_id)
        self.wx.SendMsg(text, who=contact_id)
        rec["sent"] = True; self.sent.append(rec); return rec

    def monitor(self):
        return {"running": True, "mode": "wxauto-listen", "host": "Windows WeChat client"}

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class WeChatMessage:
    message_id: str
    contact_id: str
    contact_name: str=""
    kind: str="text"  # text|image|voice|video|emoji|file|link
    content: str=""
    timestamp: float=0
    metadata: dict=field(default_factory=dict)

class MockWeChatAdapter:
    """Safe default for tests/demo. Never touches a real WeChat client."""
    def __init__(self): self.sent=[]
    def receive(self, raw: dict) -> WeChatMessage:
        return WeChatMessage(message_id=raw.get("message_id","mock-1"),contact_id=raw.get("contact_id","person_001"),contact_name=raw.get("contact_name",""),kind=raw.get("kind","text"),content=raw.get("content",""),timestamp=raw.get("timestamp",0),metadata=raw.get("metadata",{}))
    def send(self, contact_id: str, text: str, dry_run: bool=True) -> dict:
        rec={"contact_id":contact_id,"text":text,"dry_run":dry_run,"sent":not dry_run}
        self.sent.append(rec); return rec
    def monitor(self): return {"running":False,"mode":"mock"}

class LearnLoveWeChatAdapter:
    """
    Production path assessed from jx-2-a/LearnLove (read 2026-10-08):
    - Receive: Windows WeChat local DB -> decrypt (wechat-decrypt/all_keys.json) -> DBCache -> monitor polls every ~2s
      -> agent/wechat_parser.normalize_message() unified fact object (type 1 text,3 image,34 voice,43 video,47 emoji,49 app/link/file)
    - Media: voice SILK archived from media_0.db -> SenseVoice/Whisper; image .dat archived -> Qwen2.5-VL/OCR provider
    - Send: agent/tools/send.py copy_to_clipboard (Valve L1) or pyautogui auto_send (Valve L2: activate WeChat, Ctrl+F contact, paste, Enter)
    - Gate: agent/valve.py L0 READ / L1 SUGGEST / L2 SEND
    This class is an interface wrapper; on Linux/dev it stays dry-run until run on the user's Windows host with LearnLove installed.
    """
    def __init__(self, data_dir: str="", valve_level: int=1): self.data_dir=data_dir; self.valve_level=valve_level
    def receive(self, raw: dict) -> WeChatMessage: return MockWeChatAdapter().receive(raw)
    def send(self, contact_id: str, text: str, dry_run: bool=True) -> dict:
        if self.valve_level < 2: return {"contact_id":contact_id,"text":text,"sent":False,"blocked_by":"valve<L2 SEND; confirmation required"}
        return {"contact_id":contact_id,"text":text,"sent":False,"dry_run":dry_run,"note":"execute via LearnLove send.auto_send on Windows host"}
    def monitor(self): return {"running":False,"mode":"learnlove-db-poll","interval_sec":2,"host":"Windows WeChat required"}

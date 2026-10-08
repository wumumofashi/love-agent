from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

STAGES=["陌生","认识","普通朋友","熟人","暧昧","追求","恋爱","稳定恋爱","冲突","冷淡","分手","复合期","婚姻"]
FORBIDDEN_AUTO_TOPICS=["分手","复合","借钱","转账","金钱","结婚","婚姻","重大承诺","性决定","威胁","法律","自杀","自伤","家暴"]

@dataclass
class Interpretation:
    hypothesis: str
    confidence: float
    evidence: list[str]=field(default_factory=list)
    alternative_note: str=""

@dataclass
class Candidate:
    label: str
    text: str
    intent: str=""
    tone: str=""
    risk: float=0.0

def empty_context() -> dict[str,Any]:
    return {
        "person": {}, "relationship_stage": "", "stage_confidence": 0.0,
        "alternative_stages": [], "recent_context": "", "current_message": "",
        "observed_facts": [], "possible_interpretations": [], "confidence": 0.0,
        "emotional_state": {}, "relationship_dynamics": {}, "user_goal": "",
        "recommended_strategy": "", "reply_intent": "", "tone": "",
        "things_to_avoid": [], "candidate_replies": [], "simulated_reactions": [],
        "critic_results": [], "final_reply": "", "should_send": False,
        "send_decision": "", "decision_reason": "", "mode": "suggest",
        "knowledge_used": [], "memory_updates": [], "multimodal": {},
    }

def to_dict(obj):
    return asdict(obj) if hasattr(obj,"__dataclass_fields__") else obj

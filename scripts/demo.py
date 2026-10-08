import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from love_agent.engine import LoveAgentEngine
eng=LoveAgentEngine()
cases=[
 {"person_id":"person_001","content":"今天加班好累，饭都没吃","relationship_stage":"暧昧","mode":"confirm"},
 {"person_id":"person_001","content":"嗯","relationship_stage":"暧昧","recent_context":"昨天聊得很热，今天突然只回嗯","mode":"autopilot"},
 {"person_id":"person_001","content":"我们分手吧","relationship_stage":"恋爱","mode":"autopilot"},
 {"person_id":"person_001","kind":"image","description":"一张海边落日自拍","relationship_stage":"暧昧","mode":"suggest"},
]
for c in cases:
    out=eng.process(c)
    print(json.dumps({k:out[k] for k in ("current_message","relationship_stage","stage_confidence","possible_interpretations","recommended_strategy","final_reply","confidence","send_decision","decision_reason")},ensure_ascii=False,indent=2))
    print("---")

from __future__ import annotations
from .simulator import PRESSURE, NEEDY, AI_TONE, INTIMATE

def critique(candidate: dict, ctx: dict, simulation: dict) -> dict:
    text=candidate.get("text","")
    checks=[]
    def add(name, passed, detail=""):
        checks.append({"check":name,"pass":bool(passed),"detail":detail})
    flags=ctx.get("relationship_dynamics",{}).get("flags",[])
    add("1_overinterpretation", not any(w in text for w in ["你就是","你肯定是","你其实就是"]), "不得把猜测写成对方动机")
    add("2_guess_as_fact", "肯定是因为" not in text and "就是吃醋" not in text, "推断需带概率")
    stage_ok=not (ctx.get("relationship_stage") in ("陌生","认识","普通朋友") and any(w in text for w in INTIMATE))
    add("3_stage_match", stage_ok, f"stage={ctx.get('relationship_stage')}")
    add("4_not_needy", not any(w in text for w in NEEDY), "需求感检查")
    add("5_not_cold", text not in ("哦","嗯","随便","你忙你的吧") and not text.endswith("吧，我没事"), "避免冷漠赌气")
    add("6_low_pressure", not any(w in text for w in PRESSURE) and simulation.get("risk",0)<0.75, f"risk={simulation.get('risk')}")
    add("7_not_manipulative", not any(w in text for w in ["故意不回","让她 jealous","欲擒故纵","测试她","服从"]), "不操控")
    add("8_user_intent_match", bool(text) or ctx.get("send_decision")=="no_send", "空回复仅用于不回复判断")
    # repetition / memory conflict: simple hooks supplied by engine in ctx
    repeated=text and text in ctx.get("recent_sent_texts",[])
    add("9_not_repeated", not repeated, "避免复读上一句")
    conflict=text and any(w in text for w in ctx.get("memory_conflicts",[]))
    add("10_memory_consistent", not conflict, "与人物记忆冲突词检查")
    add("11_not_ai_tone", not any(w in text for w in AI_TONE) and len(text)<=120, "去AI腔/报告腔")
    add("12_necessary", bool(text) or "silence" in flags, "无必要时允许不回复")
    failed=[c for c in checks if not c["pass"]]
    return {"reply":text,"checks":checks,"passed":len(failed)==0,"failed_checks":[f["check"] for f in failed],"score":round(1-len(failed)/12,2)}

def revise(candidate: dict, critic: dict, ctx: dict) -> dict:
    text=candidate.get("text","")
    if critic.get("passed") or not text: return candidate
    # deterministic light revision: shorten, remove pressure phrases
    for w in PRESSURE+NEEDY:
        text=text.replace(w,"")
    if len(text)>70: text=text[:62].rstrip("，。！？")+"。"
    if not text: text="没事，你先忙。想聊的时候喊我。"
    revised=dict(candidate); revised["text"]=text; revised["label"]=candidate.get("label","修正版"); revised["revised"]=True
    return revised

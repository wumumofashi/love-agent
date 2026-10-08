from __future__ import annotations
PRESSURE=["为什么不回","你必须","到底","求你","别离开我","不许","马上回","你总是","你从来","不回我是不是"]
NEEDY=["没有你不行","我离不开","求你了","别不要我"]
AI_TONE=["我理解你的感受","作为一个","希望能帮助你","深表歉意","综上所述"]
INTIMATE=["宝宝","宝贝","想你了","亲爱的"]

def simulate(candidate: dict, ctx: dict) -> dict:
    text=candidate.get("text","")
    if not text:
        return {"reply":"","predicted_reaction":["对方不会收到新压力","适合观察等待"],"risk":0.05,"pressure":0.0,"interest":0.3}
    risk=0.18; notes=[]
    if len(text)>80: risk+=0.25; notes.append("可能觉得长篇压力大")
    if text.count("？")+text.count("?")>=2: risk+=0.15; notes.append("可能觉得被连环追问")
    for w in PRESSURE:
        if w in text: risk+=0.35; notes.append("可能觉得被质问或施压")
    for w in NEEDY:
        if w in text: risk+=0.4; notes.append("可能觉得需求感过高")
    for w in AI_TONE:
        if w in text: risk+=0.2; notes.append("可能觉得像AI或咨询报告")
    stage=ctx.get("relationship_stage","认识")
    if stage in ("陌生","认识","普通朋友","熟人") and any(w in text for w in INTIMATE): risk+=0.35; notes.append("可能觉得越界或太快")
    if "你 busy" in text: risk+=0.1
    interest=0.55
    if "？" in text or "?" in text: interest+=0.1
    if len(text)<=45: interest+=0.08
    risk=max(0.0,min(0.95,risk)); interest=max(0.0,min(0.95,interest))
    reactions=notes[:3] or ["大概率会自然接话","不会有明显压力","愿意继续聊的概率中等"]
    if risk>=0.6: reactions=["可能防御或冷淡","可能觉得有压力"]+reactions[:1]
    return {"reply":text,"predicted_reaction":reactions,"risk":round(risk,2),"pressure":round(min(0.95,risk),2),"interest":round(interest,2),"willingness_to_continue":round(max(0.05,interest-risk*0.5),2)}

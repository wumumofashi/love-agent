from __future__ import annotations

def plan_reply(ctx: dict) -> dict:
    stage=ctx.get("relationship_stage","认识")
    flags=ctx.get("relationship_dynamics",{}).get("flags",[])
    emo=ctx.get("emotional_state",{})
    if "breakup" in flags: intent, tone, strategy = "respect_and_clarify","克制真诚","先尊重决定，不纠缠；只确认是否还有沟通空间"
    elif "rejection" in flags: intent, tone, strategy = "graceful_exit","体面克制","接受信号，体面收尾，保留自尊"
    elif "conflict" in flags: intent, tone, strategy = "de-escalate","平静共情","先降温和承认感受，不争对错，不翻旧账"
    elif "cold" in flags: intent, tone, strategy = "low_pressure_reconnect","轻松低压","低压力接住，不追问为什么不回，给对方台阶"
    elif "silence" in flags: intent, tone, strategy = "wait_or_light_ping","克制","优先不追发；如需发，只发一条无压力分享"
    elif "jealousy" in flags: intent, tone, strategy = "reassure_without_control","稳重坦诚","给确定性但不控制，不用反激将"
    elif "apology_needed" in flags: intent, tone, strategy = "own_and_repair","真诚具体","具体认错+影响+补救，不甩锅不卖惨"
    elif "misunderstanding" in flags: intent, tone, strategy = "clarify","清晰温和","澄清事实和本意，给对方确认机会"
    elif "date_opportunity" in flags: intent, tone, strategy = "invite","自然具体","给具体低压邀约选项，可拒绝"
    elif "reconcile" in flags: intent, tone, strategy = "reconcile_careful","克制真诚","不冲动答应也不冷处理，先确认分开原因是否解决，必须用户确认"
    elif "money" in flags: intent, tone, strategy = "money_boundary","稳重清晰","金钱问题先问清用途与金额，不自动承诺，必须用户确认"
    elif "passive_aggressive" in flags: intent, tone, strategy = "acknowledge_subtext","温和稳重","不阴阳回去，不赌气；轻轻确认感受，给台阶把话说开"
    elif "proactive_goodwill" in flags: intent, tone, strategy = "warm_reciprocate","真诚开心","具体感谢对方心意，自然回馈，不受宠若惊也不理所当然"
    elif "flirt_signal" in flags: intent, tone, strategy = "light_flirt","自然轻松","轻接好感，不油腻，不强行升温"
    elif emo.get("primary") in ("难过","累","焦虑","生气","疲惫/难过"): intent, tone, strategy = "comfort","温暖具体","先共情具体处境，再给陪伴，不讲大道理"
    elif ctx.get("multimodal",{}).get("kind") in ("image","video"): intent, tone, strategy = "respond_to_share","自然具体","回应图片/视频的具体细节和分享意图，不只夸好看"
    elif ctx.get("multimodal",{}).get("kind")=="voice": intent, tone, strategy = "respond_to_voice","自然具体","先回应语音核心内容，确认听清，不假装听见未转写内容"
    elif stage in ("陌生","认识","相亲"): intent, tone, strategy = "get_to_know","礼貌好奇","围绕对方具体信息好奇提问，保持分寸"
    elif stage in ("婚姻","稳定恋爱"): intent, tone, strategy = "maintain","踏实亲近","务实关心+共同安排，少套路多兑现"
    else: intent, tone, strategy = "continue","自然","接住话题，加入自己的视角，再递回一个好接的点"
    avoid=["把猜测当事实","长篇解释","连续追问","油腻情话","过度热情","施压回复","翻旧账"]
    if stage in ("陌生","认识","普通朋友"): avoid+=["亲昵称呼","强行暧昧"]
    if "conflict" in flags: avoid+=["你总是/你从来","冷嘲热讽"]
    return {"reply_intent":intent,"tone":tone,"recommended_strategy":strategy,"things_to_avoid":avoid}

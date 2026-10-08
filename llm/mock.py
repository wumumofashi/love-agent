from __future__ import annotations
import json, re
from .provider import LLMProvider

COLD_SCORES={"嗯":0.82,"嗯嗯":0.58,"哦":0.88,"哦哦":0.7,"行":0.6,"行吧":0.66,"没事":0.42,"你忙你的":0.58,"你忙你的吧":0.6,"算了":0.76,"随你":0.72,"随便":0.7,"都可以":0.32,"好":0.45,"好的":0.4,"哈哈":0.25}

def _payload(prompt_payload): return prompt_payload if isinstance(prompt_payload, dict) else {}
def _ctx(p): return p.get("context",{}) if isinstance(p,dict) else {}

class MockLLMProvider(LLMProvider):
    """Deterministic semantic stand-in for CI. It reasons over message nuance,
    recent-context pattern and person model fields in the prompt payload - it is
    NOT the old keyword template chain, and it is labelled mock wherever used."""
    name="mock"
    def __init__(self): self.calls=[]; self.fallback_reason=""
    def available(self): return True
    def complete_json(self, task, system, payload):
        self.calls.append({"task":task,"system":system,"payload":json.dumps(payload,ensure_ascii=False)})
        fn=getattr(self, f"task_{task}")
        return fn(payload)

    # -- helpers reading semantic features from payload --
    def _features(self, p):
        ctx=_ctx(p); msg=(ctx.get("current_message") or "").strip()
        recent=ctx.get("recent_context","") or ""
        person=ctx.get("person",{}) or {}
        prefs=(person.get("preferences") or {})
        style=" ".join([str(prefs.get("chat_style","")), " ".join(prefs.get("likes",[])), " ".join(person.get("boundaries",[]) if isinstance(person.get("boundaries"),list) else [])])
        hist="neutral"
        if any(w in recent for w in ["聊得很热","聊得开","很热","火热"]): hist="hot"
        if any(w in recent for w in ["冷淡","一个星期冷","持续冷","降温"]): hist="cold_week"
        if any(w in recent for w in ["争吵","吵架","刚吵","冲突"]): hist="conflict"
        if any(w in recent for w in ["普通朋友","朋友局"]): hist="friend"
        needs_space=any(w in style for w in ["空间","独立","慢热","不要高频"])
        high_freq=any(w in style for w in ["高频","黏","喜欢多聊","秒回"])
        avoid_conflict=any(w in style for w in ["回避冲突","不喜欢吵","怕冲突"])
        return {"msg":msg,"recent":recent,"hist":hist,"needs_space":needs_space,"high_freq":high_freq,"avoid_conflict":avoid_conflict,"person":person,"prefs":prefs,"ctx":ctx}

    def task_interpret(self, p):
        f=self._features(p); msg=f["msg"]; facts=f["ctx"].get("observed_facts",[]) or [f"对方说：{msg}"]
        cold=COLD_SCORES.get(msg, 0.35 if len(msg)<=4 else 0.15)
        interps=[]
        if f["hist"]=="hot" and cold>0.5:
            interps=[{"hypothesis":"在原本热络的基线下突然降温，可能有情绪或现实事务插入","confidence":0.62,"evidence":facts},{"hypothesis":"可能只是短暂忙碌，需看后续主动性","confidence":0.34,"evidence":facts}]
            emo={"primary":"降温敏感","intensity":0.6}
        elif f["hist"]=="cold_week" and cold>0.4:
            interps=[{"hypothesis":"延续一周冷淡模式，投入下降的解释权重上升，但仍不能断言动机","confidence":0.66,"evidence":facts},{"hypothesis":"对方可能在用低投入维持联系","confidence":0.4,"evidence":facts}]
            emo={"primary":"持续冷淡","intensity":0.6}
        elif f["hist"]=="conflict":
            interps=[{"hypothesis":"这句更像争吵后的余波或收尾，不宜当普通冷淡处理","confidence":0.64,"evidence":facts},{"hypothesis":"可能仍在生气，也可能想暂停冲突","confidence":0.48,"evidence":facts}]
            emo={"primary":"冲突余波","intensity":0.7}
        elif f["hist"]=="friend":
            interps=[{"hypothesis":"在普通朋友框架下这是低信息回复，未必代表关系降温","confidence":0.6,"evidence":facts}]
            emo={"primary":"平静","intensity":0.3}
        elif "没找我" in msg:
            base=0.45
            conf=0.62 if f["high_freq"] else 0.5
            interps=[{"hypothesis":"对方在表达想被主动联系的期待，可能带一点撒娇或试探","confidence":conf,"evidence":facts},{"hypothesis":"也可能只是随口一问，不宜过度解读为指责","confidence":0.35,"evidence":facts}]
            emo={"primary":"期待被在意","intensity":0.5}
        elif cold>0.6:
            interps=[{"hypothesis":"可能精力低或当下回复意愿下降","confidence":round(min(0.7,cold),2),"evidence":facts},{"hypothesis":"可能对当前话题兴趣不高","confidence":0.38,"evidence":facts}]
            emo={"primary":"冷淡","intensity":0.6}
        elif any(w in msg for w in ["分手","结束"]):
            interps=[{"hypothesis":"对方正在表达结束关系的决定或强烈冲动，需确认是否为气话","confidence":0.65,"evidence":facts}]
            emo={"primary":"决绝或冲动","intensity":0.8}
        else:
            interps=[{"hypothesis":"对方在正常分享或延续话题","confidence":0.55,"evidence":facts}]
            emo={"primary":"平静","intensity":0.3}
        signals=[{"signal":"short_low_information_reply","strength":round(cold,2)}] if cold>0.4 else []
        return {"observed_facts":facts,"possible_interpretations":interps,"emotional_state":emo,"relationship_signals":signals,"uncertainties":["单句信息不足，需结合基线与后续主动性验证"]}

    def task_stage(self, p):
        f=self._features(p); ctx=f["ctx"]; provided=ctx.get("provided_stage") or ""
        stage=provided or "认识"; conf=0.58
        flags=ctx.get("pre_flags",[])
        if "breakup" in flags: stage,conf="分手",0.7
        elif "conflict" in flags and provided in ("恋爱","稳定恋爱","婚姻"): stage,conf="冲突",0.66
        elif f["hist"]=="cold_week" and provided in ("暧昧","追求","恋爱"): stage,conf="冷淡",0.62
        alts=[]
        for s in ["普通朋友","暧昧","认识"]:
            if s!=stage: alts.append({"stage":s,"confidence":0.18})
        return {"stage":stage,"confidence":conf,"alternatives":alts[:2],"evidence_used":["provided_stage_as_evidence" if provided else "no_provided_stage","history_pattern="+f["hist"]]}

    def task_strategize(self, p):
        f=self._features(p); ctx=f["ctx"]; flags=ctx.get("pre_flags",[])
        interps=ctx.get("possible_interpretations",[])
        if "breakup" in flags: out=("尊重决定，不纠缠；只确认是否还有沟通空间","respect_and_clarify","克制真诚","reply")
        elif "rejection" in flags: out=("接受信号，体面收尾","graceful_exit","体面克制","reply")
        elif "conflict" in flags or f["hist"]=="conflict": out=("先降温和承认感受，不争对错","de-escalate","平静共情","reply")
        elif "date" in flags: out=("给具体低压邀约选项，可拒绝","invite","自然具体","reply")
        elif "jealousy" in flags: out=("给确定性但不控制","reassure_without_control","稳重坦诚","reply")
        elif "apology_needed" in flags: out=("具体认错+影响+补救","own_and_repair","真诚具体","reply")
        elif "misunderstanding" in flags: out=("澄清事实和本意","clarify","清晰温和","reply")
        elif "reconcile" in flags: out=("不冲动答应，先说清分开原因","reconcile_careful","克制真诚","reply")
        elif "money" in flags: out=("先问清用途与金额，不自动承诺","money_boundary","稳重清晰","reply")
        elif "passive_aggressive" in flags: out=("不阴阳回去，轻确认感受给台阶","acknowledge_subtext","温和稳重","reply")
        elif "proactive_goodwill" in flags: out=("具体感谢并自然回馈","warm_reciprocate","真诚开心","reply")
        elif "silence" in flags: out=("优先不追发，避免施压","wait_or_light_ping","克制","wait")
        elif "cold" in flags: out=("低压力接住，不追问为什么不回","low_pressure_reconnect","轻松低压","reply")
        elif f["ctx"].get("multimodal_kind") in ("image","video"): out=("回应具体细节和分享意图","respond_to_share","自然具体","reply")
        elif f["ctx"].get("multimodal_kind")=="voice": out=("回应语音核心，已转写才谈内容","respond_to_voice","自然具体","reply")
        elif "想被主动" in json.dumps(interps,ensure_ascii=False) or "没找我" in f["msg"]:
            out=("接住想被在意的期待，不反问施压","acknowledge_subtext","温和稳重","reply") if not f["needs_space"] else ("给空间，低频稳定联系即可","low_pressure_reconnect","克制","reply")
        elif ctx.get("relationship_stage") in ("陌生","认识","相亲"): out=("围绕具体信息好奇提问","get_to_know","礼貌好奇","reply")
        elif ctx.get("relationship_stage") in ("婚姻","稳定恋爱"): out=("务实关心+共同安排","maintain","踏实亲近","reply")
        elif any(w in f["msg"] for w in ["累","难受","烦"]): out=("先共情具体处境，再陪伴","comfort","温暖具体","reply")
        elif "flirt_signal" in flags: out=("轻接好感，不油腻不强行升温","light_flirt","自然轻松","reply")
        else: out=("接住话题，加入自己视角，递回好接的点","continue","自然","reply")
        avoid=["把猜测当事实","长篇解释","连续追问","油腻情话","施压回复"]
        if f["needs_space"]: avoid.append("高频追问")
        return {"goal":ctx.get("user_goal",""),"strategy":out[0],"reply_intent":out[1],"tone":out[2],"things_to_avoid":avoid,"wait_or_reply":out[3],"reasoning_summary":"基于事实、历史模式、人物模型与检索知识的概率判断"}

    def task_generate(self, p):
        f=self._features(p); ctx=f["ctx"]; intent=ctx.get("reply_intent","continue"); mm=ctx.get("multimodal",{})
        c=[]
        def add(label,text):
            if all(x["text"]!=text for x in c): c.append({"label":label,"text":text,"intent":intent})
        if f["needs_space"] and intent in ("acknowledge_subtext","continue"):
            add("自然型","在呢。今天有点忙，看到你消息了。你先忙你的，咱们有空再聊。")
        elif intent=="comfort": add("自然型","听起来今天是真的累着了。你先缓缓，不用硬撑，我在呢。"); add("轻松型","先下班模式关机一会儿。吃点热的，剩下的明天再说。")
        elif intent=="low_pressure_reconnect":
            nuance={"嗯嗯":"好嘞，那你先忙，晚点咱们再接着聊。","哦":"好，那我先不打扰了，你忙你的。","行吧":"行，那就先这么定，你有别的想法随时喊我。","没事":"真没事就行。有事别一个人憋着，随时跟我说。","算了":"先别急着算了嘛，卡在哪一步了？你说说看。","随你":"好，听你的。需要我搭把手的时候喊一声就行。","都可以":"行，那我来拍板，定好了发你看。"}
            add("自然型", nuance.get(f["msg"], "没事，你先忙你的。刚看到个有意思的，回头丢给你。"))
            add("稳妥","好，那你先休息。想聊的时候喊我。")
        elif intent=="wait_or_light_ping": c.append({"label":"建议不发","text":"","intent":intent}); add("低风险","刚刷到一个你可能会笑的，先存着，你忙完再看。")
        elif intent=="invite": add("自然型","这周末你要是有空，一起去试试那家你之前提过的店？没空也没事，咱们再约。"); add("轻松型","我发现个地方感觉你会喜欢。周六下午有空一起去看看？")
        elif intent=="de-escalate": add("低风险","我先不争这个。你刚才那句，我听着是有点委屈，是我没顾上你的感受。"); add("稳妥","等咱俩都平静点再说行吗？我不想越聊越冲。")
        elif intent=="clarify": add("自然型","我刚那句可能说得容易误会。我本意不是那个意思，是想说这事咱们可以慢慢商量。"); add("稳妥","怕你误会，我补一句：我不是在怪你，就是想把话说清楚。")
        elif intent=="reassure_without_control": add("自然型","这事我跟你说清楚，省得你瞎想。他就是同事，那天是大家一起吃的饭。"); add("稳妥","你在意这个，我其实挺开心的。以后这种场合我提前跟你说一声。")
        elif intent=="own_and_repair": add("自然型","这事是我的问题，我光顾着自己着急，没考虑你听着难受。对不起。"); add("稳妥","你生气有道理。我不找借口了，今晚我把这事处理好，再跟你交代。")
        elif intent=="respect_and_clarify": add("低风险","好，我尊重你。这个决定我听到了，不会再缠着你问。"); add("稳妥","如果之后你愿意把话说完，我听。不愿意，也就到这儿。")
        elif intent=="graceful_exit": add("低风险","明白，那我就不打扰了。祝你一切顺利。")
        elif intent=="reconcile_careful": add("低风险","我听到了。先别急着定，之前分开的那个问题，咱们得先说清楚。"); add("稳妥","我不是不想，就是不想稀里糊涂又回到老样子。你愿意慢慢聊聊吗？")
        elif intent=="money_boundary": add("低风险","你先跟我说下是啥情况，大概需要多少？我看完再回复你。")
        elif intent=="acknowledge_subtext": add("自然型","你这句听着不像没事。是不是我刚哪里让你不舒服了？你直说就行。"); add("稳妥","行，我先不猜。你想说的时候我在，不想说就先放一放。")
        elif intent=="warm_reciprocate": add("自然型","你还记得这个啊，被你投喂得很开心。下次换我来。"); add("轻松型","收到了，这份心意我先记账了，必须回请。")
        elif intent=="respond_to_share":
            desc=(mm.get("description","") or "").removeprefix("一张").removeprefix("一段")
            if desc: add("自然型",f"这个{desc}看着就很舒服，你今天是专门去的还是路过拍的？")
            else: add("自然型","这张氛围真好，是你今天拍的吗？")
            add("轻松型","可以啊，这状态看着比昨天精神多了。")
        elif intent=="respond_to_voice":
            if mm.get("transcript"): add("自然型","听到了。你说的那个事我懂了，咱们就按你说的来。")
            else: add("低风险","我这边刚没听清，你这条语音方便打个字不？不想打也没事，我回头再听。")
        elif intent=="get_to_know": add("自然型","听起来你对这个还挺有研究的。入门的时候踩过什么坑没？"); add("轻松型","这个我还真不太懂，你算是把我好奇心勾起来了。")
        elif intent=="maintain": add("自然型","行，那家里这个事就这么定。晚上回去咱们再把周末安排捋一下。")
        elif intent=="light_flirt": add("自然型","你这样说，我会有点当真了啊。"); add("轻松型","行，那我先记下了。欠我的，下次见面补。")
        else: add("自然型","哈哈这个我能懂。我刚才还刷到个差不多的，回头给你看。"); add("轻松型","你这一说我想起来了，上次那个事后来还真被你说中了。")
        return {"candidates":c[:3],"generation_basis":["strategy","person_model","recent_context","retrieved_scripts_tier_c_as_examples_only"]}

    def task_simulate(self, p):
        f=self._features(p); ctx=f["ctx"]; cand=ctx.get("candidate",{})
        text=cand.get("text","")
        if not text: return {"interpretation":"不发送，不给对方新增压力","likely_reactions":["继续原有节奏","无新增误解"],"possible_reply":"","pressure":0.05,"interest":0.2,"risk":0.05,"uncertainty":"无法知道对方沉默原因，模拟仅为概率"}
        risk=0.2; pressure=0.2; interest=0.55
        if len(text)>80: risk+=0.2; pressure+=0.15
        if text.count("？")+text.count("?")>=2: risk+=0.12; pressure+=0.1
        if any(w in text for w in ["为什么","到底","是不是忙忘了","怎么没找","求你"]): risk+=0.25; pressure+=0.25
        if f["needs_space"] and any(w in text for w in ["怎么没","想我","找我"]): risk+=0.3; pressure+=0.3
        if f["avoid_conflict"] and any(w in text for w in ["说清楚","必须","凭什么"]): risk+=0.25
        if f["high_freq"] and any(w in text for w in ["在呢","想聊"]): interest+=0.15; risk-=0.05
        interp="对方大概率会理解为正常回应"
        if risk>0.55: interp="对方可能理解为被追问或被施压"
        possible="嗯嗯" if risk>0.55 else "可能会自然接一句自己的近况"
        return {"interpretation":interp,"likely_reactions":["防御或敷衍"] if risk>0.55 else ["自然接话","愿意继续聊"],"possible_reply":possible,"pressure":round(min(0.95,pressure),2),"interest":round(max(0.05,min(0.95,interest)),2),"risk":round(max(0.02,min(0.95,risk)),2),"uncertainty":"基于人物模型与近期模式的概率模拟，不是真实预测"}

    def task_critic(self, p):
        f=self._features(p); ctx=f["ctx"]; cand=ctx.get("candidate",{}); text=cand.get("text","")
        issues=[]
        if any(w in text for w in ["就是吃醋","肯定是因为"]): issues.append("把猜测当事实")
        if f["needs_space"] and any(w in text for w in ["怎么没","找我","想我"]): issues.append("与人物空间边界冲突，施压")
        if any(w in text for w in ["到底","为什么不回","求你"]): issues.append("施压或需求过高")
        if "作为一个" in text or "我理解你的感受" in text: issues.append("不像真人，像AI咨询")
        if text and len(text)>110: issues.append("过长")
        return {"llm_pass":len(issues)==0,"issues":issues,"suggestion":"降低压力，给空间，短句具体" if issues else "可发送或按模式决策"}

    def task_revise(self, p):
        ctx=_ctx(p); text=(ctx.get("candidate",{}) or {}).get("text","")
        revised=text
        for w in ["到底","为什么不回","求你了"]: revised=revised.replace(w,"")
        if len(revised)>70: revised=revised[:60].rstrip("，。！？")+"。"
        if not revised or any(w in text for w in ["怎么没","找我"]):
            revised="在呢，我看到啦。你先忙你的，咱们有空再慢慢聊。"
        return {"text":revised,"changed":revised!=text}

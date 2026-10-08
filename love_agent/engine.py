from __future__ import annotations
import json, re
from pathlib import Path
from .schema import empty_context, STAGES, FORBIDDEN_AUTO_TOPICS
from .memory import PersonMemoryStore
from .knowledge import KnowledgeBase
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from reply.planner import plan_reply
from reply.generator import generate_candidates
from reply.simulator import simulate
from reply.critic import critique, revise
from multimodal.vision import describe_image
from multimodal.audio import transcribe_voice, video_frames

DEFAULT_CONFIG={"autopilot_min_confidence":0.85,"confirm_min_confidence":0.60,"max_auto_risk":0.35,"sensitive_topics":FORBIDDEN_AUTO_TOPICS}

COLD={"嗯","哦","好","好的","行","哈哈","嗯嗯","哦哦","知道了"}
PASSIVE=["你忙你的吧","随便你","无所谓","呵呵","你开心就好","行吧，你说的都对"]
FLIRT=["想你","撩","心动","好看","喜欢你","约吗","一起吃饭","周末一起"]
REJECT=["别联系","不想聊","有男朋友","有女朋友","不合适","别烦","拉黑","停止联系"]
BREAKUP=["分手","结束吧","过不下去了","离婚"]
CONFLICT=["你总是","你从来","吵","生气","凭什么","受够了"]
JEALOUS=["那个男生是谁","那个女生是谁","吃醋","你跟他","你跟她"]
MONEY=["借钱","转账","红包","多少钱","付款"]

class LoveAgentEngine:
    def __init__(self, project_root: str|Path|None=None, config: dict|None=None):
        self.root=Path(project_root) if project_root else Path(__file__).resolve().parent.parent
        cfg={}
        cfg_path=self.root/"config/default.json"
        if cfg_path.exists():
            try: cfg=json.loads(cfg_path.read_text(encoding="utf-8"))
            except Exception: cfg={}
        self.config={**DEFAULT_CONFIG, **cfg, **(config or {})}
        self.memory=PersonMemoryStore(self.root/"memory")
        self.kb=KnowledgeBase(self.root)

    # Observe
    def observe(self, raw: dict) -> dict:
        kind=raw.get("kind","text")
        if kind=="image": mm=describe_image(raw)
        elif kind=="voice": mm=transcribe_voice(raw)
        elif kind=="video": mm=video_frames(raw)
        elif kind in ("screenshot","ocr"): mm={"kind":"ocr","observed_facts":["对方/用户提供了聊天截图（需OCR且发言人低置信不硬判）"],"confidence":0.4}
        elif kind=="silence": mm={"kind":"silence","observed_facts":[f"对方已 {raw.get('hours',0)} 小时未回复"],"confidence":0.9}
        else: mm={"kind":kind,"observed_facts":[],"confidence":0.8}
        return mm

    def process(self, raw: dict) -> dict:
        ctx=empty_context()
        ctx["mode"]=raw.get("mode","suggest")
        ctx["user_goal"]=raw.get("user_goal","")
        person_id=raw.get("person_id","person_001")
        mem=self.memory.load(person_id)
        person={"person_id":person_id, **(raw.get("person") or {}), **(mem.get("profile") or {})}
        ctx["person"]=person
        ctx["recent_context"]=raw.get("recent_context","") or (mem.get("conversation_summary") or {}).get("summary","")
        ctx["recent_sent_texts"]=raw.get("recent_sent_texts",[])
        mm=self.observe(raw); ctx["multimodal"]=mm
        msg=raw.get("content","") or mm.get("transcript","") or mm.get("description","")
        ctx["current_message"]=msg
        facts=[]
        if raw.get("kind")=="silence": facts+=mm.get("observed_facts",[])
        elif msg: facts.append(f"对方说：{msg}")
        facts+= [f for f in mm.get("observed_facts",[]) if f not in facts]
        if raw.get("observed_facts"): facts+=raw["observed_facts"]
        ctx["observed_facts"]=facts
        # Interpret: flags + emotion, strictly probabilistic
        text=msg or ""
        flags=[]
        if raw.get("kind")=="silence" or raw.get("silence_hours"): flags.append("silence")
        if text.strip() in COLD or (len(text.strip())<=3 and text.strip()): flags.append("cold")
        if any(w in text for w in PASSIVE): flags.append("passive_aggressive")
        if any(w in text for w in FLIRT): flags.append("flirt_signal")
        if any(w in text for w in REJECT): flags.append("rejection")
        if any(w in text for w in BREAKUP): flags.append("breakup")
        if any(w in text for w in CONFLICT) or raw.get("scenario")=="conflict": flags.append("conflict")
        if any(w in text for w in JEALOUS) or raw.get("scenario")=="jealousy": flags.append("jealousy")
        if any(w in text for w in MONEY): flags.append("money")
        if "复合" in text: flags.append("reconcile")
        if any(w in text for w in ["给你带","给你买","请你吃","给你点了"]): flags.append("proactive_goodwill")
        if raw.get("scenario") in ("apology","misunderstanding","date","image","voice","video"): flags.append(raw["scenario"]+"_needed" if raw["scenario"] in ("apology",) else raw["scenario"])
        if "date" in flags: flags.append("date_opportunity")
        emo="平静"
        if any(w in text for w in ["累","烦","难受","哭","焦虑"]): emo="疲惫/难过"
        if "conflict" in flags: emo="生气/防御"
        if "passive_aggressive" in flags: emo="不满/试探"
        ctx["emotional_state"]={"primary":emo,"intensity":0.7 if emo!="平静" else 0.3}
        ctx["relationship_dynamics"]={"flags":flags,"reciprocity":"unknown","note":"dynamics inferred from behavior only, not mind-reading"}
        interps=[]
        def interp(h,c,ev): interps.append({"hypothesis":h,"confidence":c,"evidence":ev})
        if "cold" in flags: interp("可能忙或精力低，回复意愿暂时下降",0.45,facts); interp("可能对当前话题兴趣不高",0.35,facts)
        elif "silence" in flags: interp("可能在忙或需要空间，尚无足够证据判断关系降温",0.5,facts); interp("可能投入下降，需结合基线和后续主动性验证",0.32,facts)
        elif "passive_aggressive" in flags: interp("可能有不满或失望，但也可能只是随口语气",0.58,facts); interp("可能在试探用户是否在意",0.30,facts)
        elif "flirt_signal" in flags: interp("可能存在好感或愿意升温，仍需看持续主动和线下兑现",0.55,facts)
        elif "conflict" in flags: interp("可能感到不被理解或边界被碰到",0.6,facts)
        elif "breakup" in flags: interp("对方正在表达结束关系的决定或强烈冲动，需用户确认真实意图",0.65,facts)
        else: interp("对方在正常分享或延续话题",0.55,facts)
        ctx["possible_interpretations"]=interps
        # Stage estimate with alternatives, never forced
        rel=(mem.get("relationship") or {})
        stage=raw.get("relationship_stage") or rel.get("stage") or "认识"
        if "breakup" in flags: stage="分手"
        elif "conflict" in flags and stage in ("恋爱","稳定恋爱","婚姻"): stage="冲突"
        elif "cold" in flags and stage in ("暧昧","追求","恋爱"): stage="冷淡"
        sconf=float(raw.get("stage_confidence") or rel.get("stage_confidence") or 0.55)
        ctx["relationship_stage"]=stage; ctx["stage_confidence"]=sconf
        alt=[s for s in STAGES if s!=stage][:2]
        ctx["alternative_stages"]=[{"stage":alt[0],"confidence":round(max(0.05,1-sconf-0.15),2)}] if alt else []
        if len(alt)>1: ctx["alternative_stages"].append({"stage":alt[1],"confidence":0.08})
        # Strategize + plan
        plan=plan_reply(ctx); ctx.update(plan)
        # Knowledge on demand (Tier routing)
        ctx["knowledge_used"]=self.kb.search(text+" "+stage+" "+ctx["reply_intent"], limit=3)
        # Generate -> simulate -> critic -> revise
        cands=generate_candidates(ctx)
        sims=[]; crits=[]; finals=[]
        for cand in cands:
            sim=simulate(cand,ctx); sims.append(sim)
            crit=critique(cand,ctx,sim); crits.append(crit)
            finals.append(revise(cand,crit,ctx) if not crit["passed"] else cand)
        ctx["candidate_replies"]=finals; ctx["simulated_reactions"]=sims; ctx["critic_results"]=crits
        # Decide
        best_idx=min(range(len(finals)), key=lambda i: sims[i].get("risk",1)) if finals else 0
        best=finals[best_idx] if finals else {"text":""}
        ctx["final_reply"]=best.get("text","")
        risk=sims[best_idx].get("risk",0.5) if sims else 0.5
        evidence_q=0.8 if facts else 0.4
        conf=round(max(0.0,min(0.97, sconf*0.3+(1-risk)*0.45+evidence_q*0.25)),2)
        ctx["confidence"]=conf
        sensitive=any(t in text or t in stage for t in self.config.get("sensitive_topics",[])) or bool(set(flags)&{"breakup","money","rejection","conflict"})
        if not ctx["final_reply"]:
            ctx["should_send"]=False; ctx["send_decision"]="no_send"; ctx["decision_reason"]="建议不回复：等待对方或避免追发施压"
        elif ctx["mode"]=="suggest":
            ctx["should_send"]=False; ctx["send_decision"]="suggest_only"; ctx["decision_reason"]="建议模式：只给建议，用户自己发送"
        elif sensitive:
            ctx["should_send"]=False; ctx["send_decision"]="needs_confirmation"; ctx["decision_reason"]="敏感场景（分手/冲突/金钱/拒绝等）默认禁止自动发送，必须确认"
        elif ctx["mode"]=="confirm":
            ctx["should_send"]=False; ctx["send_decision"]="needs_confirmation"; ctx["decision_reason"]="确认模式：等待用户确认后发送"
        elif ctx["mode"]=="autopilot":
            if conf>=self.config["autopilot_min_confidence"] and risk<=self.config["max_auto_risk"]:
                ctx["should_send"]=True; ctx["send_decision"]="auto_send"; ctx["decision_reason"]=f"autopilot: confidence {conf}>= {self.config['autopilot_min_confidence']} 且 risk {risk} 低"
            elif conf>=self.config["confirm_min_confidence"]:
                ctx["should_send"]=False; ctx["send_decision"]="needs_confirmation"; ctx["decision_reason"]=f"autopilot 降级确认: confidence {conf} 在确认区间"
            else:
                ctx["should_send"]=False; ctx["send_decision"]="no_send"; ctx["decision_reason"]=f"confidence {conf} < {self.config['confirm_min_confidence']}，不自动回复"
        else:
            ctx["should_send"]=False; ctx["send_decision"]="needs_confirmation"; ctx["decision_reason"]="未知模式，按确认处理"
        # Memory update only on facts, not guesses
        if raw.get("record_memory", True):
            ctx["memory_updates"]=[self.memory.record_turn(person_id,msg,ctx["final_reply"] if ctx["should_send"] else "",facts)]
        return ctx

def process_message(raw: dict, project_root: str|Path|None=None) -> dict:
    return LoveAgentEngine(project_root).process(raw)

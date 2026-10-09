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
from reply.adversarial import adversarial_review
from reply.ai_fallback import ai_fallback_reason
from multimodal.vision import describe_image
from multimodal.audio import transcribe_voice, video_frames
from llm.provider import load_provider, LLMUnavailable

DEFAULT_CONFIG={"autopilot_min_confidence":0.85,"confirm_min_confidence":0.60,"max_auto_risk":0.35,"sensitive_topics":FORBIDDEN_AUTO_TOPICS}

COLD={"嗯","哦","好","好的","行","哈哈","嗯嗯","哦哦","知道了"}
PASSIVE=["你忙你的吧","随便你","无所谓","呵呵","你开心就好","行吧，你说的都对"]
FLIRT=["想你","撩","心动","好看","喜欢你","约吗","一起吃饭","周末一起"]
REJECT=["别联系","不想聊","有男朋友","有女朋友","不合适","别烦","拉黑","停止联系"]
BREAKUP=["分手","结束吧","过不下去了","离婚"]
CONFLICT=["你总是","你从来","吵","生气","凭什么","受够了"]
JEALOUS=["那个男生是谁","那个女生是谁","吃醋","你跟他","你跟她"]
MONEY=["借钱","转账","红包","多少钱","付款","借","借款","还钱"]

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
        person={"person_id":person_id, **(mem.get("profile") or {}),
                "preferences": mem.get("preferences") or {},
                "relationship": mem.get("relationship") or {},
                "interaction_patterns": mem.get("interaction_patterns") or {},
                "relationship_events": mem.get("relationship_events") or {}}
        raw_person=raw.get("person") or {}
        for k,v in raw_person.items():
            if isinstance(v,dict) and isinstance(person.get(k),dict): person[k]={**person[k], **v}
            else: person[k]=v
        ctx["person"]=person; ctx["person_memory"]=mem
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
        # Text-pattern silence detection: "没回"/"不回"/"冷战"/"沉默" + time indicator
        if any(w in text for w in ["没回","不回","冷战","沉默期"]) and any(w in text for w in ["天","小时","周","月"]):
            if "silence" not in flags: flags.append("silence")
        if text.strip() in COLD or (len(text.strip())<=3 and text.strip()): flags.append("cold")
        if any(w in text for w in PASSIVE): flags.append("passive_aggressive")
        if any(w in text for w in FLIRT): flags.append("flirt_signal")
        if any(w in text for w in REJECT):
            # Don't trigger rejection if the word is negated (e.g., "不拉黑" is not a rejection)
            has_rejection = False
            for w in REJECT:
                idx = text.find(w)
                if idx >= 0:
                    # Check if immediately preceded by negation
                    if idx > 0 and text[idx-1] in "不没非": continue
                    has_rejection = True; break
            if has_rejection: flags.append("rejection")
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
        # ---- Fast heuristic is only a pre-classifier / safety signal ----
        ctx["pre_flags"]=flags
        # ---- Knowledge retrieval (Tier-labelled) BEFORE LLM reasoning ----
        kb_hits=self.kb.search(text+" "+ctx["recent_context"]+" "+" ".join(flags), limit=3)
        ctx["knowledge_used"]=kb_hits
        kb_block=self.kb.prompt_block(kb_hits)
        # ---- LLM chain: interpret -> stage -> strategize -> generate -> simulate -> critic/revise ----
        llm_cfg=raw.get("llm_config") or {k:self.config[k] for k in ("provider","base_url","model","api_key_env","temperature","language") if k in self.config}
        provider=raw.get("llm_provider_instance") or load_provider(self.root, llm_cfg)
        ctx["llm_provider"]=getattr(provider,"name","unknown")
        ctx["llm_provider_used"]=ctx["llm_provider"]
        if getattr(provider,"fallback_reason",""): ctx["llm_fallback_reason"]=provider.fallback_reason
        ctx["real_llm_available"]=ctx["llm_provider"]=="openai_compatible"
        prompts_dir=self.root/"llm/prompts"
        lang=self.config.get("language","zh")
        # Allow runtime llm_config to override language
        _rc = raw.get("llm_config") or {}
        if "language" in _rc:
            lang = _rc["language"]
        lang_map={"zh":"中文","en":"English","ja":"日本語","ko":"한국어","es":"Español","fr":"Français","de":"Deutsch","vi":"Tiếng Việt","id":"Indonesia","th":"ไทย"}
        lang_name=lang_map.get(lang,"中文")
        def sysprompt(name):
            lang_short = lang if lang in ("en","ja","ko","es","fr","de","vi","id","th") else "zh"
            fp_lang = prompts_dir/f"{name}_{lang_short}.md"
            fp_default = prompts_dir/f"{name}.md"
            if fp_lang.exists():
                base = fp_lang.read_text(encoding="utf-8")
            elif fp_default.exists():
                base = fp_default.read_text(encoding="utf-8")
            else:
                base = f"You are the love-agent {name}. Output strict JSON only."
            if "{{LANGUAGE}}" in base:
                base = base.replace("{{LANGUAGE}}", lang_name)
            return base
        def payload(extra=None):
            base={"context":{"current_message":text,"recent_context":ctx["recent_context"],"person":ctx["person"],
                             "language":lang,"lang_name":lang_map.get(lang,"中文"),
                             "person_memory":mem,"provided_stage":raw.get("relationship_stage",""),"pre_flags":flags,
                             "observed_facts":facts,"multimodal":mm,"multimodal_kind":mm.get("kind","text"),
                             "relationship_stage":ctx.get("relationship_stage",""),"possible_interpretations":ctx.get("possible_interpretations",[]),
                             "reply_intent":ctx.get("reply_intent",""),"user_goal":ctx["user_goal"]},
                  "knowledge_tiered":kb_hits,"knowledge_prompt_block":kb_block,
                  "tier_rule":"Tier C is practical examples only, never scientific fact. Tier D is this person's memory and outranks generic advice."}
            if extra: base["context"].update(extra)
            return base
        llm_calls=[]
        try:
            interp_out=provider.complete_json("interpret", sysprompt("interpret"), payload()); llm_calls.append("interpret")
            if interp_out.get("possible_interpretations"):
                _raw_interps = interp_out["possible_interpretations"]
                # Cap confidence at 0.5 when minimal context (anti-overinterpretation)
                # Minimal context = no relationship stage info and no conversation history
                _has_context = bool(ctx.get("recent_context")) or bool(raw.get("relationship_stage"))
                if not _has_context:
                    _raw_interps = [{**i, "confidence": min(i.get("confidence", 0.5), 0.5)} for i in _raw_interps]
                ctx["possible_interpretations"] = _raw_interps
            else:
                default_hyp = {"hypothesis":"对方在正常分享或延续话题","evidence":facts}
                if not facts: default_hyp["confidence"]=0.35
                else: default_hyp["confidence"]=0.4
                ctx["possible_interpretations"]=[default_hyp]
            # Cap interpretation confidence when no solid evidence
            if not facts:
                for interp in ctx["possible_interpretations"]:
                    if interp.get("confidence",0) > 0.5:
                        interp["confidence"]=0.5
            if interp_out.get("observed_facts"): ctx["observed_facts"]=list(dict.fromkeys(facts+interp_out["observed_facts"]))
            if interp_out.get("emotional_state"): ctx["emotional_state"]=interp_out["emotional_state"]
            ctx["relationship_signals"]=interp_out.get("relationship_signals",[])
            ctx["uncertainties"]=interp_out.get("uncertainties",[])
            stage_out=provider.complete_json("stage", sysprompt("stage"), payload()); llm_calls.append("stage")
            stage=stage_out.get("stage") or raw.get("relationship_stage") or "认识"
            sconf=float(stage_out.get("confidence") or 0.55)
            ctx["relationship_stage"]=stage; ctx["stage_confidence"]=sconf
            ctx["alternative_stages"]=stage_out.get("alternatives",[])
            strat=provider.complete_json("strategize", sysprompt("strategize"), payload()); llm_calls.append("strategize")
            ctx["recommended_strategy"]=strat.get("strategy","")
            ctx["reply_intent"]=strat.get("reply_intent","continue")
            ctx["tone"]=strat.get("tone","自然")
            ctx["things_to_avoid"]=strat.get("things_to_avoid",[])
            ctx["wait_or_reply"]=strat.get("wait_or_reply","reply")
            ctx["strategy_reasoning"]=strat.get("reasoning_summary","")
            gen=provider.complete_json("generate", sysprompt("generate"), payload()); llm_calls.append("generate")
            cands=gen.get("candidates",[])
            if not cands: raise LLMUnavailable("LLM returned no candidates")
            sims=[]; crits=[]; finals=[]; iterations=0
            for cand in cands:
                cur=dict(cand); sim=None; crit=None
                for attempt in range(4):  # initial + max 3 revisions
                    sim_raw=provider.complete_json("simulate", sysprompt("simulate"), payload({"candidate":cur})); llm_calls.append("simulate")
                    sim={"reply":cur.get("text",""),"interpretation":sim_raw.get("interpretation",""),
                         "predicted_reaction":sim_raw.get("likely_reactions",[]),"possible_reply":sim_raw.get("possible_reply",""),
                         "pressure":sim_raw.get("pressure",0.3),"interest":sim_raw.get("interest",0.5),
                         "risk":sim_raw.get("risk",0.3),"uncertainty":sim_raw.get("uncertainty","概率模拟，非真实预测")}
                    rule_crit=critique(cur,ctx,sim)
                    llm_crit=provider.complete_json("critic", sysprompt("critic"), payload({"candidate":cur,"simulation":sim})); llm_calls.append("critic")
                    crit={"reply":cur.get("text",""),"rule_critic":rule_crit,"llm_critic":llm_crit,
                          "passed":bool(rule_crit.get("passed")) and bool(llm_crit.get("llm_pass",True)),
                          "checks":rule_crit.get("checks",[]),"failed_checks":rule_crit.get("failed_checks",[])+llm_crit.get("issues",[])}
                    if crit["passed"] or attempt==3: break
                    iterations+=1
                    rev=provider.complete_json("revise", sysprompt("revise"), payload({"candidate":cur,"critic":crit})); llm_calls.append("revise")
                    if rev.get("text"): cur={**cur,"text":rev["text"],"revised":True}
                    else: break
                sims.append(sim); crits.append(crit); finals.append(cur)
            ctx["critic_iterations"]=iterations
            # ---- Adversarial Review (Phase 2 P0) ----
            adv_results=[]
            for i, (cand, sim, crit) in enumerate(zip(finals, sims, crits)):
                adv = adversarial_review(cand, ctx, crit)
                adv_results.append(adv)
            ctx["adversarial_results"]=adv_results
            # If any critical counter, downgrade best candidate
            if adv_results:
                critical_total = sum(a.get("critical_count",0) for a in adv_results)
                if critical_total > 0:
                    ctx["adversarial_verdict"]="flagged"
                    ctx["adversarial_summary"]="发现需要修复的反方论点，已自动降级此候选"
                else:
                    ctx["adversarial_verdict"]="approve"
                    ctx["adversarial_summary"]=adv_results[0].get("summary","无重大反对意见")
            else:
                ctx["adversarial_verdict"]="n/a"
                ctx["adversarial_summary"]=""
        except Exception as e:
            # Fallback: old rule chain, explicitly labelled - never pretend this was LLM reasoning.
            ctx["llm_provider_used"]="rules_fallback"; ctx["llm_error"]=str(e)
            ctx["possible_interpretations"]=[{"hypothesis":"规则回退：对方在延续话题或给出低信息回复","confidence":0.35,"evidence":facts}]
            rel=(mem.get("relationship") or {}); stage=raw.get("relationship_stage") or rel.get("stage") or "认识"
            if "breakup" in flags: stage="分手"
            elif "conflict" in flags and stage in ("恋爱","稳定恋爱","婚姻"): stage="冲突"
            elif "cold" in flags and stage in ("暧昧","追求","恋爱"): stage="冷淡"
            ctx["relationship_stage"]=stage; sconf=float(rel.get("stage_confidence") or 0.45); ctx["stage_confidence"]=sconf
            plan=plan_reply(ctx); ctx.update(plan)
            finals=generate_candidates(ctx); sims=[]; crits=[]
            # AI fallback: when template generation returns empty AND LLM unavailable
            if not finals and not ctx.get("real_llm_available"):
                ctx["llm_provider_used"]="ai_fallback"
                ai_result = ai_fallback_reason(ctx)
                finals = [{"text": ai_result.get("reply", ""), "intent": ai_result.get("intent", "suggest_only"), "label": "AI推理"}]
                sims = [{"risk": ai_result.get("risk", 0.5), "interest": 0.4, "pressure": 0.2, "interpretation": ai_result.get("reason", "")}]
                crits = [{"passed": True, "checks": [], "failed_checks": []}]
                ctx["ai_fallback_used"] = True
                ctx["ai_fallback_reasoning"] = ai_result.get("reason", "")
                ctx["ai_fallback_alternatives"] = ai_result.get("alternatives", [])
            for cand in finals:
                sim=simulate(cand,ctx); crit=critique(cand,ctx,sim); sims.append(sim); crits.append(crit)
            ctx["critic_iterations"]=0
        ctx["llm_calls"]=llm_calls if 'llm_calls' in locals() else []
        ctx["llm_prompt_audit"]=getattr(provider,"calls",[])
        ctx["candidate_replies"]=finals; ctx["simulated_reactions"]=sims; ctx["critic_results"]=crits
        ctx["ai_fallback_used"] = ctx.get("ai_fallback_used", False)
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
            outcome=raw.get("outcome_of_previous_reply")
            if outcome and raw.get("previous_reply_text"):
                recorded=self.memory.record_outcome(person_id, raw["previous_reply_text"], outcome)
                if recorded: ctx["memory_updates"].append(recorded)
        return ctx

def process_message(raw: dict, project_root: str|Path|None=None) -> dict:
    return LoveAgentEngine(project_root).process(raw)

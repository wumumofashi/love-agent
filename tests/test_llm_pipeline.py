#!/usr/bin/env python3
"""LLM pipeline tests: verify the actual chain, prompt inclusion, and semantic
differentiation - not merely that rule templates fire. Mock LLM is the CI provider;
the real OpenAI-compatible provider is tested for configuration behaviour."""
import json, shutil, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from love_agent.engine import LoveAgentEngine
from llm.mock import MockLLMProvider
from llm.openai_compatible import OpenAICompatibleProvider
from llm.provider import LLMUnavailable

fails = []
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" :: {detail}" if detail and not cond else ""))
    if not cond: fails.append(name)

def main():
    eng = LoveAgentEngine(ROOT)

    # 1. Full chain really walks interpret->stage->strategize->generate->simulate->critic
    out = eng.process({"content":"嗯","relationship_stage":"暧昧","recent_context":"昨天聊得很热","mode":"confirm"})
    order = []
    for t in out.get("llm_calls",[]):
        if t not in order: order.append(t)
    check("pipeline task order", order[:6] == ["interpret","stage","strategize","generate","simulate","critic"], str(order))
    check("provider labelled mock in CI", out.get("llm_provider_used") == "mock", str(out.get("llm_provider_used")))
    check("real LLM honestly unavailable without config", out.get("real_llm_available") is False)

    # 2. Knowledge + Memory actually enter prompts
    audit = json.dumps(out.get("llm_prompt_audit",[]), ensure_ascii=False)
    check("tiered knowledge enters prompt", "Tier" in audit and "knowledge_prompt_block" in audit)
    with tempfile.TemporaryDirectory() as td:
        proj = Path(td)/"proj"; shutil.copytree(ROOT, proj, ignore=shutil.ignore_patterns(".git","__pycache__"))
        store_dir = proj/"memory/people/person_001"; store_dir.mkdir(parents=True, exist_ok=True)
        pref = {"likes":["喜欢先说结论"],"dislikes":[],"chat_style":"喜欢先说结论，不绕弯","triggers":[],"effective_replies":[],"negative_replies":[],"known_preferences":["喜欢先说结论"]}
        (store_dir/"preferences.json").write_text(json.dumps(pref,ensure_ascii=False),encoding="utf-8")
        out2 = LoveAgentEngine(proj).process({"content":"今天方案定了没","relationship_stage":"熟人","mode":"suggest","record_memory":False})
        audit2 = json.dumps(out2.get("llm_prompt_audit",[]), ensure_ascii=False)
        check("person memory enters prompt", "喜欢先说结论" in audit2)
        check("extended memory files exist", (store_dir/"interaction_patterns.json").exists() and (store_dir/"relationship_events.json").exists())

    # 3. Semantic variants of short replies must not collapse to one reading
    variants = ["嗯","嗯嗯","哦","行吧","没事","你忙你的","算了","随你","都可以"]
    finals, hyps = {}, {}
    for v in variants:
        o = eng.process({"content":v,"relationship_stage":"暧昧","recent_context":"","mode":"suggest","record_memory":False})
        finals[v] = o.get("final_reply","")
        hyps[v] = json.dumps(o.get("possible_interpretations",[]),ensure_ascii=False)
    check("semantic variants produce differentiated replies", len(set(finals.values())) >= 5, str(finals))
    check("semantic variants produce differentiated interpretations", len(set(hyps.values())) >= 5)
    cold = {v: max([i["confidence"] for i in eng.process({"content":v,"relationship_stage":"暧昧","mode":"suggest","record_memory":False}).get("possible_interpretations",[])]) for v in ["嗯","嗯嗯","都可以"]}
    check("nuance changes confidence (嗯 vs 嗯嗯 vs 都可以)", cold["嗯"] != cold["嗯嗯"] and cold["嗯"] != cold["都可以"], str(cold))

    # 4. Same '嗯' under different histories must be read differently
    histories = {
     "hot": "昨天聊得很热，聊到半夜",
     "cold_week": "连续一个星期冷淡，基本都是短回复",
     "conflict": "刚刚发生争吵，还没和好",
     "friend": "普通朋友，平时就这样有一搭没一搭",
    }
    readings = {}
    for k, h in histories.items():
        o = eng.process({"content":"嗯","relationship_stage":"普通朋友" if k=="friend" else "暧昧","recent_context":h,"mode":"suggest","record_memory":False})
        readings[k] = (json.dumps(o.get("possible_interpretations",[]),ensure_ascii=False), o.get("recommended_strategy",""), o.get("final_reply",""))
    check("same message, different histories -> different readings", len(set(readings.values())) >= 3, str(readings))

    # 5. Same line against different person models -> different simulation/strategy
    people = {
     "high_freq": {"preferences":{"chat_style":"喜欢高频沟通，黏一点也没关系","likes":[],"dislikes":[]}},
     "independent": {"preferences":{"chat_style":"独立型，需要空间，不要高频追问","likes":[],"dislikes":[]}},
     "avoid_conflict": {"preferences":{"chat_style":"回避冲突，不喜欢把话说死","likes":[],"dislikes":[]}},
     "needs_space": {"preferences":{"chat_style":"明确要求空间，忙时别连发","likes":[],"dislikes":[]},"boundaries":["需要空间"]},
    }
    sims = {}
    for k, person in people.items():
        o = eng.process({"content":"你今天怎么没找我","relationship_stage":"暧昧","mode":"confirm","person":person,"record_memory":False})
        s = (o.get("simulated_reactions") or [{}])[0]
        sims[k] = (o.get("final_reply",""), s.get("risk"), s.get("possible_reply",""), s.get("interpretation",""))
    check("person models change simulation/reply", len(set(sims.values())) >= 3, str(sims))

    # 6. Revision loop: a pressurised first candidate must be criticised and revised (max 3)
    class BadFirst(MockLLMProvider):
        def task_generate(self, p):
            return {"candidates":[{"label":"高压版","text":"你到底怎么没找我，为什么不回我？","intent":"acknowledge_subtext"}]}
    out3 = eng.process({"content":"你今天怎么没找我","relationship_stage":"暧昧","mode":"confirm","record_memory":False,"llm_provider_instance":BadFirst()})
    check("critic triggers revision", (out3.get("critic_iterations") or 0) >= 1, str(out3.get("critic_iterations")))
    check("revised reply drops pressure words", "到底" not in out3.get("final_reply","") and "为什么不回" not in out3.get("final_reply",""), out3.get("final_reply",""))
    check("revision bounded", (out3.get("critic_iterations") or 0) <= 3)

    # 7. Real provider: exists, correctly refuses when unconfigured (no fake success)
    try:
        OpenAICompatibleProvider(base_url="", model="").complete_json("interpret","s",{})
        check("real provider refuses unconfigured", False)
    except LLMUnavailable:
        check("real provider refuses unconfigured", True)
    o4 = LoveAgentEngine(ROOT, config={"provider":"openai_compatible","base_url":"","model":""}).process({"content":"在吗","mode":"suggest","record_memory":False})
    check("incomplete real config falls back honestly", o4.get("llm_provider_used")=="mock" and bool(o4.get("llm_fallback_reason")))

    # 8. Sensitive topics still blocked at the rule safety gate even in autopilot
    o5 = eng.process({"content":"我们分手吧","relationship_stage":"恋爱","mode":"autopilot","record_memory":False})
    check("safety gate blocks breakup autopilot", o5.get("should_send") is False and o5.get("send_decision")=="needs_confirmation")

    print(f"\nLLM PIPELINE: {9-len(fails) if False else ''}{'FAILED '+str(fails) if fails else 'ALL PASS'}")
    return 1 if fails else 0

if __name__ == "__main__":
    raise SystemExit(main())

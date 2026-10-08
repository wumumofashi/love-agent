import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from love_agent.engine import LoveAgentEngine

def check(out, exp):
    errs=[]
    if exp.get("has_final") and not out.get("final_reply"): errs.append("final_reply empty")
    if exp.get("flag") and exp["flag"] not in out.get("relationship_dynamics",{}).get("flags",[]): errs.append(f"missing flag {exp['flag']} got {out.get('relationship_dynamics')}")
    if exp.get("stage") and out.get("relationship_stage")!=exp["stage"]: errs.append(f"stage {out.get('relationship_stage')} != {exp['stage']}")
    if exp.get("intent") and out.get("reply_intent")!=exp["intent"]: errs.append(f"intent {out.get('reply_intent')} != {exp['intent']}")
    if exp.get("decision") and out.get("send_decision")!=exp["decision"]: errs.append(f"decision {out.get('send_decision')} != {exp['decision']}")
    if exp.get("decision_in") and out.get("send_decision") not in exp["decision_in"]: errs.append(f"decision {out.get('send_decision')} not in {exp['decision_in']}")
    if "should_send" in exp and out.get("should_send")!=exp["should_send"]: errs.append(f"should_send {out.get('should_send')} != {exp['should_send']}")
    if exp.get("not_decision") and out.get("send_decision")==exp["not_decision"]: errs.append("decision should not be auto_send")
    if exp.get("multimodal_kind") and out.get("multimodal",{}).get("kind")!=exp["multimodal_kind"]: errs.append(f"multimodal {out.get('multimodal')} != {exp['multimodal_kind']}")
    if exp.get("final_not_equals") and out.get("final_reply")==exp["final_not_equals"]: errs.append("final too generic")
    if exp.get("interpretation_max_confidence_le") is not None:
        mx=max([i.get("confidence",0) for i in out.get("possible_interpretations",[])] or [0])
        if mx>exp["interpretation_max_confidence_le"]: errs.append(f"interpretation overconfident {mx}")
    if exp.get("no_assertion_in_final") and any(w in out.get("final_reply","") for w in ["就是吃醋","肯定是因为"]): errs.append("final asserts motive")
    if exp.get("person_id") and out.get("person",{}).get("person_id")!=exp["person_id"]: errs.append("person mismatch")
    if exp.get("has_memory_update") and not out.get("memory_updates"): errs.append("memory not updated")
    # universal standards
    if not out.get("observed_facts"): errs.append("no observed_facts")
    if not out.get("possible_interpretations"): errs.append("no interpretations")
    if out.get("candidate_replies") and not out.get("simulated_reactions"): errs.append("no simulation")
    if out.get("candidate_replies") and not out.get("critic_results"): errs.append("no critic")
    for c in out.get("critic_results",[]):
        if len(c.get("checks",[]))!=12: errs.append("critic checks !=12"); break
    return errs

def main():
    scenarios=json.loads((ROOT/"tests/scenarios.json").read_text(encoding="utf-8"))
    eng=LoveAgentEngine(ROOT)
    passed=failed=0; lines=[]
    for s in scenarios:
        out=eng.process(dict(s["input"]))
        errs=check(out, s.get("expect",{}))
        status="PASS" if not errs else "FAIL"
        if errs: failed+=1
        else: passed+=1
        lines.append(f"{status} {s['id']} {s['name']} stage={out.get('relationship_stage')} conf={out.get('confidence')} decision={out.get('send_decision')} final={out.get('final_reply')!r} errs={errs}")
        print(lines[-1])
    print(f"\nTOTAL {passed} passed, {failed} failed, {len(scenarios)} scenarios")
    (ROOT/"tests/last_run.txt").write_text("\n".join(lines)+f"\nTOTAL {passed} passed, {failed} failed\n",encoding="utf-8")
    return 1 if failed else 0
if __name__=="__main__": raise SystemExit(main())

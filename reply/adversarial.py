"""Adversarial review module — independent counter-argument generator.

This runs AFTER critic and BEFORE final output. It generates structured
counter-arguments that challenge the chosen response from at least 3 angles:
  1. The other person's likely negative interpretation
  2. An alternative explanation of the same facts
  3. A simpler/more direct alternative
"""
from __future__ import annotations


def adversarial_review(candidate: dict, ctx: dict, critic_result: dict) -> dict:
    """Run independent adversarial review. Returns list of counter-arguments."""
    text = candidate.get("text", "")
    stage = ctx.get("relationship_stage", "认识")
    flags = ctx.get("relationship_dynamics", {}).get("flags", [])
    person = (ctx.get("person") or {}).get("name", "对方")
    recent = ctx.get("recent_context", "")

    counters = []

    # Counter 1: Other-person interpretation challenge
    alt_interp = _generate_alternative_interpretation(text, stage, flags, recent, person)
    if alt_interp:
        counters.append({
            "angle": "对方可能这样理解",
            "challenge": alt_interp,
            "severity": "medium",
            "requires_fix": False,
        })

    # Counter 2: Simpler/more direct alternative
    simpler = _suggest_simpler_alternative(text, stage, flags)
    if simpler:
        counters.append({
            "angle": "更直接的说法",
            "challenge": simpler,
            "severity": "low",
            "requires_fix": False,
        })

    # Counter 3: Over-reaction risk
    overreact = _check_overreaction(text, flags, stage)
    if overreact:
        counters.append({
            "angle": "过度反应风险",
            "challenge": overreact,
            "severity": "high",
            "requires_fix": True,
        })

    # Counter 4: Missing information gap
    missing = _identify_missing_info(ctx)
    if missing:
        counters.append({
            "angle": "信息缺口",
            "challenge": missing,
            "severity": "medium",
            "requires_fix": False,
        })

    # Counter 5: Pattern repetition check
    repeated = _check_pattern_repeat(text, ctx)
    if repeated:
        counters.append({
            "angle": "模式重复风险",
            "challenge": repeated,
            "severity": "high",
            "requires_fix": True,
        })

    return {
        "counters": counters,
        "total": len(counters),
        "critical_count": sum(1 for c in counters if c.get("requires_fix")),
        "verdict": "approve" if not counters else "flagged",
        "summary": _summarize_counters(counters),
    }


def _generate_alternative_interpretation(text, stage, flags, recent, person):
    """Find an alternative reading of the same facts."""
    challenges = []

    if any(f in flags for f in ("silence", "cold")):
        if "忙" not in text and "工作" not in text:
            challenges.append(
                f"对方可能只是在忙/累，你的回复过度关注了。"
                f"直接问'在干嘛'可能让对方觉得被催促。"
            )
    if any(f in flags for f in ("conflict",)):
        if "对不起" in text or "我的错" in text:
            challenges.append(
                "过度道歉可能让对方觉得你在认全责，而不是解决问题。"
                "可以聚焦具体行为而非笼统认错。"
            )
    if any(f in flags for f in ("jealousy",)):
        if "那个" in text:
            challenges.append(
                "提到'那个男生/女生'可能让对方觉得你在追问或吃醋。"
                "可以更直接表达感受而非暗示怀疑。"
            )
    if stage in ("陌生", "认识", "普通朋友"):
        if any(w in text for w in ["想你", "喜欢你", "想你了"]):
            challenges.append(
                f"当前阶段{stage}，直接表达情感可能让对方压力过大。"
                "建议先用轻松话题建立舒适感。"
            )
    if not challenges:
        # Generic alternative for any case
        if len(text) > 30 and any(w in text for w in ["因为", "所以", "但是"]):
            challenges.append(
                "回复中有较多解释性语句，对方可能觉得你在找借口。"
                "更简短直接的表达往往效果更好。"
            )
    return "；".join(challenges) if challenges else None


def _suggest_simpler_alternative(text, stage, flags):
    """Suggest a more direct alternative."""
    if len(text) > 50:
        simpler = text[:25] + "……"
        return f"可以更简洁：「{simpler}」"
    if any(w in text for w in ["其实", "可能", "也许", "应该"]):
        return "使用'其实/可能/也许'等模糊词削弱了立场，直接说想法更好。"
    return None


def _check_overreaction(text, flags, stage):
    """Check if the response overreacts to the situation."""
    overreact_words = ["为什么", "凭什么", "你是不是", "你总是", "你从来"]
    if any(w in text for w in overreact_words):
        return f"使用质问句式'{[w for w in overreact_words if w in text][0]}'容易让对方进入防御状态。"
    if "分手" in text or "结束" in text:
        return "在冲突中使用分手/结束词汇是高风险信号，可能触发不可逆的后果。"
    return None


def _identify_missing_info(ctx):
    """Identify what information is missing that would change the advice."""
    gaps = []
    if not ctx.get("recent_context"):
        gaps.append("无近期对话历史，无法判断互动基线")
    if ctx.get("relationship_stage") in ("陌生", "认识"):
        gaps.append("关系阶段尚浅，对方偏好未知，建议先收集更多信息")
    if not ctx.get("observed_facts"):
        gaps.append("无观察事实，仅凭推测做决策风险高")
    return "；".join(gaps) if gaps else None


def _check_pattern_repeat(text, ctx):
    """Check if this response repeats a problematic pattern."""
    recent = ctx.get("recent_sent_texts", [])
    if text in recent:
        return "此回复与上一句高度相似，重复发送会显得缺乏诚意。"
    # Check for escalating patterns
    escalation_words = ["最后一次", "我再说一遍", "你最好", "别逼我"]
    if any(w in text for w in escalation_words):
        return "使用威胁/最后通牒式语言，可能加速关系恶化。"
    return None


def _summarize_counters(counters):
    """Generate human-readable summary."""
    if not counters:
        return "无重大反对意见，回复可通过。"
    parts = []
    for c in counters:
        sev = "🔴" if c["severity"] == "high" else "🟡" if c["severity"] == "medium" else "🟢"
        parts.append(f"{sev} {c['angle']}: {c['challenge']}")
    critical = sum(1 for c in counters if c.get("requires_fix"))
    return f"发现{len(counters)}个反方论点（{critical}个需修复）：\n" + "\n".join(parts)

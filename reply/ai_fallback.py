"""AI reasoning fallback — when no template candidate matches the situation.

This module is called when generate_candidates() returns an empty list or when
the user's situation doesn't match any known intent. It uses the LLM to
generate a fresh, context-aware response based on the full pipeline state.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from llm.provider import load_provider, LLMUnavailable


def ai_fallback_reason(ctx: dict, model_name: str = "") -> dict:
    """Generate a fresh AI reasoning when no template matches.

    Returns a dict with:
      - reason: str — the AI's reasoning chain
      - reply: str — the suggested reply text
      - intent: str — inferred reply intent
      - confidence: float — 0-1 confidence score
      - evidence: list[str] — supporting evidence
      - alternatives: list[str] — alternative readings
      - risk: float — 0-1 risk score
    """
    llm_cfg = ctx.get("llm_config") or {}
    language = llm_cfg.get("language", "zh")
    lang_map = {
        "zh": "中文", "en": "English", "ja": "日本語", "ko": "한국어",
        "es": "Español", "fr": "Français", "de": "Deutsch",
        "vi": "Tiếng Việt", "id": "Bahasa Indonesia", "th": "ภาษาไทย",
    }
    lang_name = lang_map.get(language, "中文")

    stage = ctx.get("relationship_stage", "认识")
    flags = ctx.get("relationship_dynamics", {}).get("flags", [])
    person = (ctx.get("person") or {}).get("name", "")
    facts = ctx.get("observed_facts", [])
    recent = ctx.get("recent_context", "")
    emo = ctx.get("emotional_state", {}).get("primary", "平静")

    system_prompt = (
        f"你是一个{lang_name}恋爱关系AI推理引擎。"
        f"当模板回复无法覆盖当前情境时，你需要基于以下信息进行全新推理。"
        f"请严格按照JSON格式输出，不要添加任何额外文本。\n\n"
        f"【关系阶段】{stage}\n"
        f"【当前标志】{flags}\n"
        f"【对方情绪】{emo}\n"
        f"【观察事实】{facts}\n"
        f"【近期对话】{recent}\n"
        f"【用户目标】{ctx.get('user_goal', '寻求建议')}\n\n"
        f"输出要求：\n"
        f'1. reason: 你的推理过程（2-3句话）\n'
        f'2. reply: 建议的回复文本（自然口语化，不超过50字）\n'
        f'3. intent: 回复意图（continue/comfort/invite/de-escalate/graceful_exit/suggest_only/no_send）\n'
        f'4. confidence: 置信度0-1\n'
        f'5. evidence: 支持你结论的证据列表\n'
        f'6. alternatives: 至少1个替代解释\n'
        f'7. risk: 风险评分0-1\n'
        f"禁止：AI腔、过度解读、把猜测当事实、操控性语言"
    )

    try:
        provider, llm_cfg = load_provider(llm_cfg)
        result = provider.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请分析并给出建议：{ctx.get('current_message', '')}"}
        ])
        # Try to parse as JSON
        try:
            parsed = json.loads(result.strip())
        except json.JSONDecodeError:
            # If not valid JSON, wrap it
            parsed = {
                "reason": result.strip(),
                "reply": result.strip(),
                "intent": "suggest_only",
                "confidence": 0.5,
                "evidence": [],
                "alternatives": ["需人工审核此推理结果"],
                "risk": 0.3,
            }
        return parsed
    except LLMUnavailable:
        return {
            "reason": "LLM服务不可用，无法生成AI推理回复。建议检查API配置。",
            "reply": "抱歉，我需要联网才能帮你分析。请稍后再试。",
            "intent": "suggest_only",
            "confidence": 0.1,
            "evidence": [],
            "alternatives": ["LLM unavailable"],
            "risk": 0.9,
        }
    except Exception as e:
        return {
            "reason": f"AI推理失败：{str(e)[:100]}",
            "reply": "分析出了点问题，请稍后再试。",
            "intent": "suggest_only",
            "confidence": 0.1,
            "evidence": [],
            "alternatives": [f"Error: {type(e).__name__}"],
            "risk": 0.9,
        }

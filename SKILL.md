---
name: love-agent
description: "统一 AI 恋爱军师 + 微信自动回复 Skill：关系决策、心理学分析（证据分级）、中文聊天话术、对方反应模拟、回复 Critic、人物长期记忆与微信执行闭环。用于分析聊天/截图/语音/图片、判断关系阶段、生成可直接发送的中文回复、模拟对方反应、决定要不要回/何时回，以及在建议/确认/自动驾驶三种模式下通过微信 Adapter 发送。触发：恋爱、暧昧、追求、相亲、约会、冷淡、已读不回、吵架、吃醋、道歉、分手、复合、婚姻、怎么回、她/他什么意思、微信自动回复。"
version: "0.1.0"
---

# love-agent — AI 恋爱军师 + 微信自动回复

## 定位：不是话术生成器

这是一个闭环系统：Observe → Remember → Interpret → Estimate → Strategize → Generate → Simulate → Critique → Revise → Decide whether to send → Send → Observe reaction → Update memory。

心理学层只负责理解，不直接写最终聊天文本。核心判断由统一 LLM Provider 完成（llm/：interpret→stage→strategize→generate→simulate→critic→revise，OpenAI-compatible，Mock 供 CI）；关键词规则只是 fast pre-classifier、安全门与 LLM 不可用时的 fallback，不得冒充最终智能。KnowledgeBase 的 Tier 条目与人物 Memory 必须实际进入 LLM prompt（可由 llm_prompt_audit 核查）。

## 三种模式（默认建议模式）

- MODE 1 suggest（建议）：分析+建议，用户自己发。
- MODE 2 confirm（确认）：生成回复，用户确认后才通过 Adapter 发送。
- MODE 3 autopilot（自动驾驶）：仅当 confidence >= config.autopilot_min_confidence（默认 0.85）、risk 低、且非敏感主题时自动发送；0.60–0.85 降级确认；<0.60 不自动回复。

敏感主题默认禁止自动发送，必须确认：分手、复合、金钱/借钱/转账、性相关重大决定、婚姻、重大承诺、明显冲突、威胁、法律、自伤/家暴风险。

## 每次运行的固定流水线

1. Observe：区分文字/表情/图片/截图/语音/视频/文件/链接/沉默。图片走 Vision、语音走 ASR、视频抽帧+Vision、截图走 speaker-aware OCR（低置信发言人不硬判）。
2. Remember：先读 `memory/people/<person_id>/` 五件套（profile/preferences/relationship/important_events/conversation_summary）。Tier D 个人数据优先级最高。
3. Interpret：严格区分 `observed_facts`（实际发生）与 `possible_interpretations`（带 confidence 的假设）。禁止「她这样就是吃醋」式断言；只能写「可能存在吃醋/失望解释，证据支持度 0.58」。
4. Estimate stage：输出 stage + confidence + alternative_stages，不强行分类。阶段枚举：陌生/认识/普通朋友/熟人/暧昧/追求/恋爱/稳定恋爱/冲突/冷淡/分手/复合期/婚姻。
5. Strategize：先定战略（推进/降温/修复/给空间/体面退出/等待），再定 reply_intent 与 tone，并列 things_to_avoid。
6. Retrieve knowledge（按需，不全量加载）：Tier A 科学证据只用于理解机制；Tier B 成熟实践用于沟通方法；Tier C 实战经验只用于「怎么说」，不得包装成科学事实；Tier D 个人记忆优先。
7. Generate：生成自然中文候选。普通闲聊可只给最终一条；需要权衡时给 A 自然型/B 轻松型/C 暧昧型；敏感场景只给低风险/稳妥。禁止 AI 腔、咨询报告腔、长篇、油腻情话、阶段不匹配的热情。
8. Simulate：对每条候选预测对方可能理解、压力、敷衍感、兴趣、继续聊天意愿与可能回复，给 risk。
9. Critique：过 12 项检查（过度解读、猜测当事实、阶段匹配、舔/需求感、冷漠、压力、操控、用户意图、重复、记忆冲突、AI 腔、是否必要回复）。允许结论「建议不要回复」。
10. Revise & Decide：修正后按模式与阈值决定 suggest_only / needs_confirmation / auto_send / no_send。
11. Send（仅确认或 autopilot 达标）：走 `adapters/wechat/`。默认 Mock/dry-run；生产用 LearnLove 路线（见 adapters/wechat/README.md）。
12. Update memory：只把 observed_facts 与已发送文本写回人物档案；猜测不得静默变事实。判断改变时记录新证据。

## 统一中间数据结构

输出必须是可 JSON 序列化的 UnifiedContext（见 `love_agent/schema.py` 与 docs/ARCHITECTURE.md）：person、relationship_stage、stage_confidence、alternative_stages、recent_context、current_message、observed_facts、possible_interpretations[{hypothesis,confidence,evidence}]、confidence、emotional_state、relationship_dynamics、user_goal、recommended_strategy、reply_intent、tone、things_to_avoid、candidate_replies、simulated_reactions、critic_results、final_reply、should_send、send_decision、decision_reason、knowledge_used、memory_updates、multimodal。

## 路由：什么时候读哪层知识

- 关系机制/为什么：`brain/psychology/` + `knowledge/psychology/`（Tier A/B）
- 阶段/信号/投入：`brain/relationship/` + LoveHelper 式 10 维证据（Tier B/C）
- 下一步战略：`brain/strategy/`（Tier B/C）
- 具体怎么说：`knowledge/scripts/`、`knowledge/cases/`、`knowledge/tactics/`（Tier C）
- 操控/PUA 识别：`brain/goutoujunshi/manipulation-and-ethics.md`，只给伦理替代，不给操控实施。
- 证据纪律：`brain/evidence/evidence-first.md`（借鉴 analyze-romantic-relationships：evidence → inference → uncertainty）
- 对方模拟：`reply/simulator.py`（借鉴 HeartFlow 人物卡：interaction/affection/boundaries/signal patterns，但不做沉浸式角色扮演替代真人）

## 微信与多模态边界

- 微信生产路线以 LearnLove 为底座：Windows 微信 DB 解密 → 规范化解析 → 2 秒轮询监听 → 媒体归档 → 发送阀门 L0/L1/L2。无 Windows 微信环境时只能 Mock/dry-run，不得声称已真实发送。
- 语音未转写、图片未识别时，必须标注待处理，禁止假装听见/看见。
- 不保存整份聊天无限累积；按人物压缩摘要 + 重要事件 + 有效/无效回复经验。

## 安全与诚实边界

- 不诊断心理疾病，不保证话术让某人爱上用户。
- 明确拒绝/要求停止联系后停止推进，给体面退出。
- 不协助胁迫、跟踪、偷拍、诈骗、性施压、制造嫉妒操控。
- 出现自伤、家暴、威胁时先安全与求助，不进入话术流程。

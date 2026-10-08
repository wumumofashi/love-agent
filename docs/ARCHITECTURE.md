# love-agent 统一架构

```text
微信消息 → adapters/wechat (receive/parse/OCR/ASR/Vision)
→ Observe (unified message) → Remember (memory/people/<id> Tier D)
→ Interpret (facts vs interpretations+confidence, psychology Tier A/B)
→ Estimate stage (stage+confidence+alternatives)
→ Strategize (brain/strategy + Tier B/C)
→ Reply planner (intent/tone/avoid)
→ Generator (knowledge/scripts Tier C, Chinese natural)
→ Simulator (HeartFlow-like person model, risk/interest)
→ Critic (12 checks) → Revise
→ Decide (suggest / confirm / autopilot thresholds + sensitive block)
→ Send (WeChat adapter, valve) → Observe reaction → Update memory
```

目录：SKILL.md 只做流程与路由；brain/ 是推理层；knowledge/ 是分级知识（A 心理学、B 实践、C 实战、D 在 memory/）；reply/ 是生成闭环；multimodal/ 是 provider 接口；adapters/wechat/ 是执行层；config/ 是阈值与敏感词；tests/ 是 20+ 场景。

中间结构见 love_agent/schema.py 的 empty_context()。所有推断带 confidence，所有发送带 decision_reason。

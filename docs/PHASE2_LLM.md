# 第二阶段：LLM 化改造报告

## 现在仍然是规则的部分（如实）
- Observe 的消息类型识别、微信类型码解析
- Fast pre-classifier（COLD/PASSIVE 等关键词）只作预分类与安全信号，不再是最终判断
- Rule Critic 12 项、敏感主题拦截、三种模式、置信阈值 Decision Gate
- LLM 不可用/未配置时的 fallback 规则链（会明确标 `llm_provider_used=rules_fallback`）
- Mock LLM 本质是确定性语义模拟器，仅供 CI，不是真模型

## 已经进入 LLM 的部分
Interpret、Stage Estimator、Strategist、Reply Generator、Counterpart Simulator、LLM Critic、Revision 全部走统一 Provider 的 `complete_json(task,...)`，任务顺序由 tests/test_llm_pipeline.py 校验。真实 Provider 为 `llm/openai_compatible.py`（OpenAI-compatible /chat/completions，JSON 模式，密钥只读环境变量）。

## KnowledgeBase 是否进 prompt：是
每次 LLM 调用 payload 带 `knowledge_tiered` 与 `knowledge_prompt_block`（含 Tier 标签與来源路径），测试断言 prompt audit 中含 Tier 与条目。Tier C 只作 examples，prompt 中有 tier_rule 明示。

## Memory 是否进 prompt：是
payload 带完整 person 与 person_memory（profile/preferences/relationship/interaction_patterns/relationship_events）。测试用偏好“喜欢先说结论”断言其出现在 prompt audit 中。长期写入仍只限 observed facts 与用户确认的 outcome（effective/negative），推测不写。

## Simulator 是否用人物信息：是
Mock/真实 prompt 都带 person profile、preferences、boundaries 与近期上下文；同一句“你今天怎么没找我”对高频/独立/回避冲突/要空间四种人物产生不同 simulation 与回复，测试已断言至少 3 种差异。模拟输出带 uncertainty，明示非真实预测。

## Critic 是否用上下文：是
Rule Critic + LLM Critic 并行，LLM Critic 输入 candidate+simulation+人物/历史 payload；不通过则 Revision，最多 3 次（测试用注入的高压候选验证触发、修正与上限）。

## 配置真实 LLM 需要的环境变量
`LOVE_AGENT_API_KEY`（必需）、`LOVE_AGENT_BASE_URL`、`LOVE_AGENT_MODEL`、`LOVE_AGENT_LLM_PROVIDER=openai_compatible`（或改 config/model.json 的 provider）。仓库不存任何 key。未配置时系统用 mock 并明确标注，不会假装真模型在跑。

## 真实微信状态
仍未接通真实发送：需用户 Windows 微信 + LearnLove 环境。当前 Adapter 为 Mock/LearnLove 接口与阀门设计。

# love-agent

统一的「AI 恋爱军师 + 微信自动回复 Skill」：关系决策 + 对话策略 + 回复生成 + 对方模拟 + 长期记忆 + 微信执行。

- 研究依据：实际克隆并读取 12 个 GitHub 项目，横向比较见 `docs/RESEARCH_COMPARISON.md`，复用判断见 `docs/REUSE_ASSESSMENT.md`。
- 核心代码：`love_agent/engine.py`（闭环）、`reply/`（planner/generator/simulator/critic）、`love_agent/memory.py`、`adapters/wechat/`。
- 运行演示：`python3 scripts/demo.py`
- 跑测试：`python3 tests/run_tests.py`（24 个场景，无第三方依赖）
- 安装为 Skill：把本目录复制到你的 skills 目录，确保根目录有 SKILL.md。真实微信发送需在 Windows 上另装 LearnLove，见 `docs/INSTALL_RUN.md`。

当前状态：在 Linux 上可运行分析、生成、模拟、Critic、决策与 Mock 发送；真实微信收发未在本机接通（需要用户 Windows 微信环境）。

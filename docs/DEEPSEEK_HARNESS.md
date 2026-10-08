# DeepSeek Harness 验证指南

## 拉取
```bash
git clone https://github.com/wumumofashi/love-agent.git
cd love-agent
```
如仓库为 private，harness 需用仓库所有者的 GitHub 凭据拉取（PAT 或已登录的 gh）。

## 一键验证（无第三方依赖，Python 3.10+）
```bash
python3 tests/run_tests.py
```
期望最后一行：`TOTAL 24 passed, 0 failed, 24 scenarios`

## 演示
```bash
python3 scripts/demo.py
```
输出结构化 JSON：关系阶段、事实/推测分离、策略、最终回复、置信度与发送决策。

## 重点核查点
- possible_interpretations 每条带 confidence，不把猜测写成事实
- 分手/复合/借钱/冲突在 autopilot 下 send_decision=needs_confirmation
- 突然不回复场景 final_reply 为空且 send_decision=no_send
- 图片场景回复引用具体细节，不只说“好漂亮”
- 语音未转写时明确表示没听清，不编造内容

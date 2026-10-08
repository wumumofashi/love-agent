# 安装与运行

## 1. 离线分析与测试（当前即可）
```bash
cd ~/workspace/love-agent
python3 tests/run_tests.py
python3 scripts/demo.py
```
无第三方依赖，Python 3.10+。

## 2. 作为 Skill 安装
把 `love-agent/` 整目录复制到 Agent 的 skills 目录（根目录含 SKILL.md）。SKILL.md 负责路由，具体知识按需读 brain/ 与 knowledge/。

## 3. 接入真实微信（生产，需 Windows）
1. 在用户 Windows 电脑安装 LearnLove（jx-2-a/LearnLove），按其 README 解密微信 DB、配置 ~/.learnlove_data/config.yaml 与联系人。
2. 先 valve=1 跑建议模式，核对解析与记忆无误。
3. 确认模式：love-agent 生成 → 用户确认 → Adapter 以 L2 单次发送。
4. 自动驾驶：仅低风险日常场景开启，阈值在 config/default.json；敏感主题永远拦截确认。

## 4. 多模态 Provider
语音：LearnLove SenseVoice/Whisper；图片：Qwen2.5-VL 或远程 Vision；截图 OCR：LoveHelper speaker-aware OCR。未配置 provider 时系统只标注待处理，不编造内容。

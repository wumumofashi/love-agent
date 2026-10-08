# 视觉传输层（融合 WeChat-AI-AutoReply）

主力微信路线：视觉收发当「手」，love-agent 引擎当「脑」。

- 传输：`wechat_vision_bot.py`（源自 Luofeng-Cloud/WeChat-AI-AutoReply，MIT，见 NOTICE.md）——PrintWindow 截图 + RapidOCR 识别 + Win32 PostMessage 发送，鼠标零移动，支持 Windows 微信 3.x/4.x。
- 大脑：`love_agent_bridge.py`——对方消息经 love-agent 引擎（解读→阶段→战略→生成/语句库→模拟→Critic→决策）后才决定发不发。
- 模式：suggest/confirm 永不发送（建议写 outbox 供客户看）；autopilot 仅 auto_send 才发；且 `loveagent.live` 默认 false（dry-run），客户 explicit 改 true 才真发。敏感话题（分手/要钱/自杀等）永远拦。

## 客户机运行（Windows）

1. 微信登录（3.x 或 4.x 均可），保持窗口可被 PrintWindow 捕获（可离屏收纳，见上游说明）。
2. 安装依赖：`pip install rapidocr-onnxruntime pillow numpy psutil pyperclip requests`
3. 把 `wechat_config.loveagent.example.json` 复制为传输脚本同目录的 `wechat_config_dev.json`，把白名单和 `loveagent.chats` 改成客户的对象/模式/人设/阶段。
4. 先以 confirm 模式 + live=false 运行 `python adapters/wechat/vision/wechat_vision_bot.py`，在 outbox 里验收建议质量。
5. 验收后再把对应聊天 mode 改为 autopilot、live 改 true。

## 已知边界

- 感知靠截图 OCR：微信改版/DPI/主题变化可能影响识别，需要现场回归。
- 语音/图片消息在这一层只能被 OCR 看到气泡形态，内容理解走 love-agent 多模态路由（需另行转写/描述），未转写时引擎不会假装听见。
- 上游项目年轻（2026-09 建仓），此 vendored 副本由本项目自行维护。

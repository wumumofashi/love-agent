# WeChat Adapter 设计与 LearnLove 复用结论

## 结论：生产路线复用 LearnLove 架构，不在 Linux 上假装已接通真微信

已读 `jx-2-a/LearnLove` 源码（2026-10-08 克隆）：
- 接收：Windows 微信本地 DB（`wechat-decrypt` 提 key）→ DBCache 解密 → `agent/tools/monitor.py` 每 ~2 秒轮询 → `agent/wechat_parser.py:normalize_message()` 输出统一事实对象。
- 解析类型：1 文本、3 图片、34 语音、42 名片、43 视频、47 表情、48 位置、49 应用消息（链接/文件/引用/转账/红包）、50 通话、10000 系统、10002 撤回。
- 媒体：语音从 media_0.db 归档 SILK → SenseVoice/Whisper；图片 .dat 归档 → Qwen2.5-VL/远程 Vision；模型注册表 `agent/media_models.json`。
- 记忆：`agent/memory.py` 每联系人 transcript.jsonl + 五段 memory.md；全局记忆单独注入，不混人物档案。
- 发送：`agent/tools/send.py` 剪贴板（L1）或 pyautogui 自动发送（L2：激活微信、Ctrl+F 搜联系人、粘贴、Enter）；`agent/valve.py` L0 只读 / L1 建议 / L2 发送。
- 技能插件：内置狗头军师知识库（LearnLove 的 skills/goutoujunshi 与上游 goutoujunshi 同源）。

## 本项目 Adapter 接口

`adapter.py` 提供 `WeChatMessage`、`MockWeChatAdapter`（测试/演示，dry-run）、`LearnLoveWeChatAdapter`（生产接口，valve<2 禁止发送）。

映射：love-agent MODE1→L1 建议，MODE2→L1+用户确认后 L2 单次发送，MODE3→L2 但仍受敏感主题与置信阈值拦截。

## 安装前提（真实发送）

必须在用户 Windows 电脑：微信已登录、LearnLove 已解密 DB、配置 `~/.learnlove_data/config.yaml`、valve 设置、联系人 wxid 指定。本仓库在当前 Linux VM 只能做到 Mock 与接口验证，未真实发送。

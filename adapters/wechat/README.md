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

## 2026-10-09 更新：生产传输层改选 wxauto（对接完成）

调研结论（GitHub 实测，2026-10-09 更正）：**cluic/wxauto**（约 7.4k stars，Apache-2.0）代码已于 2026 年 2 月停止维护（最后代码提交为「停止维护」，之后只有 README 修改；wxauto4 也已停更）——此前「2026 年仍在推送」的说法是被仓库元数据误导，特此更正。它目前仍可驱动微信客户端，但微信改版后可能无人修复；真正持续维护的是 **CowAgent**（47k stars，MIT，2026-10-08 仍有 weixin 渠道代码提交）。wxauto 在此保留为可用的冻结传输层，主力路线建议改走 CowAgent 集成，待用户拍板。，直接驱动 Windows 微信客户端收发，不碰网页协议、不需要解密数据库，客户侧部署最轻。Wechaty（23k stars）依赖 puppet（padlocal 等）收费且不稳；CowAgent（47k stars，前 chatgpt-on-wechat）是整套 Agent 框架而非传输层，接进来会喧宾夺主；LearnLove 的 DB 路线保留为重型备选。

已对接：
- `wxauto_adapter.py`：`WxAutoWeChatAdapter`（receive 归一化、listen、send、monitor），非 Windows 或未装 wxauto 时明确报错，不假装接通。
- `runner.py`：客户机运行入口。监听指定聊天 → 引擎决策 → suggest/confirm 永不发送只写 outbox；autopilot 仅当决策为 auto_send 才发送，且真实发送必须显式加 `--live`，默认 dry-run。
- `scripts/wechat_env_check.py`：第 1 步环境检查，只报事实。

客户机安装：`pip install wxauto`（微信 3.x）或 `pip install wxauto4`（微信 4.x），微信登录后运行 runner。

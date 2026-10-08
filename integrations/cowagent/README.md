> **定位更正（2026-10-09）**：CowAgent 的 weixin 渠道走 ilink bot 协议，登录的是一个机器人身份，消息是别人（主要是客户本人）和这个机器人之间的对话——性质是「AI 助理工作台」，和豆包+飞书/微信同类。它**不能**读取或回复客户个人微信里与某位联系人的对话，因此不适合本技能的主产品形态（在客户本人微信里回复对方）。本集成保留，适用于把 love-agent 做成「咨询机器人」的场景；主产品请走 wxauto 路线（adapters/wechat/runner.py，可 vendor 源码自维护）。

# love-agent × CowAgent 集成（主力微信路线）

选用原因（2026-10-09 核实）：CowAgent（zhayujie/CowAgent，约 4.7 万 stars，MIT）是同类里真正在持续维护的项目——2026-10-08 当天仍有 weixin 渠道的代码提交。wxauto 已于 2026 年 2 月停止维护（仓库内保留为冻结备选），WeChatFerry 已归档。

## 形态

CowAgent 当运行底座（微信收发、渠道、登录），love-agent 当大脑（解读→阶段→战略→生成→模拟→Critic→决策），通过 CowAgent 插件机制对接：

- `plugin/love_agent/love_agent.py`：插件本体（priority 950），只处理 config 里指定的单聊；其余聊天仍走 CowAgent 默认大脑。
- suggest / confirm：**绝不向对方发送**，建议写进 outbox jsonl，客户自己看、自己发。
- autopilot：仅当引擎决策为 auto_send（confidence 与 risk 双门通过且非敏感话题）才把 final_reply 交给 CowAgent 发送；分手、要钱、自杀等敏感话题永远不自动发送。
- 人物记忆、阶段、人设都在 love-agent 侧按 person_id 隔离；CowAgent 不另存一份。

## 在客户 Windows 机器上部署

1. 安装 CowAgent（按其官方文档），在 CowAgent 的 `config.json` 里设置 `"channel_type": "weixin"` 并完成微信登录。
2. 把 love-agent 技能放到任意目录（即本仓库）。
3. 安装插件并写入这个客户/对象的配置：

```bat
python integrations\cowagent\install.py --cowagent D:\CowAgent --chat "对方备注名" --person-id person_001 --mode confirm --persona "幽默、直接、不卑不亢" --stage 暧昧
```

4. 启动 CowAgent，先用 confirm 模式跑：对方来消息时，对方不会收到任何东西；建议出现在 CowAgent 目录的 `love_agent_outbox.jsonl` 和运行日志里。
5. 确认建议质量后，再把该聊天的 mode 改成 autopilot。改 config 后重启 CowAgent 生效。

## 边界

- 本集成已用 CowAgent 真实插件 API 写成（plugins.register / ON_HANDLE_CONTEXT / EventAction），并在本仓库用模拟 EventContext 验证三种模式与敏感拦截；真实微信收发仍需在客户 Windows + CowAgent + 微信登录环境联调。
- CowAgent 的 weixin 渠道为协议路线，封号风险与任何第三方微信自动化一样存在；建议新号先小流量跑 confirm 模式。
- wxauto 路线（`adapters/wechat/runner.py`）保留为冻结备选：能用，但上游不再修。

# 复用 / 不复用清单

## 直接复用（设计或接口层）
- LearnLove：微信 DB 规范化消息对象、monitor 轮询、media 归档、valve L0/L1/L2、send 两段式（剪贴板/自动）。本项目 Adapter 按其接口实现，生产部署直接装 LearnLove。
- LoveHelper score_stage.py 思路：10 维打分、阶段门槛、信号家族封顶、风险覆盖。本项目 stage-model 借鉴，未复制其前台话术标签。
- LoveHelper wechat_ocr.py 思路：bbox+头像同水平带判发言人，低置信不硬判。作为 OCR provider 规范。
- HeartFlow relationship-card 字段：interaction_style、affection_style、boundaries、signal_patterns、progress/risk triggers、sample_lines。用于 Simulator 的人物模型输入。
- analyze-romantic-relationships validator 字段纪律：observable_actions、risk_flags、consent/deidentified。用于 case 与 memory 写入标准。

## 蒸馏复用（归纳改写，标注 Tier 与来源，不整包复制）
- 狗头军师：情绪落地→事实拆分→利益判断→明确建议；证据分级；PUA 伦理替代；长期记忆同意/撤销。MIT，可引用，但本项目只做归纳以免上下文臃肿。
- Love-Skill：11 框架路由表。只做理解层路由，不让它生成最终文本。其 SKILL 含 EvoMap 网络进化与 personality_state 等与本任务无关机制，不采用。
- LoveLab：四骑士、依恋双维度、NVC 四格、认知扭曲清单、中文文化校准与危机提示。分析维度采用，报告体不采用。
- 情圣/guanxi/浩威/dating/smart-reply：中文短句原则、场景意图表、冷场重启、邀约与冲突话术模式。只蒸馏模式到 generator，不复制案例原文与人设口吻。浩威为非商用许可，尤其只借场景分类，不复制金句库。

## 不能直接复用及原因
- 把任一上游 SKILL.md 整包塞入：会互相冲突（咨询腔 vs 兄弟腔 vs 模拟器）、上下文爆炸、阶段定义不一致。
- HeartFlow 沉浸模拟：会把预测当真人，且不支持复合，与本项目证据纪律冲突。
- 情圣 autopilot 直接发送：它只是对话树文本，无真实微信发送与置信门控；本项目加了阈值、敏感拦截与 Critic。
- 微信协议类重写：风险高且 LearnLove 已验证 DB 路线；本项目不在 Linux 重写。
- 上游仓库的性别预设/推进话术：必须经 Critic 的阶段、压力、操控检查后才能用。

## 许可证注意
MIT：goutoujunshi、LoveHelper、analyze-romantic-relationships、heartflow、lovelab、qingsheng。浩威：Personal and non-commercial。LearnLove、love-skill、dating-chat-helper、smart-reply、guanxi-skills 仓库根未见 LICENSE 文件，按只研究不复制代码处理。最终项目代码为本项目新写。

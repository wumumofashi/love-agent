# GitHub 横向研究（实际克隆读取，2026-10-08）

克隆目录：`~/workspace/research/love-repos/`，12 个仓库全部 git clone --depth 1 成功，无失效仓库。

| 项目 | 心理学 | 恋爱策略 | 中文话术 | 对方模拟 | 长期记忆 | 微信自动化 |
|---|---|---|---|---|---|---|
| 狗头军师 goutoujunshi | 强（20 篇知识：依恋/MBTI/PUA伦理/婚姻/法律） | 强 | 强（实战话术编排器等 23 篇 practical） | 弱（靠信号判断，无模拟器） | 有协议（同意/撤销/压缩档案） | 无（明确不导出微信数据） |
| Love-Skill | 最强（11 frameworks + 4 protocols：Attachment/Gottman/CBT/NVC/EFT/DBT/IFS/Imago/Polyvagal 等） | 中（咨询式） | 弱（偏咨询报告） | 中（双视角分析） | 弱（进化日志非人物档案） | 无 |
| 情圣 qingsheng-skill | 中 | 强（七阶段、信号工具） | 最强（40 案例、平台指南、自动驾驶对话树） | 弱 | 有（user-profile + targets） | 无真实发送（autopilot 是文本对话树） |
| LoveHelper | 中 | 强（阶段评估 10 维打分脚本 score_stage.py） | 强（copilot 可直接发的话） | 弱 | 中 | 半（wechat-chat-ocr speaker-aware OCR） |
| dating-chat-helper | 弱 | 中 | 中强（2-3 风格，场景库） | 无 | 无 | 无 |
| smart-reply | 中（潜台词/PUA 识别） | 中 | 强（去 AI 味、多语气） | 弱 | 无 | 无（明确不自动发送） |
| guanxi-skills | 中 | 强（追求到婚姻全阶段 references） | 强 | 无 | 有 handoff JSON | 无 |
| 浩威关系 | 弱（内核力，非临床心理） | 强（场景→回复、金句 atoms） | 强 | 弱 | 有（本地存档/读档） | 无 |
| HeartFlow | 弱 | 中 | 中 | 最强方向（人物卡 interaction/affection/boundaries/signal/sample） | 有（relationships/<slug> 人物卡+corrections） | 半（social_chat_import 导入） |
| LoveLab | 强（Gottman/Attachment/NVC/CBT 多维仪表盘+中文校准） | 弱（分析仪） | 弱（给改写示例） | 弱 | 无 | 无 |
| analyze-romantic-relationships | 中（证据纪律最强） | 中 | 弱 | 无 | 案例 JSON validator | 无 |
| LearnLove | 中（内置狗头军师 43 篇） | 强 | 强（短句真人风） | 弱 | 最强工程（每联系人 transcript+压缩五段记忆） | 最强（DB解密/2秒监听/语音图片/剪贴板+pyautogui 发送/阀门） |

## 判断

- Love-Skill 是关系理解/心理学推理引擎，不是直接聊天回复器。让它写最终话术会咨询腔、长篇、慢。正确位置：Interpret/Strategize 的理解层。
- 狗头军师是最均衡的军师框架：情绪-事实-利益-建议、证据边界、操控伦理、话术编排。适合做战略与 Tier C 知识骨架。
- 情圣的中文微信语感、阶段与 autopilot 对话树最贴实战，但默认男性追求视角与部分推进话术需经 Critic 与阶段门槛过滤。
- LoveHelper 的阶段打分脚本是唯一确定性阶段工具，值得借鉴 10 维与门槛/封顶逻辑。
- HeartFlow 唯一认真做对方人物模型，但目标是沉浸式恋爱模拟（明确不支持复合），只能借人物卡字段做 Simulator，不能让它替代真人或保证预测。
- analyze-romantic-relationships 规模小但纪律最好：evidence→inference→uncertainty、案例 validator、防读心。做全系统的证据宪法。
- LearnLove 是唯一完整可运行的微信工程：DB、监听、媒体、记忆、阀门、发送全有。生产 Adapter 应寄生它，而不是重写微信协议。

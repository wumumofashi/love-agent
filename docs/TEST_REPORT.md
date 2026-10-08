# 测试报告（2026-10-08 本机实跑）

命令：`python3 tests/run_tests.py` 结果：24 passed, 0 failed。

覆盖：普通聊天、冷淡、突然不回复（正确 no_send）、暧昧、主动示好、拒绝、约会、吵架、误会、吃醋、道歉、分手、复合、朋友、相亲、长期恋爱、图片自拍、语音、视频、阴阳怪气、金钱禁止自动发、禁止过度解读、语音未转写不假装听见、人物记忆加载。

每个场景的通用断言：有 observed_facts、有带 confidence 的 possible_interpretations、有 simulator 输出、有 12 项 critic 检查、敏感场景 should_send=false。

未验证：真实微信发送（需 Windows 微信 + LearnLove 环境）、真实 Vision/ASR 模型效果（当前为 provider 接口 + 已识别输入透传）。完整逐条输出见 tests/last_run.txt。

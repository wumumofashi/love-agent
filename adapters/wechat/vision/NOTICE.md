# NOTICE — vendored third-party code

The vision transport in this directory (`wechat_vision_bot.py`) is derived from:

- Project: Luofeng-Cloud/WeChat-AI-AutoReply
- URL: https://github.com/Luofeng-Cloud/WeChat-AI-AutoReply
- License: MIT (full text in `LICENSE.upstream`, copyright held by its authors)
- Retrieved: 2026-10-09 (main branch, v1.0.1 era)

Modifications by this project: the upstream single-prompt reply generator was
replaced with `love_agent_bridge.decide_reply` (love-agent engine, three modes,
sensitive-topic gates, outbox audit log), and its built-in fallback reply text
was removed. All other transport code (window capture, OCR perception, Win32
message sending, whitelist gating) is upstream work; maintenance of this copy
is ours.

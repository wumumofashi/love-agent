from __future__ import annotations
def describe_image(payload: dict) -> dict:
    # Provider plug point: LearnLove uses Qwen2.5-VL local or remote API. Offline default never invents details.
    if payload.get("description"): return {"kind":"image","description":payload["description"],"observed_facts":[f"对方发送了一张图片：{payload['description']}"],"confidence":0.7}
    return {"kind":"image","description":"","observed_facts":["对方发送了一张图片（尚未识别内容）"],"confidence":0.2,"needs_vision_provider":True}

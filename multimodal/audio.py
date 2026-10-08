from __future__ import annotations
def transcribe_voice(payload: dict) -> dict:
    # LearnLove: SILK -> WAV -> SenseVoice/Whisper. Offline default requires transcript, does not hallucinate.
    if payload.get("transcript"): return {"kind":"voice","transcript":payload["transcript"],"observed_facts":[f"对方发送语音，转写：{payload['transcript']}"],"confidence":0.75}
    return {"kind":"voice","transcript":"","observed_facts":["对方发送了一条语音（尚未转写）"],"confidence":0.2,"needs_asr_provider":True}
def video_frames(payload: dict) -> dict:
    if payload.get("description"): return {"kind":"video","description":payload["description"],"observed_facts":[f"对方发送视频：{payload['description']}"],"confidence":0.65}
    return {"kind":"video","description":"","observed_facts":["对方发送了一段视频（尚未抽帧识别）"],"confidence":0.2,"needs_vision_provider":True}

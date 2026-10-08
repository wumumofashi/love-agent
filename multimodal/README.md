# 多模态流水线
文字→NLP；图片→Vision；语音→ASR（SILK→WAV→SenseVoice/Whisper）；视频→抽帧+Vision；链接→内容解析；截图→speaker-aware OCR。未识别内容必须标注待处理。Provider 接口：vision.py / ocr.py / audio.py。

from __future__ import annotations
def ocr_screenshot(payload: dict) -> dict:
    # Reuse assessment: LoveHelper wechat_ocr.py does speaker-aware bbox OCR; integrate as provider, keep low-conf speaker unknown.
    return {"kind":"ocr","text":payload.get("ocr_text",""),"speaker_confidence":payload.get("speaker_confidence",0.0),"note":"speaker must not be guessed when confidence is low"}

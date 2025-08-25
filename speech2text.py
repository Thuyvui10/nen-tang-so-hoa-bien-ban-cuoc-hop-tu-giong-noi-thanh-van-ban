import os
import speech_recognition as sr
from faster_whisper import WhisperModel

# ✅ Load Whisper model 1 lần khi app khởi động
# Nếu có GPU: dùng "cuda" để tăng tốc
DEVICE = "cuda" if os.environ.get("USE_GPU", "0") == "1" else "cpu"
MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")

print(f"🚀 Khởi tạo Whisper model [{MODEL_SIZE}] trên {DEVICE}...")
whisper_model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="float16" if DEVICE=="cuda" else "int8")

def _transcribe_with_whisper(audio_path: str) -> str:
    print(f"🔎 Whisper xử lý file: {audio_path}")
    try:
        segments, info = whisper_model.transcribe(audio_path, language="vi", vad_filter=True)
        text = " ".join([seg.text for seg in segments]).strip()
        print("📃 Whisper:", text[:200])
        return text
    except Exception as e:
        print("❌ Whisper lỗi:", e)
        return ""

def _transcribe_with_google(audio_path: str) -> str:
    print(f"🔎 Google SR xử lý file: {audio_path}")
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language="vi-VN")
        print("📃 Google SR:", text[:200])
        return text
    except Exception as e:
        print("❌ Google SR lỗi:", e)
        return ""

def audio_to_text(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        return "❌ Không tìm thấy file audio"

    text = _transcribe_with_whisper(audio_path)
    if text:
        return text

    print("ℹ️ Whisper thất bại → thử Google SR...")
    text = _transcribe_with_google(audio_path)
    if text:
        return text

    return "❌ Không thể nhận dạng giọng nói"

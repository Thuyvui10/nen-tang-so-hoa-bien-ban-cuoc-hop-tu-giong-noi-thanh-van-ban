from transformers import pipeline

# ✅ Load summarizer 1 lần khi app start
print("🚀 Khởi tạo Summarizer model (VietAI/vit5-base)...")
summarizer = pipeline("summarization", model="VietAI/vit5-base")

def summarize_text(text: str) -> str:
    if not text or len(text.strip()) == 0:
        return "Không có nội dung để tóm tắt."
    try:
        # Nếu text quá dài → cắt nhỏ rồi tóm tắt từng phần
        MAX_CHARS = 1000
        if len(text) > MAX_CHARS:
            parts = [text[i:i+MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]
            summaries = []
            for part in parts:
                s = summarizer(part, max_length=100, min_length=30, do_sample=False)
                summaries.append(s[0]["summary_text"])
            return " ".join(summaries)
        else:
            summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
            return summary[0]["summary_text"]
    except Exception as e:
        return f"Tóm tắt lỗi: {e}"

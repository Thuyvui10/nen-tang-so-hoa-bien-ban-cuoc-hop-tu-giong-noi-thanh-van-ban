import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from modules.speech2text import audio_to_text
from modules.summarize import summarize_text
from modules.export import save_as_docx, save_as_pdf

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ✅ Hàm loại bỏ câu lặp trong summary
def remove_duplicates(summary: str) -> str:
    sentences = summary.split(". ")
    seen = set()
    result = []
    for s in sentences:
        clean = s.strip()
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return ". ".join(result)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Trường hợp upload file
        if "file" in request.files:
            f = request.files["file"]
            if f and f.filename:
                filename = secure_filename(f.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                f.save(filepath)

                # Chuyển thành văn bản
                text = audio_to_text(filepath)
                print("📃 Văn bản thu được:", text)

                # Sinh summary và loại trùng
                summary = summarize_text(text)
                summary = remove_duplicates(summary)

                # Xuất file
                docx_path = save_as_docx(text, summary, filename + ".docx")
                pdf_path = save_as_pdf(text, summary, filename + ".pdf")

                return render_template(
                    "result.html",
                    text=text,
                    summary=summary,
                    docx=url_for("static", filename=docx_path),
                    pdf=url_for("static", filename=pdf_path),
                )
            else:
                return render_template("index.html", error="Chưa chọn file!")

    return render_template("index.html")


@app.route("/record", methods=["POST"])
def record():
    """Nhận audio từ ghi âm trực tiếp"""
    if "audio_data" not in request.files:
        return "Không có audio_data", 400

    f = request.files["audio_data"]
    filename = secure_filename(f.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    f.save(filepath)

    # Chuyển thành văn bản
    text = audio_to_text(filepath)
    print("📃 Văn bản thu được:", text)

    # Sinh summary và loại trùng
    summary = summarize_text(text)
    summary = remove_duplicates(summary)

    # Xuất file
    docx_path = save_as_docx(text, summary, filename + ".docx")
    pdf_path = save_as_pdf(text, summary, filename + ".pdf")

    return render_template(
        "result.html",
        text=text,
        summary=summary,
        docx=url_for("static", filename=docx_path),
        pdf=url_for("static", filename=pdf_path),
    )


if __name__ == "__main__":
    app.run(debug=True)

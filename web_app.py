from flask import Flask, request, jsonify, send_file, render_template
import os
from pdf_processor import replace_highlight_colors_hex
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 颜色映射
COLOR_MAPPING = {
    "#f0ff00": "#FFFBAB",
    "#00b036": "#CDE7B4",
    "#00f0ff": "#C2EBFF"
}

@app.route("/")
def index():
    """返回 HTML 界面"""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """上传 PDF 文件并进行颜色替换"""
    if "file" not in request.files:
        return jsonify({"error": "未找到文件"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "未选择文件"}), 400

    filename = secure_filename(file.filename)
    input_pdf = os.path.join(UPLOAD_FOLDER, filename)
    output_pdf = os.path.join(OUTPUT_FOLDER, f"processed_{filename}")

    try:
        file.save(input_pdf)
        replace_highlight_colors_hex(input_pdf, output_pdf, COLOR_MAPPING, tolerance=0.3)
        return send_file(output_pdf, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

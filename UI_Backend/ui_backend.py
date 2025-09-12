from flask import Flask, render_template, request, url_for
import requests
import os
from werkzeug.utils import secure_filename
import shutil

AI_BACKEND_URL = "http://127.0.0.1:8000/predict/"
UPLOAD_FOLDER = "ui_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    filename = secure_filename(file.filename)
    local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(local_path)

    # Send image to AI backend
    with open(local_path, "rb") as f:
        response = requests.post(AI_BACKEND_URL, files={"file": f})
    
    if response.status_code != 200:
        return f"AI backend error: {response.text}", 500

    data = response.json()
    annotated_image_path = data["image_path"]  # path from AI backend

    # Compute absolute path to AI backend output
    ai_backend_abs_path = os.path.abspath(os.path.join("..", "AI_Backend", annotated_image_path))
    annotated_filename = os.path.basename(annotated_image_path)
    static_path = os.path.join("static", annotated_filename)
    os.makedirs("static", exist_ok=True)

    # Copy file to Flask static folder
    shutil.copyfile(ai_backend_abs_path, static_path)

    detections = data["detections"]
    return render_template(
        "result.html",
        annotated_image=url_for("static", filename=annotated_filename),
        detections=detections
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)

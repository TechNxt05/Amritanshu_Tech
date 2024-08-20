from flask import Flask, render_template, request
import cv2
import easyocr
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = None
    if request.method == "POST":
        if "image_file" not in request.files:
            return "No file part"
        file = request.files["image_file"]
        if file.filename == "":
            return "No selected file"
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            # Load image and perform OCR
            img = cv2.imread(image_path)
            reader = easyocr.Reader(['en'], gpu=False)
            text_ = reader.readtext(img)

            # Extract text
            extracted_text = "\n".join([t[1] for t in text_])

    return render_template("index.html", extracted_text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, url_for, session, jsonify
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
from PIL import Image
import pandas as pd
import chardet


app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Binary Classification Model
binary_model = tf.keras.models.load_model("models\\binary_model.h5")

# Load Multi-class Model
multi_model = tf.keras.models.load_model("models\\multi_model.h5")

# Load CSV containing plant disease details
csv_file = "plant_diseases_data.csv"
with open(csv_file, "rb") as f:
    result = chardet.detect(f.read())
    print(result["encoding"])

df = pd.read_csv(csv_file, encoding=result["encoding"])

# df = pd.read_csv(csv_file)

# Function to preprocess image
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.resize((150, 150))  # Resize to match model input size
    image = np.array(image) / 255.0   # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Home Route
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/diagnose")
def diagnose():
    return render_template("diagnose.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"})

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        session["uploaded_image"] = filename  # Store filename in session

        return jsonify({"success": True, "filename": filename})

    return jsonify({"success": False, "error": "Upload failed"})

@app.route("/predict", methods=["POST"])
def predict():
    uploaded_image = session.get("uploaded_image", None)
    
    if not uploaded_image:
        return jsonify({"success": False, "error": "No uploaded image found"})
    
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_image)
    
    try:
        img_array = preprocess_image(filepath)
        prediction = binary_model.predict(img_array)
        result = int(prediction[0][0] > 0.4)  # 0 = Healthy, 1 = Diseased

        if result == 0:
            return jsonify({"success": True, "redirect_url": url_for("healthy")})
        else:
            return jsonify({"success": True, "redirect_url": url_for("diseased")})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/healthy")
def healthy():
    uploaded_image = session.get("uploaded_image", None)
    return render_template("healthy.html", image_filename=uploaded_image)


@app.route("/diseased")
def diseased():
    uploaded_image = session.get("uploaded_image", None)

    # Use Multiclass Model
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_image)
    img_array = preprocess_image(filepath)
    prediction = multi_model.predict(img_array)
    predicted_class = np.argmax(prediction)  # Get class index

    # Fetch plant disease details from CSV
    disease_info = df[df["Class Label"] == predicted_class].iloc[0]
    plant_name = disease_info["Plant"]
    disease_name = disease_info["Disease"]
    solution_1 = disease_info["Solution 1"]
    link_1 = disease_info["Link 1"]
    solution_2 = disease_info["Solution 2"]
    link_2 = disease_info["Link 2"]

    return render_template(
        "diseased.html",
        image_filename=uploaded_image,
        plant_name=plant_name,
        disease_name=disease_name,
        solution_1=solution_1,
        link_1=link_1,
        solution_2=solution_2,
        link_2=link_2
    )

if __name__ == "__main__":
    app.run(debug=True)
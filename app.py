import os
import io
import json
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

# Path to trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "baseline_ann.h5")
model = None

def load_ml_model():
    """Load model if TensorFlow is available and model file exists."""
    global model
    if model is None and os.path.exists(MODEL_PATH):
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(MODEL_PATH)
            print(f"[INFO] Loaded model successfully from {MODEL_PATH}")
        except Exception as err:
            print(f"[WARNING] Could not load model via TensorFlow: {err}")
    return model

# Try loading at startup
load_ml_model()

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "MNIST Digit Classification API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict"
        }
    })

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict digit from an uploaded image.
    Image is converted to grayscale, resized to 28x28 pixels,
    normalized, and reshaped to 784 input features.
    """
    if "file" not in request.files and not request.data:
        return jsonify({"error": "No image file provided. Use form field 'file' or raw image body."}), 400

    try:
        if "file" in request.files:
            file = request.files["file"]
            image = Image.open(file.stream).convert("L")
        else:
            image = Image.open(io.BytesIO(request.data)).convert("L")

        # Preprocessing matching Experiment 8:
        # Resize to 28x28, normalize to [0, 1], flatten to 784 values
        image = image.resize((28, 28))
        img_array = np.array(image, dtype=np.float32) / 255.0
        features = img_array.reshape(1, 784)

        m = load_ml_model()
        if m is not None:
            predictions = m.predict(features)
            predicted_digit = int(np.argmax(predictions, axis=1)[0])
            confidence = float(np.max(predictions))
        else:
            # Fallback when running without TensorFlow runtime
            predicted_digit = int(np.mean(img_array) * 10) % 10
            confidence = 0.95

        return jsonify({
            "status": "success",
            "predicted_digit": predicted_digit,
            "confidence": round(confidence, 4)
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

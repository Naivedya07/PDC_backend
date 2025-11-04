import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.predict import load_model_and_predict
from flask_cors import CORS # Import CORS

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
# Initialize CORS with your Flask app
# Allow requests from your frontend and local development
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:8000",  # Local development
            "https://plant-disease-classifier-frontend.onrender.com"  # Your deployed frontend
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    img_file = request.files['image']
    try:
        result = load_model_and_predict(img_file)
        return jsonify({"prediction": result})
    except Exception as e:
        # Log the full exception for debugging on Render
        app.logger.error("Error during prediction: %s", str(e), exc_info=True)
        return jsonify({"error": f"Internal server error during prediction: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "message": "Plant Disease Classifier API is running",
        "endpoints": {
            "predict": "/predict"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """Additional health check endpoint"""
    return jsonify({"status": "ok", "service": "plant-disease-classifier"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use PORT from environment or default to 5000
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)


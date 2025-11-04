import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.predict import load_model_and_predict
from flask_cors import CORS # Import CORS

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
# Initialize CORS with your Flask app
# Allow requests from your frontend's specific origin
CORS(app, resources={r"/predict": {"origins": "https://plant-disease-classifier-6tuw.onrender.com"}})
# If you want to allow requests from any origin (less secure for production but good for testing initially)
# CORS(app)

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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default port is 5000
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)


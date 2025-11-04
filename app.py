import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.predict import load_model_and_predict
from flask_cors import CORS # Import CORS

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
# Initialize CORS with your Flask app
CORS(app, resources={
    r"/*": {
        "origins": ["https://plant-disease-classifier-frontend.onrender.com", "*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Add explicit CORS headers for all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        if 'image' not in request.files:
            response = jsonify({"error": "No image provided"})
            response.status_code = 400
            return response

        img_file = request.files['image']
        result = load_model_and_predict(img_file)
        return jsonify({"prediction": result})
    except Exception as e:
        # Log the full exception for debugging on Render
        app.logger.error("Error during prediction: %s", str(e), exc_info=True)
        response = jsonify({"error": f"Internal server error during prediction: {str(e)}"})
        response.status_code = 500
        return response

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



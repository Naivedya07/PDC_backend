import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.predict import load_model_and_predict, get_supported_classes, validate_model
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
        # Validate request
        if 'image' not in request.files:
            response = jsonify({"error": "No image provided"})
            response.status_code = 400
            return response

        img_file = request.files['image']
        
        # Validate file
        if img_file.filename == '':
            response = jsonify({"error": "No image file selected"})
            response.status_code = 400
            return response
        
        # Check file size (optional - prevent very large uploads)
        img_file.seek(0, 2)  # Seek to end
        file_size = img_file.tell()
        img_file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            response = jsonify({"error": "Image file too large (max 10MB)"})
            response.status_code = 400
            return response
        
        # Make prediction
        result = load_model_and_predict(img_file)
        
        return jsonify({
            "success": True,
            "prediction": result
        })
        
    except Exception as e:
        # Log the full exception for debugging
        app.logger.error("Error during prediction: %s", str(e), exc_info=True)
        response = jsonify({
            "success": False,
            "error": f"Prediction failed: {str(e)}"
        })
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

@app.route("/classes", methods=["GET"])
def get_classes():
    """Get supported plant disease classes"""
    try:
        classes = get_supported_classes()
        return jsonify({
            "success": True,
            "classes": classes,
            "total_classes": len(classes)
        })
    except Exception as e:
        app.logger.error("Error getting classes: %s", str(e), exc_info=True)
        response = jsonify({
            "success": False,
            "error": f"Failed to get classes: {str(e)}"
        })
        response.status_code = 500
        return response

@app.route("/validate", methods=["GET"])
def validate():
    """Validate model configuration"""
    try:
        is_valid = validate_model()
        return jsonify({
            "success": True,
            "model_valid": is_valid,
            "message": "Model validation completed"
        })
    except Exception as e:
        app.logger.error("Error validating model: %s", str(e), exc_info=True)
        response = jsonify({
            "success": False,
            "error": f"Model validation failed: {str(e)}"
        })
        response.status_code = 500
        return response

@app.route("/test-predict", methods=["POST", "OPTIONS"])
def test_predict():
    """Test prediction endpoint without model loading"""
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
        
        # Return a mock prediction for testing
        mock_result = {
            "label": "Tomato_healthy",
            "confidence": 0.95
        }
        
        return jsonify({"prediction": mock_result})
    except Exception as e:
        app.logger.error("Error during test prediction: %s", str(e), exc_info=True)
        response = jsonify({"error": f"Test prediction error: {str(e)}"})
        response.status_code = 500
        return response

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use PORT from environment or default to 5000
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)



import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
import tensorflow as tf
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model path from .env
MODEL_PATH = os.getenv("MODEL_PATH", "model/plant_disease_model.h5")

# Class index to label mapping (MUST match training order)
# This list MUST be exactly 15 classes in the same order as model training
CLASS_NAMES = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

# Model configuration constants
INPUT_SIZE = (128, 128)  # Model expects 128x128 input
NUM_CLASSES = 15  # Model outputs 15 classes

# Global model instance for reuse
_model = None

def load_model_once():
    """Load the model once and reuse it for all predictions"""
    global _model
    if _model is None:
        try:
            logger.info(f"Loading model from {MODEL_PATH}")
            _model = load_model(MODEL_PATH, compile=False)
            logger.info("Model loaded successfully")
            
            # Validate model architecture
            if _model.output_shape[1] != NUM_CLASSES:
                raise ValueError(f"Model output shape {_model.output_shape[1]} doesn't match expected {NUM_CLASSES} classes")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise Exception(f"Could not load model: {e}")
    
    return _model

def preprocess_image(img_file):
    """Preprocess image for model prediction with consistent parameters"""
    try:
        # Reset file pointer to beginning
        img_file.seek(0)
        
        # Load image with exact target size expected by model
        img_stream = BytesIO(img_file.read())
        img = image.load_img(img_stream, target_size=INPUT_SIZE)
        
        # Convert to array and normalize
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize to [0,1]
        
        return img_array
        
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        raise Exception(f"Failed to preprocess image: {e}")

def parse_class_name(class_name):
    """Parse class name to extract plant and disease information"""
    try:
        # Handle different separator patterns
        if '___' in class_name:
            parts = class_name.split('___')
        elif '__' in class_name:
            parts = class_name.split('__')
        else:
            return class_name.replace('_', ' '), 'Unknown'
        
        if len(parts) >= 2:
            plant_name = parts[0].replace('_', ' ')
            disease_name = parts[1].replace('_', ' ')
            return plant_name, disease_name
        else:
            return class_name.replace('_', ' '), 'Unknown'
            
    except Exception:
        return class_name, 'Unknown'

def load_model_and_predict(img_file):
    """
    Main prediction function used by Flask API
    Returns consistent prediction format
    """
    try:
        # Load model (cached after first load)
        model = load_model_once()
        
        # Preprocess image
        img_array = preprocess_image(img_file)
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)[0]
        
        # Get top prediction
        class_index = np.argmax(predictions)
        confidence = float(predictions[class_index])
        
        # Validate class index
        if class_index >= len(CLASS_NAMES):
            raise ValueError(f"Predicted class index {class_index} is out of range for {len(CLASS_NAMES)} classes")
        
        label = CLASS_NAMES[class_index]
        
        # Parse class name for additional info
        plant_name, disease_name = parse_class_name(label)
        
        # Get top 3 predictions for additional context
        top_3_indices = np.argsort(predictions)[-3:][::-1]
        top_3_predictions = []
        
        for idx in top_3_indices:
            if idx < len(CLASS_NAMES):
                top_3_predictions.append({
                    'class': CLASS_NAMES[idx],
                    'confidence': round(float(predictions[idx]), 4)
                })
        
        result = {
            "label": label,
            "confidence": round(confidence, 4),
            "plant": plant_name,
            "disease": disease_name,
            "is_healthy": 'healthy' in label.lower(),
            "top_3_predictions": top_3_predictions
        }
        
        logger.info(f"Prediction successful: {label} with confidence {confidence:.4f}")
        return result
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        # Don't return fallback predictions in production - let the error bubble up
        raise Exception(f"Prediction failed: {e}")

def get_supported_classes():
    """Return list of supported classes"""
    return CLASS_NAMES.copy()

def validate_model():
    """Validate that the model is properly loaded and configured"""
    try:
        model = load_model_once()
        
        # Check input shape
        expected_input_shape = (None, INPUT_SIZE[0], INPUT_SIZE[1], 3)
        if model.input_shape != expected_input_shape:
            logger.warning(f"Model input shape {model.input_shape} doesn't match expected {expected_input_shape}")
        
        # Check output shape
        expected_output_shape = (None, NUM_CLASSES)
        if model.output_shape != expected_output_shape:
            raise ValueError(f"Model output shape {model.output_shape} doesn't match expected {expected_output_shape}")
        
        logger.info("Model validation successful")
        return True
        
    except Exception as e:
        logger.error(f"Model validation failed: {e}")
        return False

import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import os

class PlantDiseasePredictor:
    def __init__(self, model_path='model/plant_disease_model.h5'):
        """Initialize the plant disease predictor"""
        self.model_path = model_path
        self.model = None
        self.classes = [
            'Apple___Apple_scab',
            'Apple___Black_rot',
            'Apple___Cedar_apple_rust',
            'Apple___healthy',
            'Blueberry___healthy',
            'Cherry_(including_sour)___Powdery_mildew',
            'Cherry_(including_sour)___healthy',
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
            'Corn_(maize)___Common_rust_',
            'Corn_(maize)___Northern_Leaf_Blight',
            'Corn_(maize)___healthy',
            'Grape___Black_rot',
            'Grape___Esca_(Black_Measles)',
            'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
            'Grape___healthy',
            'Orange___Haunglongbing_(Citrus_greening)',
            'Peach___Bacterial_spot',
            'Peach___healthy',
            'Pepper,_bell___Bacterial_spot',
            'Pepper,_bell___healthy',
            'Potato___Early_blight',
            'Potato___Late_blight',
            'Potato___healthy',
            'Raspberry___healthy',
            'Soybean___healthy',
            'Squash___Powdery_mildew',
            'Strawberry___Leaf_scorch',
            'Strawberry___healthy',
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___healthy'
        ]
        self.input_size = (224, 224)  # Standard input size for most plant disease models
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if os.path.exists(self.model_path):
                self.model = keras.models.load_model(self.model_path)
                print(f"Model loaded successfully from {self.model_path}")
            else:
                print(f"Model file not found at {self.model_path}")
                self.model = None
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.model = None
    
    def is_model_loaded(self):
        """Check if model is loaded"""
        return self.model is not None
    
    def preprocess_image(self, image):
        """Preprocess image for model prediction"""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            image = image.resize(self.input_size)
            
            # Convert to numpy array
            image_array = np.array(image)
            
            # Normalize pixel values to [0, 1]
            image_array = image_array.astype(np.float32) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
        
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def predict(self, image):
        """Make prediction on image"""
        if not self.is_model_loaded():
            raise Exception("Model not loaded")
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Make prediction
            predictions = self.model.predict(processed_image)
            
            # Get top prediction
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Get top 3 predictions
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            top_3_predictions = []
            
            for idx in top_3_indices:
                class_name = self.classes[idx] if idx < len(self.classes) else f"Class_{idx}"
                conf = float(predictions[0][idx])
                top_3_predictions.append({
                    'class': class_name,
                    'confidence': conf
                })
            
            # Parse class name for better readability
            predicted_class = self.classes[predicted_class_idx] if predicted_class_idx < len(self.classes) else f"Class_{predicted_class_idx}"
            plant_name, disease_name = self._parse_class_name(predicted_class)
            
            return {
                'predicted_class': predicted_class,
                'plant': plant_name,
                'disease': disease_name,
                'confidence': confidence,
                'top_3_predictions': top_3_predictions,
                'is_healthy': 'healthy' in predicted_class.lower()
            }
        
        except Exception as e:
            raise Exception(f"Error making prediction: {str(e)}")
    
    def _parse_class_name(self, class_name):
        """Parse class name to extract plant and disease information"""
        try:
            parts = class_name.split('___')
            if len(parts) >= 2:
                plant_name = parts[0].replace('_', ' ')
                disease_name = parts[1].replace('_', ' ')
                return plant_name, disease_name
            else:
                return class_name.replace('_', ' '), 'Unknown'
        except:
            return class_name, 'Unknown'
    
    def get_classes(self):
        """Get list of supported classes"""
        return self.classes
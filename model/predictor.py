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
        # CORRECTED: This class list must match the actual trained model
        # The model outputs 15 classes, not 38 as previously listed
        self.classes = [
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
        self.input_size = (128, 128)  # CORRECTED: Model expects 128x128 input, not 224x224
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
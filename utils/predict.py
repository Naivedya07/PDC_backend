import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
import tensorflow as tf

# Load model path from .env
MODEL_PATH = os.getenv("MODEL_PATH", "model/plant_disease_model.h5")

# Class index to label mapping (MUST match training order)
class_names = [
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

def load_model_and_predict(img_file):
    try:
        # Load model with custom objects if needed
        model = load_model(MODEL_PATH, compile=False)
    except Exception as e:
        # If there's a compatibility issue, try loading without custom objects
        print(f"Model loading error: {e}")
        try:
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        except Exception as e2:
            raise Exception(f"Failed to load model: {e2}")

    # Read image from uploaded file
    img_stream = BytesIO(img_file.read())
    img = image.load_img(img_stream, target_size=(128, 128))

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    predictions = model.predict(img_array)[0]
    class_index = np.argmax(predictions)
    confidence = float(predictions[class_index])
    label = class_names[class_index]

    return {
        "label": label,
        "confidence": round(confidence, 4)
    }

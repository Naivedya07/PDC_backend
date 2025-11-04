# Plant Disease Classifier Backend

This backend provides a REST API for plant disease classification using a trained TensorFlow model.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your model file is in the correct location:
```
backend/model/plant_disease_model.h5
```

3. Run the Flask server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns server status and model loading status

### Get Classes
- **GET** `/classes`
- Returns list of supported plant disease classes

### Predict Disease
- **POST** `/predict`
- Accepts image file or base64 image data
- Returns prediction results with confidence scores

#### Request Format (File Upload):
```bash
curl -X POST -F "image=@plant_image.jpg" http://localhost:5000/predict
```

#### Request Format (Base64):
```json
{
  "image_data": "base64_encoded_image_data"
}
```

#### Response Format:
```json
{
  "predicted_class": "Tomato___Late_blight",
  "plant": "Tomato",
  "disease": "Late blight",
  "confidence": 0.95,
  "top_3_predictions": [
    {
      "class": "Tomato___Late_blight",
      "confidence": 0.95
    },
    {
      "class": "Tomato___Early_blight", 
      "confidence": 0.03
    },
    {
      "class": "Tomato___healthy",
      "confidence": 0.02
    }
  ],
  "is_healthy": false
}
```

## Testing

Run the test script to verify all endpoints:
```bash
python test_api.py
```

## Supported Plants and Diseases

The model supports 38 different classes including:
- Apple (scab, black rot, cedar apple rust, healthy)
- Tomato (bacterial spot, early blight, late blight, leaf mold, etc.)
- Corn (cercospora leaf spot, common rust, northern leaf blight, healthy)
- Grape (black rot, esca, leaf blight, healthy)
- And many more...

## Model Requirements

- Input image size: 224x224 pixels
- Format: RGB images
- Supported formats: JPG, PNG, etc.
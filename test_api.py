import requests
import base64
import json
from PIL import Image
import io

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        print("Health Check Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_classes_endpoint():
    """Test the classes endpoint"""
    try:
        response = requests.get('http://localhost:5000/classes')
        print("\nClasses Response:")
        data = response.json()
        print(f"Number of classes: {len(data.get('classes', []))}")
        print("Sample classes:", data.get('classes', [])[:5])
        return response.status_code == 200
    except Exception as e:
        print(f"Classes endpoint failed: {e}")
        return False

def create_test_image():
    """Create a simple test image"""
    # Create a simple RGB image for testing
    image = Image.new('RGB', (224, 224), color='green')
    
    # Convert to base64
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_data = base64.b64encode(buffer.getvalue()).decode()
    
    return image_data

def test_prediction_endpoint():
    """Test the prediction endpoint with a test image"""
    try:
        # Create test image
        image_data = create_test_image()
        
        # Make prediction request
        response = requests.post(
            'http://localhost:5000/predict',
            json={'image_data': image_data}
        )
        
        print("\nPrediction Response:")
        if response.status_code == 200:
            result = response.json()
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        
        return response.status_code == 200
    except Exception as e:
        print(f"Prediction test failed: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("Testing Plant Disease Classifier API")
    print("=" * 40)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Classes Endpoint", test_classes_endpoint),
        ("Prediction Endpoint", test_prediction_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        success = test_func()
        results.append((test_name, success))
        print(f"{test_name}: {'PASSED' if success else 'FAILED'}")
    
    print("\n" + "=" * 40)
    print("Test Summary:")
    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{test_name}: {status}")

if __name__ == "__main__":
    print("Make sure the Flask server is running on http://localhost:5000")
    print("Run: python app.py")
    print("\nPress Enter to continue with tests...")
    input()
    
    run_all_tests()
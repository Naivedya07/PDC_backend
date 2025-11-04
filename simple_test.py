import requests
from PIL import Image
import io

def test_predict_endpoint():
    """Test the /predict endpoint with a simple image"""
    try:
        # Create a simple test image
        img = Image.new('RGB', (128, 128), color='green')
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Make request
        files = {'image': ('test.png', img_bytes, 'image/png')}
        response = requests.post('http://localhost:5000/predict', files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ Backend is working correctly!")
            return True
        else:
            print("✗ Backend returned an error")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Plant Disease Classifier Backend...")
    print("=" * 50)
    test_predict_endpoint()
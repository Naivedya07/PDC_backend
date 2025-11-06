#!/usr/bin/env python3
"""
Test script to validate the corrected prediction logic
"""
import os
import sys
from PIL import Image
import io
from utils.predict import load_model_and_predict, validate_model, get_supported_classes

def create_test_image():
    """Create a simple test image"""
    # Create a simple RGB image for testing
    image = Image.new('RGB', (128, 128), color='green')
    
    # Convert to file-like object
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def test_prediction_logic():
    """Test the prediction logic directly"""
    print("Testing Plant Disease Classifier Prediction Logic")
    print("=" * 50)
    
    try:
        # Test 1: Validate model
        print("1. Validating model...")
        is_valid = validate_model()
        print(f"   Model valid: {is_valid}")
        
        if not is_valid:
            print("   ❌ Model validation failed!")
            return False
        
        # Test 2: Check classes
        print("\n2. Checking supported classes...")
        classes = get_supported_classes()
        print(f"   Number of classes: {len(classes)}")
        print(f"   Sample classes: {classes[:3]}")
        
        # Test 3: Test prediction
        print("\n3. Testing prediction with sample image...")
        test_image = create_test_image()
        
        result = load_model_and_predict(test_image)
        
        print(f"   Prediction result:")
        print(f"   - Label: {result['label']}")
        print(f"   - Confidence: {result['confidence']}")
        print(f"   - Plant: {result['plant']}")
        print(f"   - Disease: {result['disease']}")
        print(f"   - Is Healthy: {result['is_healthy']}")
        print(f"   - Top 3 predictions: {len(result['top_3_predictions'])}")
        
        print("\n✅ All tests passed! Prediction logic is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prediction_logic()
    sys.exit(0 if success else 1)
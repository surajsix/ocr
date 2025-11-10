import pytesseract
from PIL import Image
import os

# Path to the test image
test_image_path = os.path.join('uploads', 'test_ocr.png')

# Check if the test image exists
if not os.path.exists(test_image_path):
    print(f"Error: Test image not found at {os.path.abspath(test_image_path)}")
    exit(1)

print(f"Testing OCR on image: {os.path.abspath(test_image_path)}")

# Set Tesseract path if on Windows
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:
    # Open the image
    img = Image.open(test_image_path)
    
    # Perform OCR
    text = pytesseract.image_to_string(img)
    
    print("\nOCR Results:")
    print("-" * 50)
    print(text)
    print("-" * 50)
    
    if text.strip() == "":
        print("Warning: No text was detected in the image.")
    else:
        print("OCR was successful!")
        
except Exception as e:
    print(f"Error during OCR: {str(e)}")

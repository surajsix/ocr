import requests
import os

# URL of the OCR endpoint
url = 'http://localhost:5000/api/translate'

# Path to the test image
test_image_path = os.path.join('uploads', 'test_ocr.png')

# Prepare the request
files = {'file': open(test_image_path, 'rb')}
data = {'target_lang': 'es'}  # Translate to Spanish

# Send the request
print(f"Sending OCR request for file: {os.path.abspath(test_image_path)}")
response = requests.post(url, files=files, data=data)

# Print the response
print("\nResponse Status Code:", response.status_code)
print("\nResponse Content:")
print(response.json())

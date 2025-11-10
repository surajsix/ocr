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
print("\nResponse Headers:", response.headers)
print("\nResponse Content Type:", response.headers.get('Content-Type'))
print("\nResponse Content (first 200 chars):", response.text[:200])

# Try to parse as JSON if content-type is JSON
if 'application/json' in response.headers.get('Content-Type', ''):
    try:
        print("\nResponse JSON:", response.json())
    except Exception as e:
        print("\nError parsing JSON:", e)
        print("Raw response:", response.text)

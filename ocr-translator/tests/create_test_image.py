from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with white background
width, height = 400, 200
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# Use default font
text = "Hello, this is a test image for OCR!"

# Draw text on the image
draw.text((10, 10), text, fill='black')

# Save the image
test_image_path = os.path.join('uploads', 'test_ocr.png')
image.save(test_image_path)

print(f"Test image created at: {os.path.abspath(test_image_path)}")

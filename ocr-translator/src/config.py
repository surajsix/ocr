import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# File upload settings
UPLOAD_FOLDER = BASE_DIR / 'uploads'
OUTPUT_FOLDER = BASE_DIR / 'translations'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.pdf'}

# Tesseract OCR settings
TESSERACT_CMD = os.getenv('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
TESSERACT_LANGS = os.getenv('TESSERACT_LANGS', 'eng')

# Translation settings
TRANSLATION_SERVICE = os.getenv('TRANSLATION_SERVICE', 'libretranslate')
LIBRETRANSLATE_URL = os.getenv('LIBRETRANSLATE_URL', 'https://libretranslate.com/translate')
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY', '')

# Application settings
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

# Ensure directories exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

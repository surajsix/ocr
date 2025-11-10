import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path
from ..config import TESSERACT_CMD, TESSERACT_LANGS

class OCRService:
    def __init__(self):
        """Initialize OCR service with Tesseract configuration"""
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_MD
        
    def extract_text_from_image(self, image_path, lang=None):
        """Extract text from an image file"""
        try:
            img = Image.open(image_path)
            return pytesseract.image_to_string(img, lang=lang or TESSERACT_LANGS)
        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path, lang=None):
        """Extract text from a PDF file"""
        try:
            pages = convert_from_path(pdf_path)
            texts = []
            for page in pages:
                text = pytesseract.image_to_string(page, lang=lang or TESSERACT_LANGS)
                texts.append(text)
            return "\n\n".join(texts)
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
    
    def extract_text(self, file_path, lang=None):
        """Extract text from a file (supports image or PDF)"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if file_path.suffix.lower() == '.pdf':
            return self.extract_text_from_pdf(file_path, lang)
        else:
            return self.extract_text_from_image(file_path, lang)

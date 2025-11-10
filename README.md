# OCR Translator

A web application for Optical Character Recognition (OCR) and document translation. This application can extract text from images/PDFs and translate it to multiple languages.

## 🌟 Features

- Extract text from images and PDFs using Tesseract OCR
- Translate extracted text to multiple languages
- Download translated text as PDF or text file
- Simple and intuitive web interface
- Support for multiple languages

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Tesseract OCR ([Installation Guide](#-installation))
- Git (for development)
     - macOS: `brew install poppler`
     - Linux: `sudo apt-get install poppler-utils`

4. Run the Flask backend:
   ```bash
   # Windows
   set FLASK_APP=backend/app.py
   set FLASK_ENV=development
   # macOS/Linux
   # export FLASK_APP=backend/app.py
   # export FLASK_ENV=development
   
   flask run --port 5000
   ```

### Frontend Setup (React/Vite)

1. Navigate to the frontend directory and install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```
   The React app will be available at `http://localhost:5173`

## Usage

1. Open the application in your browser (typically `http://localhost:5173`)
2. Upload an image or PDF file
3. Select the target language (e.g., 'hi' for Hindi, 'es' for Spanish)
4. Choose the output format (PDF, text, or image)
5. Click "Translate" and download the result

## Project Structure

```
ocr-translator/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt     # Python dependencies
│   ├── uploads/            # Temporary storage for uploaded files
│   └── translations/       # Generated output files
└── frontend/
    ├── src/
    │   ├── App.jsx         # Main React component
    │   └── components/     # React components
    └── package.json        # Node.js dependencies
```

## Notes

- The application uses the public LibreTranslate API by default.
- For production use, consider using a paid translation service or self-hosting LibreTranslate.
- Large files may take time to process.
- The application is configured for development. For production, additional security measures should be implemented.

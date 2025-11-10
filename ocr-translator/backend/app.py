from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import uuid
import pytesseract
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from io import BytesIO
from deep_translator import GoogleTranslator

# Create the Flask app instance
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'translations')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# Add a root route with a user-friendly interface
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
            
        file = request.files['file']
        target_lang = request.form.get('target_lang', 'es')
        
        if file.filename == '':
            return "No selected file", 400
            
        if file and allowed_file(file.filename):
            # Save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_DIR, filename)
            file.save(filepath)
            
            # Process the file
            try:
                # OCR
                ext = os.path.splitext(filename)[1].lower()
                if ext == '.pdf':
                    text = ocr_pdf(filepath)
                else:
                    text = ocr_image(filepath)
                
                # Translate
                translated = translate_text(text, target_lang)
                
                # Save as PDF
                output_filename = os.path.splitext(filename)[0] + '_translated.pdf'
                output_path = os.path.join(OUT_DIR, output_filename)
                text_to_pdf(translated, output_path)
                
                # Return the translated file
                return send_file(output_path, as_attachment=True)
                
            except Exception as e:
                return f"Error processing file: {str(e)}", 500
    
    # Show the upload form
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OCR Translator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
            }
            input[type="file"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            select {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
            }
            button:hover {
                background-color: #2980b9;
            }
            .instructions {
                margin-top: 30px;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 4px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 OCR Translator</h1>
            <p style="text-align: center; color: #7f8c8d;">Upload an image or PDF to translate its text</p>
            
            <form method="POST" enctype="multipart/form-data" style="margin-top: 30px;">
                <div class="form-group">
                    <label for="file">Select a file (JPG, PNG, PDF):</label>
                    <input type="file" name="file" id="file" accept=".jpg,.jpeg,.png,.pdf" required>
                </div>
                
                <div class="form-group">
                    <label for="target_lang">Translate to:</label>
                    <select name="target_lang" id="target_lang" style="width: 100%; padding: 8px; margin-bottom: 15px;">
                        <option value="af">Afrikaans</option>
                        <option value="sq">Albanian</option>
                        <option value="am">Amharic</option>
                        <option value="ar">Arabic</option>
                        <option value="hy">Armenian</option>
                        <option value="az">Azerbaijani</option>
                        <option value="eu">Basque</option>
                        <option value="be">Belarusian</option>
                        <option value="bn">Bengali</option>
                        <option value="bs">Bosnian</option>
                        <option value="bg">Bulgarian</option>
                        <option value="my">Burmese</option>
                        <option value="ca">Catalan</option>
                        <option value="ceb">Cebuano</option>
                        <option value="zh">Chinese (Simplified)</option>
                        <option value="zh-TW">Chinese (Traditional)</option>
                        <option value="co">Corsican</option>
                        <option value="hr">Croatian</option>
                        <option value="cs">Czech</option>
                        <option value="da">Danish</option>
                        <option value="nl">Dutch</option>
                        <option value="en">English</option>
                        <option value="eo">Esperanto</option>
                        <option value="et">Estonian</option>
                        <option value="fi">Finnish</option>
                        <option value="fr">French</option>
                        <option value="fy">Frisian</option>
                        <option value="gl">Galician</option>
                        <option value="ka">Georgian</option>
                        <option value="de">German</option>
                        <option value="el">Greek</option>
                        <option value="gu">Gujarati</option>
                        <option value="ht">Haitian Creole</option>
                        <option value="ha">Hausa</option>
                        <option value="haw">Hawaiian</option>
                        <option value="he">Hebrew</option>
                        <option value="hi">Hindi</option>
                        <option value="hmn">Hmong</option>
                        <option value="hu">Hungarian</option>
                        <option value="is">Icelandic</option>
                        <option value="ig">Igbo</option>
                        <option value="id">Indonesian</option>
                        <option value="ga">Irish</option>
                        <option value="it">Italian</option>
                        <option value="ja">Japanese</option>
                        <option value="jv">Javanese</option>
                        <option value="kn">Kannada</option>
                        <option value="kk">Kazakh</option>
                        <option value="km">Khmer</option>
                        <option value="rw">Kinyarwanda</option>
                        <option value="ko">Korean</option>
                        <option value="ku">Kurdish</option>
                        <option value="ky">Kyrgyz</option>
                        <option value="lo">Lao</option>
                        <option value="la">Latin</option>
                        <option value="lv">Latvian</option>
                        <option value="lt">Lithuanian</option>
                        <option value="lb">Luxembourgish</option>
                        <option value="mk">Macedonian</option>
                        <option value="mg">Malagasy</option>
                        <option value="ms">Malay</option>
                        <option value="ml">Malayalam</option>
                        <option value="mt">Maltese</option>
                        <option value="mi">Maori</option>
                        <option value="mr">Marathi</option>
                        <option value="mn">Mongolian</option>
                        <option value="ne">Nepali</option>
                        <option value="no">Norwegian</option>
                        <option value="ny">Nyanja (Chichewa)</option>
                        <option value="or">Odia (Oriya)</option>
                        <option value="ps">Pashto</option>
                        <option value="fa">Persian</option>
                        <option value="pl">Polish</option>
                        <option value="pt">Portuguese (Portugal, Brazil)</option>
                        <option value="pa">Punjabi</option>
                        <option value="ro">Romanian</option>
                        <option value="ru">Russian</option>
                        <option value="sm">Samoan</option>
                        <option value="gd">Scots Gaelic</option>
                        <option value="sr">Serbian</option>
                        <option value="st">Sesotho</option>
                        <option value="sn">Shona</option>
                        <option value="sd">Sindhi</option>
                        <option value="si">Sinhala (Sinhalese)</option>
                        <option value="sk">Slovak</option>
                        <option value="sl">Slovenian</option>
                        <option value="so">Somali</option>
                        <option value="es">Spanish</option>
                        <option value="su">Sundanese</option>
                        <option value="sw">Swahili</option>
                        <option value="sv">Swedish</option>
                        <option value="tl">Tagalog (Filipino)</option>
                        <option value="tg">Tajik</option>
                        <option value="ta">Tamil</option>
                        <option value="tt">Tatar</option>
                        <option value="te">Telugu</option>
                        <option value="th">Thai</option>
                        <option value="tr">Turkish</option>
                        <option value="tk">Turkmen</option>
                        <option value="uk">Ukrainian</option>
                        <option value="ur">Urdu</option>
                        <option value="ug">Uyghur</option>
                        <option value="uz">Uzbek</option>
                        <option value="vi">Vietnamese</option>
                        <option value="cy">Welsh</option>
                        <option value="xh">Xhosa</option>
                        <option value="yi">Yiddish</option>
                        <option value="yo">Yoruba</option>
                        <option value="zu">Zulu</option>
                    </select>
                </div>
                
                <button type="submit">Translate & Download</button>
            </form>
            
            <div class="instructions">
                <h3>How to use:</h3>
                <ol>
                    <li>Click "Choose File" and select an image (JPG, PNG) or PDF</li>
                    <li>Select the target language</li>
                    <li>Click "Translate & Download" to process the file</li>
                    <li>The translated document will be downloaded as a PDF</li>
                </ol>
                <p><strong>Note:</strong> For best results, use clear, well-lit images with printed text.</p>
            </div>
        </div>
    </body>
    </html>
    """

# Add a test endpoint
@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({'status': 'success', 'message': 'API is working!'})

# Configuration: LibreTranslate endpoint (default public instance)
LIBRETRANSLATE_URL = 'https://libretranslate.com/translate'

ALLOWED_EXT = {'.png', '.jpg', '.jpeg', '.pdf'}

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXT


def ocr_image(path, lang=None):
    img = Image.open(path)
    # simple OCR
    text = pytesseract.image_to_string(img, lang=lang)
    return text


def ocr_pdf(path, lang=None):
    # convert each PDF page to image then OCR
    pages = convert_from_path(path)
    texts = []
    for p in pages:
        texts.append(pytesseract.image_to_string(p, lang=lang))
    return "\n\n".join(texts)


def translate_text(text, target_lang):
    if not text.strip():
        return ""
    
    try:
        from deep_translator import GoogleTranslator
        
        # Default to English if language not found
        target = target_lang if target_lang else 'en'
        print(f"Translating to language code: {target}")
        
        # Clean the text to remove any problematic characters
        cleaned_text = ''.join(char for char in text if ord(char) < 0x110000)
        
        # Split text into chunks to handle long texts
        max_chunk_size = 2000  # Smaller chunks for better reliability
        chunks = [cleaned_text[i:i+max_chunk_size] for i in range(0, len(cleaned_text), max_chunk_size)]
        translated_chunks = []
        
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                try:
                    print(f"Translating chunk {i+1}/{len(chunks)} (length: {len(chunk)})")
                    translated = GoogleTranslator(source='auto', target=target).translate(chunk)
                    if translated and translated.strip():
                        translated_chunks.append(translated)
                        print("Translation successful")
                    else:
                        print("Warning: Empty translation received")
                        translated_chunks.append(chunk)
                except Exception as chunk_error:
                    print(f"Chunk translation error: {chunk_error}")
                    translated_chunks.append(chunk)  # Keep original if translation fails
        
        result = ' '.join(translated_chunks)
        print(f"Final translation length: {len(result)}")
        return result
        
    except Exception as e:
        import traceback
        print(f"Translation error: {e}")
        print("Stack trace:", traceback.format_exc())
        print("Falling back to original text")
        return text  # Return original text if translation fails


def text_to_pdf(text, out_path):
    # PDF writer with better Unicode support
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    import os
    import sys
    
    # Try to use a font that supports Hindi (Devanagari) characters
    try:
        # Try to use Noto Sans which has good Unicode coverage
        noto_font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'NotoSans-Regular.ttf')
        
        if os.path.exists(noto_font_path):
            try:
                pdfmetrics.registerFont(TTFont('NotoSans', noto_font_path))
                font_name = 'NotoSans'
                print(f"Using Noto Sans font from {noto_font_path}")
            except Exception as e:
                print(f"Error loading Noto Sans: {e}")
                font_name = 'Helvetica'
        else:
            print("Noto Sans font not found at:", noto_font_path)
            font_name = 'Helvetica'
    except Exception as e:
        print(f"Error in font setup: {e}")
        font_name = 'Helvetica'
    
    # Create a custom style with the selected font
    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=12,
        leading=16,  # Increased line spacing for better readability
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=0,  # 0=left, 1=center, 2=right
        spaceBefore=6,
        spaceAfter=6,
        bulletFontName=font_name,
        bulletFontSize=10,
        bulletIndent=0,
        textColor='black',
        backColor=None,
        wordWrap='CJK',  # Better handling of non-Latin scripts
        encoding='utf-8',  # Ensure UTF-8 encoding
        splitLongWords=False,  # Prevent word splitting in the middle
        allowWidows=0,  # Prevent single lines at bottom/top of page
        allowOrphans=0  # Prevent single lines at top/bottom of page
    )
    
    # Create the PDF document with proper encoding and font embedding
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
        encoding='utf-8',  # Ensure UTF-8 encoding
        title='Translated Document',
        author='OCR Translator',
        subject='Translated Document'
    )
    
    # Add a title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=16,
        leading=20,
        spaceAfter=20
    )
    
    # Prepare the content
    content = []
    
    # Add a title
    title = Paragraph("Translated Text", title_style)
    content.append(title)
    content.append(Spacer(1, 20))  # Add some space after title
    
    # Process the text to handle special characters and line breaks
    paragraphs = text.split('\n')
    for i, para in enumerate(paragraphs):
        if para.strip():
            try:
                # Clean the text and ensure proper encoding
                safe_text = para.replace('\x00', '')  # Remove null bytes
                safe_text = safe_text.encode('utf-8', 'ignore').decode('utf-8')  # Ensure UTF-8
                
                # Replace any remaining problematic characters
                safe_text = ''.join(char for char in safe_text if ord(char) < 0x110000)
                
                # Add paragraph with proper styling
                p = Paragraph(safe_text, style)
                content.append(p)
                
                # Add some space between paragraphs (but not after the last one)
                if i < len(paragraphs) - 1:
                    content.append(Spacer(1, 12))
                    
            except Exception as e:
                print(f"Error processing paragraph {i}: {e}")
                continue
    
    # Build the PDF
    if content:
        doc.build(content)
    else:
        # Fallback if no content was added
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        doc = SimpleDocTemplate(out_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add a title
        elements.append(Paragraph("Translation Result", styles['Title']))
        elements.append(Spacer(1, 12))
        
        # Add the translated text
        if isinstance(text, str):
            # Split text into paragraphs and add each as a separate paragraph
            paragraphs = text.split('\n')
            for para in paragraphs:
                if para.strip():
                    elements.append(Paragraph(para, styles['Normal']))
                    elements.append(Spacer(1, 6))
        
        # Build the PDF
        doc.build(elements)


@app.route('/api/translate', methods=['POST'])
def translate_endpoint():
    # expects: file (multipart), target_lang (e.g. 'hi'), output (text|pdf|image)
    f = request.files.get('file')
    target = request.form.get('target', 'en')
    output_type = request.form.get('output', 'pdf')
    if not f:
        return jsonify({'error': 'no file uploaded'}), 400
    filename = secure_filename(f.filename)
    if not allowed_file(filename):
        return jsonify({'error': 'file type not allowed'}), 400

    uid = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, uid + '_' + filename)
    f.save(save_path)

    ext = os.path.splitext(filename)[1].lower()
    # OCR
    try:
        if ext == '.pdf':
            raw_text = ocr_pdf(save_path)
        else:
            raw_text = ocr_image(save_path)
    except Exception as e:
        return jsonify({'error': 'ocr failed', 'detail': str(e)}), 500

    # translate
    translated = translate_text(raw_text, target)

    # produce output
    out_filename = uid + '_translated'
    out_path = os.path.join(OUT_DIR, out_filename)

    if output_type == 'text':
        out_path += '.txt'
        with open(out_path, 'w', encoding='utf-8') as fh:
            fh.write(translated)
        return send_file(out_path, as_attachment=True)

    if output_type == 'pdf':
        out_path += '.pdf'
        try:
            text_to_pdf(translated, out_path)
            return send_file(out_path, as_attachment=True)
        except Exception as e:
            return jsonify({'error': 'pdf generation failed', 'detail': str(e)}), 500

    if output_type == 'image':
        # create a simple image with translated text
        out_path += '.png'
        try:
            # naive: create white canvas and draw text
            img = Image.new('RGB', (1200, 1600), color='white')
            d = ImageDraw.Draw(img)
            # try to pick a default font
            try:
                font = ImageFont.truetype('arial.ttf', 20)
            except:
                font = ImageFont.load_default()

            y = 10
            for line in translated.split('\n'):
                d.text((10, y), line, fill=(0, 0, 0), font=font)
                y += 22
                if y > img.size[1] - 40:
                    break
            img.save(out_path)
            return send_file(out_path, as_attachment=True)
        except Exception as e:
            return jsonify({'error': 'image generation failed', 'detail': str(e)}), 500

    return jsonify({'error': 'unknown output type'}), 400

if __name__ == '__main__':
    # Set Tesseract path if on Windows
    if os.name == 'nt':  # Windows
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if not os.path.exists(tesseract_path):
            print(f"Error: Tesseract not found at {tesseract_path}")
            print("Please install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
            sys.exit(1)
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # Ensure upload and output directories exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    
    print("\n" + "="*50)
    print("OCR Translator API")
    print("="*50)
    print("Available endpoints:")
    print("  - http://localhost:5000/")
    print("  - http://localhost:5000/api/test")
    print("  - http://localhost:5000/api/translate (POST)")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')

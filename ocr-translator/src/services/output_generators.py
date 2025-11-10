from io import BytesIO
from pathlib import Path
from typing import Union
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont
import os

class OutputGenerator:
    """Base class for output generators"""
    
    @staticmethod
    def save_text(text: str, output_path: Union[str, Path]) -> None:
        """Save text to a file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    @staticmethod
    def create_pdf(text: str, output_path: Union[str, Path]) -> None:
        """Create a PDF file from text"""
        # Try to use a nice font if available
        try:
            font_path = os.path.join('static', 'fonts', 'DejaVuSans.ttf')
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('DejaVu', font_path))
                font_name = 'DejaVu'
            else:
                font_name = 'Helvetica'
        except:
            font_name = 'Helvetica'
        
        margin = 20 * mm
        line_height = 5 * mm
        
        c = canvas.Canvas(str(output_path), pagesize=A4)
        c.setFont(font_name, 10)
        
        width, height = A4
        width -= 2 * margin
        y = height - margin
        
        # Split text into paragraphs
        paragraphs = [p for p in text.split('\n') if p.strip()]
        
        for paragraph in paragraphs:
            # Simple text wrapping
            words = paragraph.split()
            line = []
            
            for word in words:
                # Check if adding this word would exceed the line width
                test_line = ' '.join(line + [word])
                if c.stringWidth(test_line, font_name, 10) <= width:
                    line.append(word)
                else:
                    # Draw the current line and start a new one
                    if line:
                        c.drawString(margin, y, ' '.join(line))
                        y -= line_height
                        line = [word]
                    
                    # Check if we need a new page
                    if y < margin:
                        c.showPage()
                        y = height - margin
                        c.setFont(font_name, 10)
            
            # Draw any remaining text in the current line
            if line:
                c.drawString(margin, y, ' '.join(line))
                y -= line_height
            
            # Add some space after each paragraph
            y -= line_height / 2
            
            # Check for page break
            if y < margin:
                c.showPage()
                y = height - margin
                c.setFont(font_name, 10)
        
        c.save()
    
    @staticmethod
    def create_image(text: str, output_path: Union[str, Path]) -> None:
        """Create an image with the translated text"""
        # Default image size (A4 at 72 DPI)
        width, height = 595, 842
        
        # Try to load a nice font
        try:
            # Try different font paths
            font_paths = [
                os.path.join('static', 'fonts', 'DejaVuSans.ttf'),
                'Arial.ttf',
                'arial.ttf',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
            ]
            
            font_size = 14
            font = None
            
            for path in font_paths:
                try:
                    font = ImageFont.truetype(path, font_size)
                    break
                except (IOError, OSError):
                    continue
            
            if font is None:
                font = ImageFont.load_default()
                font_size = 10
            
        except Exception as e:
            print(f"Font loading error: {e}")
            font = ImageFont.load_default()
            font_size = 10
        
        # Calculate required image height
        lines = []
        for paragraph in text.split('\n'):
            if not paragraph.strip():
                lines.append('')
                continue
                
            words = paragraph.split()
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                # Estimate text width (this is approximate)
                test_width = len(test_line) * (font_size * 0.6)
                
                if test_width < (width - 40):  # 20px margin on each side
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
        
        # Calculate required height
        line_height = int(font_size * 1.5)
        required_height = len(lines) * line_height + 40  # Add some padding
        
        # Create image with white background
        img = Image.new('RGB', (width, max(height, required_height)), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw text
        y = 20  # Start 20px from top
        for line in lines:
            if not line.strip():
                y += line_height
                continue
                
            draw.text((20, y), line, fill='black', font=font)
            y += line_height
        
        # Crop to content if needed
        if required_height < height:
            img = img.crop((0, 0, width, min(required_height, height)))
        
        # Save the image
        img.save(str(output_path))
        
    @classmethod
    def generate_output(cls, text: str, output_path: Union[str, Path], output_type: str = 'text') -> None:
        """Generate output in the specified format"""
        output_path = Path(output_path)
        
        if output_type == 'text':
            output_path = output_path.with_suffix('.txt')
            cls.save_text(text, output_path)
        elif output_type == 'pdf':
            output_path = output_path.with_suffix('.pdf')
            cls.create_pdf(text, output_path)
        elif output_type == 'image':
            output_path = output_path.with_suffix('.png')
            cls.create_image(text, output_path)
        else:
            raise ValueError(f"Unsupported output type: {output_type}")
        
        return output_path

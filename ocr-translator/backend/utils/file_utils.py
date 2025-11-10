import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from ..config import UPLOAD_FOLDER, OUTPUT_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def get_secure_filepath(filename):
    """Generate a secure file path for uploads"""
    if not filename:
        return None
    
    # Ensure filename is secure and unique
    filename = secure_filename(filename)
    unique_id = str(uuid.uuid4())
    return UPLOAD_FOLDER / f"{unique_id}_{filename}"

def cleanup_file(filepath, max_age_hours=24):
    """Cleanup old files from upload and output directories"""
    if not filepath or not filepath.exists():
        return
    
    try:
        filepath.unlink()
    except OSError:
        pass

def get_output_path(file_id, output_type):
    """Generate output file path based on type"""
    extensions = {
        'text': '.txt',
        'pdf': '.pdf',
        'image': '.png'
    }
    ext = extensions.get(output_type, '.txt')
    return OUTPUT_FOLDER / f"{file_id}_translated{ext}"

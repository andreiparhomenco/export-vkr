import subprocess
import os
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class ConversionError(Exception):
    """Custom exception for file conversion errors"""
    pass

def convert_docx_to_pdf(docx_path: str, out_dir: str) -> str:
    """
    Convert DOCX file to PDF using LibreOffice headless mode
    
    Args:
        docx_path: Path to the DOCX file
        out_dir: Output directory for the PDF
        
    Returns:
        Path to the generated PDF file
        
    Raises:
        ConversionError: If conversion fails
    """
    try:
        # Ensure output directory exists
        os.makedirs(out_dir, exist_ok=True)
        
        # Get the base filename without extension
        base_name = Path(docx_path).stem
        output_pdf = os.path.join(out_dir, f"{base_name}.pdf")
        
        # LibreOffice command for headless conversion
        cmd = [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", out_dir,
            docx_path
        ]
        
        logger.info(f"Converting DOCX to PDF: {docx_path}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            logger.error(f"LibreOffice conversion failed: {result.stderr}")
            raise ConversionError(f"DOCX conversion failed: {result.stderr}")
        
        if not os.path.exists(output_pdf):
            raise ConversionError(f"PDF file was not created: {output_pdf}")
        
        logger.info(f"Successfully converted DOCX to PDF: {output_pdf}")
        return output_pdf
        
    except subprocess.TimeoutExpired:
        logger.error(f"DOCX conversion timed out: {docx_path}")
        raise ConversionError("DOCX conversion timed out")
    except Exception as e:
        logger.error(f"Unexpected error during DOCX conversion: {str(e)}")
        raise ConversionError(f"DOCX conversion failed: {str(e)}")

def convert_image_to_pdf(img_path: str, out_path: str) -> str:
    """
    Convert image file to PDF using Pillow
    
    Args:
        img_path: Path to the image file
        out_path: Path for the output PDF file
        
    Returns:
        Path to the generated PDF file
        
    Raises:
        ConversionError: If conversion fails
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        
        logger.info(f"Converting image to PDF: {img_path}")
        
        # Open and convert image
        from PIL import Image  # Lazy import to avoid hard dependency at startup
        with Image.open(img_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(out_path, "PDF", resolution=300.0, quality=95)
        
        if not os.path.exists(out_path):
            raise ConversionError(f"PDF file was not created: {out_path}")
        
        logger.info(f"Successfully converted image to PDF: {out_path}")
        return out_path
        
    except Exception as e:
        logger.error(f"Image conversion failed: {str(e)}")
        raise ConversionError(f"Image conversion failed: {str(e)}")

def get_file_type(file_path: str) -> str:
    """
    Determine file type based on extension and file signature
    
    Args:
        file_path: Path to the file
        
    Returns:
        File type string
    """
    extension = Path(file_path).suffix.lower()
    
    if extension in ['.docx']:
        return 'docx'
    elif extension in ['.pdf']:
        return 'pdf'
    elif extension in ['.jpg', '.jpeg', '.png']:
        return 'image'
    else:
        return 'unknown'

def validate_file_size(file_path: str, max_size_mb: int = 100) -> bool:
    """
    Validate file size
    
    Args:
        file_path: Path to the file
        max_size_mb: Maximum file size in MB
        
    Returns:
        True if file size is valid, False otherwise
    """
    try:
        file_size = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024
        return file_size <= max_size_bytes
    except OSError:
        return False

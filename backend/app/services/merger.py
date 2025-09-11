import os
import logging
from pathlib import Path
from pypdf import PdfMerger, PdfReader
from typing import List, Optional

logger = logging.getLogger(__name__)

class MergeError(Exception):
    """Custom exception for PDF merging errors"""
    pass

def merge_pdfs(pdf_paths: List[str], out_path: str) -> str:
    """
    Merge multiple PDF files into a single PDF
    
    Args:
        pdf_paths: List of paths to PDF files to merge
        out_path: Path for the output merged PDF
        
    Returns:
        Path to the merged PDF file
        
    Raises:
        MergeError: If merging fails
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        
        logger.info(f"Merging {len(pdf_paths)} PDF files into: {out_path}")
        
        merger = PdfMerger()
        
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                logger.warning(f"PDF file not found, skipping: {pdf_path}")
                continue
                
            try:
                # Validate PDF file
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    if len(reader.pages) == 0:
                        logger.warning(f"Empty PDF file, skipping: {pdf_path}")
                        continue
                
                # Add PDF to merger
                merger.append(pdf_path)
                logger.info(f"Added PDF to merger: {pdf_path}")
                
            except Exception as e:
                logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
                # Continue with other files instead of failing completely
                continue
        
        # Write merged PDF
        merger.write(out_path)
        merger.close()
        
        # Validate output
        if not os.path.exists(out_path):
            raise MergeError(f"Merged PDF was not created: {out_path}")
        
        # Check if output file has content
        output_size = os.path.getsize(out_path)
        if output_size == 0:
            raise MergeError("Merged PDF is empty")
        
        logger.info(f"Successfully merged PDFs: {out_path} ({output_size} bytes)")
        return out_path
        
    except Exception as e:
        logger.error(f"PDF merging failed: {str(e)}")
        raise MergeError(f"PDF merging failed: {str(e)}")

def get_pdf_page_count(pdf_path: str) -> int:
    """
    Get the number of pages in a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Number of pages in the PDF
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            return len(reader.pages)
    except Exception as e:
        logger.error(f"Error reading PDF page count: {str(e)}")
        return 0

def validate_pdf(pdf_path: str) -> bool:
    """
    Validate that a file is a valid PDF
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        True if valid PDF, False otherwise
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            # Try to access pages to validate
            _ = len(reader.pages)
            return True
    except Exception as e:
        logger.error(f"PDF validation failed: {str(e)}")
        return False


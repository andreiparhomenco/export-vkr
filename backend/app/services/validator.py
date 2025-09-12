import os
import re
import logging
from typing import List, Tuple, Dict
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_files(file_list: List[Dict]) -> Tuple[List[str], List[str]]:
    """
    Validate uploaded files and return warnings and errors
    
    Args:
        file_list: List of file dictionaries with 'name' and 'type' keys
        
    Returns:
        Tuple of (warnings, errors)
    """
    warnings = []
    errors = []
    
    if not file_list:
        errors.append("No files uploaded")
        return warnings, errors
    
    # Check for required file types
    has_document = False
    has_title_page = False
    has_antiplagiarism = False
    
    for file_info in file_list:
        file_name = file_info.get('name', '').lower()
        file_type = file_info.get('type', '')
        
        # Check for document files
        if file_type in ['docx', 'pdf']:
            has_document = True
        
        # Check for title page (by filename)
        if any(keyword in file_name for keyword in ['titul', 'титул', 'title', 'титулник']):
            has_title_page = True
        
        # Check for antiplagiarism report
        if any(keyword in file_name for keyword in ['plag', 'antiplag', 'антиплаг', 'plagiarism']):
            has_antiplagiarism = True
    
    # Generate warnings for missing recommended files
    if not has_document:
        warnings.append("No document file found (docx/pdf)")
    
    if not has_title_page:
        warnings.append("No title page detected (look for files with 'titul', 'титул', 'title' in name)")
    
    if not has_antiplagiarism:
        warnings.append("No antiplagiarism report found (look for files with 'plag', 'antiplag' in name)")
    
    return warnings, errors

def validate_metadata(metadata: Dict) -> Tuple[List[str], List[str]]:
    """
    Validate metadata fields
    
    Args:
        metadata: Dictionary containing metadata fields
        
    Returns:
        Tuple of (warnings, errors)
    """
    warnings = []
    errors = []
    
    # Required fields validation
    if not metadata.get('title', '').strip():
        errors.append("Title is required")
    
    if not metadata.get('author', '').strip():
        errors.append("Author is required")
    
    # Year validation
    year = metadata.get('year')
    if year is None:
        errors.append("Year is required")
    else:
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 2000 or year_int > current_year + 1:
                warnings.append(f"Year {year_int} seems unusual (expected 2000-{current_year + 1})")
        except (ValueError, TypeError):
            errors.append("Year must be a valid number")
    
    # Title format validation
    title = metadata.get('title', '')
    if title and title.isupper():
        warnings.append("Title is in all caps - consider using proper case")
    
    # Author name validation
    author = metadata.get('author', '')
    if author and len(author.split()) < 2:
        warnings.append("Author name should include first and last name")
    
    return warnings, errors

def validate_file_order(file_order: List[str], available_files: List[Dict]) -> Tuple[List[str], List[str]]:
    """
    Validate file order and check for logical ordering
    
    Args:
        file_order: List of file IDs in desired order
        available_files: List of available file dictionaries
        
    Returns:
        Tuple of (warnings, errors)
    """
    warnings = []
    errors = []
    
    if not file_order:
        errors.append("No file order specified")
        return warnings, errors
    
    # Check if all files in order exist
    available_file_ids = {f.get('id') for f in available_files}
    for file_id in file_order:
        if file_id not in available_file_ids:
            errors.append(f"File ID {file_id} not found in uploaded files")
    
    # Check for logical ordering (title page should be first)
    if available_files:
        first_file = next((f for f in available_files if f.get('id') == file_order[0]), None)
        if first_file:
            first_file_name = first_file.get('name', '').lower()
            if not any(keyword in first_file_name for keyword in ['titul', 'титул', 'title']):
                warnings.append("Consider placing title page first in the order")
    
    return warnings, errors

def generate_validation_summary(warnings: List[str], errors: List[str]) -> Dict:
    """
    Generate a summary of validation results
    
    Args:
        warnings: List of warning messages
        errors: List of error messages
        
    Returns:
        Dictionary with validation summary
    """
    return {
        "has_errors": len(errors) > 0,
        "has_warnings": len(warnings) > 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "can_proceed": len(errors) == 0
    }





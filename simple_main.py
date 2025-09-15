#!/usr/bin/env python3
"""
Simple version of main.py for Railway deployment testing
"""
import os
import logging
import uuid
import tempfile
from typing import List
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pypdf
from PIL import Image
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VKR Export System MVP",
    description="Export graduate work to PDF format for electronic library upload",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "https://regal-raindrop-fa2af2.netlify.app",
        "https://*.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("=== VKR Export System Starting ===")
    logger.info(f"Python path: {os.environ.get('PYTHONPATH', 'Not set')}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info("VKR Export System started successfully")

# Global storage for sessions and files
sessions = {}

def get_file_type(filename: str) -> str:
    """Determine file type from extension"""
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    if ext in ['docx']:
        return 'docx'
    elif ext in ['pdf']:
        return 'pdf'
    elif ext in ['jpg', 'jpeg', 'png']:
        return 'image'
    else:
        return 'unknown'

def convert_docx_to_pdf(docx_path: str, output_dir: str) -> str:
    """Convert DOCX to PDF using LibreOffice"""
    try:
        base_name = Path(docx_path).stem
        output_pdf = os.path.join(output_dir, f"{base_name}.pdf")
        
        logger.info(f"Converting DOCX: {docx_path} -> {output_pdf}")
        
        # Try LibreOffice first
        cmd = [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            docx_path
        ]
        
        logger.info(f"Running LibreOffice command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        logger.info(f"LibreOffice result: returncode={result.returncode}, stdout={result.stdout}, stderr={result.stderr}")
        
        if result.returncode == 0 and os.path.exists(output_pdf):
            logger.info(f"Successfully converted DOCX to PDF using LibreOffice: {output_pdf}")
            return output_pdf
        else:
            # Fallback to docx2pdf
            logger.info("LibreOffice failed, trying docx2pdf fallback")
            try:
                from docx2pdf import convert
                convert(docx_path, output_pdf)
                logger.info(f"Successfully converted DOCX to PDF using docx2pdf: {output_pdf}")
                return output_pdf
            except Exception as e2:
                logger.error(f"docx2pdf also failed: {str(e2)}")
                raise Exception(f"Both LibreOffice and docx2pdf failed. LibreOffice: {result.stderr}, docx2pdf: {str(e2)}")
            
    except Exception as e:
        logger.error(f"Failed to convert DOCX to PDF: {str(e)}", exc_info=True)
        raise Exception(f"Failed to convert DOCX: {str(e)}")

def convert_image_to_pdf(image_path: str, output_pdf: str):
    """Convert image to PDF"""
    try:
        logger.info(f"Converting image: {image_path} -> {output_pdf}")
        
        with Image.open(image_path) as img:
            logger.info(f"Image info: size={img.size}, mode={img.mode}, format={img.format}")
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                logger.info(f"Converting image mode from {img.mode} to RGB")
                img = img.convert('RGB')
            
            img.save(output_pdf, 'PDF')
            logger.info(f"Successfully converted image to PDF: {output_pdf}")
    except Exception as e:
        logger.error(f"Failed to convert image to PDF: {str(e)}", exc_info=True)
        raise Exception(f"Failed to convert image: {str(e)}")

def merge_pdfs(pdf_paths: List[str], output_path: str):
    """Merge multiple PDFs into one"""
    try:
        logger.info(f"Merging PDFs: {pdf_paths} -> {output_path}")
        
        merger = pypdf.PdfMerger()
        
        for i, pdf_path in enumerate(pdf_paths):
            if os.path.exists(pdf_path):
                logger.info(f"Adding PDF {i+1}/{len(pdf_paths)}: {pdf_path}")
                merger.append(pdf_path)
            else:
                logger.warning(f"PDF file not found: {pdf_path}")
        
        with open(output_path, 'wb') as output_file:
            merger.write(output_file)
        
        merger.close()
        logger.info(f"Successfully merged PDFs to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to merge PDFs: {str(e)}", exc_info=True)
        raise Exception(f"Failed to merge PDFs: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VKR Export System MVP", 
        "version": "1.0.0",
        "status": "running",
        "service": "vkr-export-api"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "vkr-export-api",
        "version": "1.0.0"
    }

@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload endpoint - simplified version"""
    session_id = str(uuid.uuid4())
    
    # Create temporary directory for this session
    temp_dir = tempfile.mkdtemp()
    sessions[session_id] = {
        "temp_dir": temp_dir,
        "files": []
    }
    
    # Process uploaded files
    uploaded_files = []
    for file in files:
        # Read file content
        content = await file.read()
        
        # Save file to temporary directory
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Determine file type
        file_type = get_file_type(file.filename)
        
        file_info = {
            "id": str(uuid.uuid4()),
            "name": file.filename,
            "type": file_type,
            "size": len(content),
            "path": file_path
        }
        
        uploaded_files.append(file_info)
        sessions[session_id]["files"].append(file_info)
    
    return {
        "session_id": session_id,
        "files": uploaded_files,
        "message": f"Uploaded {len(uploaded_files)} files successfully",
        "status": "ok"
    }

@app.post("/api/prepare")
async def prepare_export(request_data: dict):
    """Prepare export endpoint - process files and create PDF"""
    try:
        logger.info(f"Prepare export request: {request_data}")
        
        session_id = request_data.get("session_id")
        files = request_data.get("files", [])
        metadata = request_data.get("metadata", {})
        
        logger.info(f"Session ID: {session_id}")
        logger.info(f"Files count: {len(files)}")
        logger.info(f"Available sessions: {list(sessions.keys())}")
        
        if session_id not in sessions:
            logger.error(f"Session {session_id} not found in {list(sessions.keys())}")
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[session_id]
        temp_dir = session["temp_dir"]
        logger.info(f"Using temp directory: {temp_dir}")
        
        # Create output directory
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Created output directory: {output_dir}")
        
        # Process files in order
        pdf_paths = []
        
        for i, file_info in enumerate(files):
            logger.info(f"Processing file {i+1}/{len(files)}: {file_info}")
            
            file_id = file_info["id"]
            file_path = None
            file_type = None
            
            # Find file path
            for f in session["files"]:
                if f["id"] == file_id:
                    file_path = f["path"]
                    file_type = f["type"]
                    break
            
            logger.info(f"File path: {file_path}, type: {file_type}")
            
            if not file_path or not os.path.exists(file_path):
                logger.warning(f"File not found or doesn't exist: {file_path}")
                continue
            
            try:
                if file_type == "pdf":
                    # PDF files - use directly
                    logger.info(f"Using PDF directly: {file_path}")
                    pdf_paths.append(file_path)
                elif file_type == "docx":
                    # Convert DOCX to PDF
                    logger.info(f"Converting DOCX to PDF: {file_path}")
                    pdf_path = convert_docx_to_pdf(file_path, output_dir)
                    pdf_paths.append(pdf_path)
                elif file_type == "image":
                    # Convert image to PDF
                    logger.info(f"Converting image to PDF: {file_path}")
                    pdf_path = os.path.join(output_dir, f"{Path(file_path).stem}.pdf")
                    convert_image_to_pdf(file_path, pdf_path)
                    pdf_paths.append(pdf_path)
                else:
                    logger.warning(f"Unknown file type: {file_type}")
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
                continue
        
        logger.info(f"Successfully processed {len(pdf_paths)} files: {pdf_paths}")
        
        # Merge all PDFs
        export_id = str(uuid.uuid4())
        final_pdf_path = os.path.join(output_dir, f"export_{export_id}.pdf")
        
        if pdf_paths:
            logger.info(f"Merging PDFs to: {final_pdf_path}")
            merge_pdfs(pdf_paths, final_pdf_path)
        else:
            logger.error("No valid files to process")
            raise HTTPException(status_code=400, detail="No valid files to process")
        
        # Store export info
        session["export_id"] = export_id
        session["final_pdf_path"] = final_pdf_path
        session["metadata"] = metadata
        
        logger.info(f"Export prepared successfully: {export_id}")
        
        return {
            "export_id": export_id,
            "status": "prepared",
            "message": f"Successfully processed {len(pdf_paths)} files into PDF"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prepare export error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to prepare export: {str(e)}")

@app.get("/api/download/{export_id}")
async def download_pdf(export_id: str):
    """Download PDF endpoint - return real PDF"""
    try:
        # Find session with this export_id
        pdf_path = None
        for session_id, session in sessions.items():
            if session.get("export_id") == export_id:
                pdf_path = session.get("final_pdf_path")
                break
        
        if not pdf_path or not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="PDF not found")
        
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"export_{export_id}.pdf",
            headers={"Content-Disposition": f"attachment; filename=export_{export_id}.pdf"}
        )
        
    except Exception as e:
        logger.error(f"Download PDF error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download PDF: {str(e)}")

@app.get("/api/metadata/{export_id}")
async def download_metadata(export_id: str):
    """Download metadata endpoint - return real metadata"""
    try:
        # Find session with this export_id
        metadata = None
        for session_id, session in sessions.items():
            if session.get("export_id") == export_id:
                metadata = session.get("metadata", {})
                break
        
        if metadata is None:
            raise HTTPException(status_code=404, detail="Metadata not found")
        
        # Add export_id to metadata
        metadata["export_id"] = export_id
        
        from fastapi.responses import JSONResponse
        return JSONResponse(
            content=metadata,
            headers={"Content-Disposition": f"attachment; filename=metadata_{export_id}.json"}
        )
        
    except Exception as e:
        logger.error(f"Download metadata error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download metadata: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

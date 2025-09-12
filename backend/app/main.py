import os
import uuid
import json
import logging
from typing import List, Dict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .models import (
    UploadResponse, PrepareRequest, PrepareResponse, 
    Session as SessionModel, Export, ProcessingStatus
)
from .db import get_session, init_db
from .services.converter import convert_docx_to_pdf, convert_image_to_pdf, get_file_type
from .services.merger import merge_pdfs
from .services.validator import validate_files, validate_metadata, validate_file_order

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
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
        "https://*.netlify.app"  # Allow all Netlify subdomains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting VKR Export System...")
    init_db()
    logger.info("Database initialized successfully")
    logger.info("VKR Export System started successfully")

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DATA_ROOT = BASE_DIR / "data"
UPLOAD_ROOT = DATA_ROOT / "uploads"
EXPORT_ROOT = DATA_ROOT / "exports"
MAX_FILE_SIZE_MB = 100

# Ensure directories exist
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

@app.post("/api/upload", response_model=UploadResponse)
async def upload_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_session)
):
    """Upload files and create a new session"""
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Create new session
        session_id = str(uuid.uuid4())
        session_dir = UPLOAD_ROOT / session_id
        session_dir.mkdir(exist_ok=True)
        
        # Create session record in database
        db_session = SessionModel(session_id=session_id)
        db.add(db_session)
        db.commit()
        
        file_records = []
        
        for file in files:
            # Save file
            file_path = session_dir / file.filename
            content = await file.read()

            # Validate file size
            if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} exceeds size limit of {MAX_FILE_SIZE_MB}MB"
                )

            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            # Determine file type
            file_type = get_file_type(str(file_path))
            
            # Create file record
            file_record = {
                "id": str(uuid.uuid4()),
                "name": file.filename,
                "type": file_type,
                "path": str(file_path),
                "size": len(content)
            }
            file_records.append(file_record)
        
        # Save file index
        index_path = session_dir / "index.json"
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump({"files": file_records}, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Uploaded {len(files)} files for session {session_id}")
        
        return UploadResponse(
            session_id=session_id,
            files=[{"id": r["id"], "name": r["name"], "type": r["type"]} for r in file_records]
        )
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/{session_id}")
async def get_files(session_id: str):
    """Get files for a session"""
    try:
        session_dir = UPLOAD_ROOT / session_id
        index_path = session_dir / "index.json"
        
        if not index_path.exists():
            raise HTTPException(status_code=404, detail="Session not found")
        
        with open(index_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return data
        
    except Exception as e:
        logger.error(f"Get files error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/prepare", response_model=PrepareResponse)
async def prepare_export(
    request: PrepareRequest,
    db: Session = Depends(get_session)
):
    """Prepare and generate the final PDF export"""
    try:
        session_id = request.session_id
        session_dir = UPLOAD_ROOT / session_id
        
        if not session_dir.exists():
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Load file index
        index_path = session_dir / "index.json"
        with open(index_path, "r", encoding="utf-8") as f:
            index_data = json.load(f)
        
        files = index_data["files"]
        
        # Validate file order
        file_order_warnings, file_order_errors = validate_file_order(request.order, files)
        if file_order_errors:
            raise HTTPException(status_code=400, detail=f"File order validation failed: {file_order_errors}")
        
        # Validate metadata
        metadata_warnings, metadata_errors = validate_metadata(request.metadata.dict())
        if metadata_errors:
            raise HTTPException(status_code=400, detail=f"Metadata validation failed: {metadata_errors}")
        
        # Validate files
        file_warnings, file_errors = validate_files(files)
        if file_errors:
            raise HTTPException(status_code=400, detail=f"File validation failed: {file_errors}")
        
        # Combine all warnings
        all_warnings = file_order_warnings + metadata_warnings + file_warnings
        
        # Create file ID to file mapping
        id_to_file = {f["id"]: f for f in files}
        
        # Process files in parallel
        export_id = str(uuid.uuid4())
        temp_pdf_paths = []
        
        def process_file(file_id: str) -> str:
            if file_id not in id_to_file:
                raise ValueError(f"File ID {file_id} not found")
            
            file_info = id_to_file[file_id]
            file_path = file_info["path"]
            file_type = file_info["type"]
            
            if file_type == "pdf":
                return file_path
            elif file_type == "docx":
                # Convert DOCX to PDF
                pdf_path = convert_docx_to_pdf(file_path, str(session_dir))
                return pdf_path
            elif file_type == "image":
                # Convert image to PDF
                pdf_path = file_path + ".pdf"
                convert_image_to_pdf(file_path, pdf_path)
                return pdf_path
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_file = {executor.submit(process_file, file_id): file_id for file_id in request.order}
            
            for future in as_completed(future_to_file):
                try:
                    pdf_path = future.result()
                    temp_pdf_paths.append(pdf_path)
                except Exception as e:
                    logger.error(f"File processing failed: {str(e)}")
                    raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")
        
        # Merge PDFs
        output_pdf = EXPORT_ROOT / f"export_{export_id}.pdf"
        merge_pdfs(temp_pdf_paths, str(output_pdf))
        
        # Create metadata record
        metadata_record = {
            "export_id": export_id,
            "session_id": session_id,
            "metadata": request.metadata.dict(),
            "files": [id_to_file[fid]["name"] for fid in request.order],
            "warnings": all_warnings,
            "created_at": str(uuid.uuid4())  # This should be datetime, but keeping simple for now
        }
        
        # Save metadata
        metadata_path = EXPORT_ROOT / f"export_{export_id}.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata_record, f, ensure_ascii=False, indent=2)
        
        # Save to database
        export_record = Export(
            export_id=export_id,
            session_id=session_id,
            pdf_path=str(output_pdf),
            metadata_json=json.dumps(metadata_record, ensure_ascii=False),
            warnings=json.dumps(all_warnings, ensure_ascii=False) if all_warnings else None
        )
        db.add(export_record)
        db.commit()
        
        logger.info(f"Export created successfully: {export_id}")
        
        return PrepareResponse(
            export_id=export_id,
            pdf_url=f"/api/download/{export_id}",
            metadata_url=f"/api/metadata/{export_id}",
            warnings=all_warnings
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prepare export error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{export_id}")
async def download_pdf(export_id: str):
    """Download the generated PDF"""
    try:
        pdf_path = EXPORT_ROOT / f"export_{export_id}.pdf"
        
        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="Export not found")
        
        return FileResponse(
            path=str(pdf_path),
            filename=f"export_{export_id}.pdf",
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metadata/{export_id}")
async def get_metadata(export_id: str):
    """Get metadata for an export"""
    try:
        metadata_path = EXPORT_ROOT / f"export_{export_id}.json"
        
        if not metadata_path.exists():
            raise HTTPException(status_code=404, detail="Metadata not found")
        
        return FileResponse(
            path=str(metadata_path),
            filename=f"export_{export_id}.json",
            media_type="application/json"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Metadata error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "VKR Export System MVP", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if data directories exist
        if not DATA_ROOT.exists():
            DATA_ROOT.mkdir(parents=True, exist_ok=True)
        if not UPLOAD_ROOT.exists():
            UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
        if not EXPORT_ROOT.exists():
            EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
        
        return {
            "status": "healthy", 
            "service": "vkr-export-api",
            "timestamp": str(uuid.uuid4()),
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

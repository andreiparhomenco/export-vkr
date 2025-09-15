#!/usr/bin/env python3
"""
Simple version of main.py for Railway deployment testing
"""
import os
import logging
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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
    import uuid
    
    # Create a mock response that matches what frontend expects
    session_id = str(uuid.uuid4())
    
    # Process uploaded files
    uploaded_files = []
    for file in files:
        # Read file content to get size
        content = await file.read()
        
        # Determine file type from extension
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else 'unknown'
        
        uploaded_files.append({
            "id": str(uuid.uuid4()),
            "name": file.filename,
            "type": file_extension,
            "size": len(content)
        })
    
    return {
        "session_id": session_id,
        "files": uploaded_files,
        "message": f"Uploaded {len(uploaded_files)} files successfully",
        "status": "ok"
    }

@app.post("/api/prepare")
async def prepare_export():
    """Prepare export endpoint - simplified version"""
    import uuid
    
    export_id = str(uuid.uuid4())
    
    return {
        "export_id": export_id,
        "status": "prepared",
        "message": "Export prepared successfully"
    }

@app.get("/api/download/{export_id}")
async def download_pdf(export_id: str):
    """Download PDF endpoint - simplified version"""
    # Return a simple text response for now
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(
        content="Mock PDF content - this is a placeholder",
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=export_{export_id}.pdf"}
    )

@app.get("/api/metadata/{export_id}")
async def download_metadata(export_id: str):
    """Download metadata endpoint - simplified version"""
    import json
    
    mock_metadata = {
        "export_id": export_id,
        "title": "Test VKR Title",
        "author": "Test Author",
        "year": 2024,
        "supervisor": "Test Supervisor",
        "faculty": "Test Faculty",
        "form_of_study": "full-time"
    }
    
    from fastapi.responses import JSONResponse
    return JSONResponse(
        content=mock_metadata,
        headers={"Content-Disposition": f"attachment; filename=metadata_{export_id}.json"}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

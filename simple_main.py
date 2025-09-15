#!/usr/bin/env python3
"""
Simple version of main.py for Railway deployment testing
"""
import os
import logging
from fastapi import FastAPI
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
async def upload_files():
    """Upload endpoint - simplified version"""
    return {"message": "Upload endpoint is working", "status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

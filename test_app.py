#!/usr/bin/env python3
"""
Simple test FastAPI app for Railway deployment
"""
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="VKR Test App", version="1.0.0")

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

logger.info("=== Test App Starting ===")
logger.info(f"Port: {os.environ.get('PORT', '8000')}")
logger.info(f"Python path: {os.environ.get('PYTHONPATH', 'Not set')}")

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "VKR Test App is running", "status": "ok", "port": os.environ.get('PORT', '8000')}

@app.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {
        "status": "healthy", 
        "service": "vkr-test",
        "port": os.environ.get('PORT', '8000'),
        "cors": "enabled"
    }

@app.get("/test")
async def test():
    logger.info("Test endpoint called")
    return {"test": "success", "port": os.environ.get('PORT', '8000')}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

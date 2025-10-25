# Python and Flask 
# Phase 1: Core Architecture and Data modeling
# building the API - Using Fast API

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from fastapi.staticfiles import StaticFiles
from services.image_service import ImageService
import uuid

import uvicorn
from pathlib import Path
import uvicorn
import uuid

from models import DesignRequest, DesignResponse
from config import get_settings
from services.pkg_service import pkg_service

app = FastAPI(
    title="Agentic Design Architect API",
    description="Geometric + Economic AI Design System",
    version="1.0.0"
)


# CORS for your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Ensure upload directory exists
Path(settings.upload_dir).mkdir(exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

@app.get("/")
async def root():
    return {
        "status": "operational",
        "service": "Agentic Design Architect",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload constraint image and return public URL
    This URL will be used in ControlNet API call
    """
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Validate and resize
        processed_image = ImageService.validate_and_resize(contents)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'png'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Upload to ImgBB and get public URL
        public_url = ImageService.upload_to_imgbb(processed_image, unique_filename)
        
        return {
            "success": True,
            "url": public_url,
            "filename": unique_filename,
            "message": "Image uploaded successfully"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/pkg/stats")
async def get_pkg_stats():
    """Get Product Knowledge Graph statistics"""
    return pkg_service.get_graph_stats()

@app.post("/pkg/query")
async def query_products(request: DesignRequest):
    """Query compatible products from PKG"""
    products = pkg_service.get_compatible_products(
        room_type=request.room_type.value,
        room_size=request.room_size,
        style_preference="modern",
        max_results=5
    )
    
    return {
        "query": {
            "room_type": request.room_type,
            "room_size": request.room_size,
            "style": request.style_preferences
        },
        "products": products,
        "count": len(products)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# Python and Flask 
# Phase 1: Core Architecture and Data modeling
# building the API - Using Fast API# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path

from models import DesignRequest, DesignResponse
from config import get_settings

app = FastAPI(
    title="Arcana",
    description="Geometric + Economic AI Design System that generates interior designs and optimizes product selections using multi-agent negotiation.",
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

# Ensure upload directory exists
Path(settings.upload_dir).mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {
        "status": "operational",
        "service": "Arcana Backend API, Agentic based Interior Design",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# We'll add endpoints here in Phase II

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
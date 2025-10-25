# Python and Flask 
# Phase 2: Multi-Agent Architecture Integration
# Updated API to use Orchestrator pattern

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

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

# Import the orchestrator
from agents.orchestrator import orchestrator


app = FastAPI(
    title="Arcana: Multi-Agent Design Architect API",
    description="AI-Powered Interior Design using Multi-Agent Orchestration",
    version="2.0.0"
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
        "service": "Arcana - Multi-Agent Design Architect",
        "version": "2.0.0",
        "architecture": "Orchestrator-Worker Pattern with 4 Specialized Agents"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "multi_agent": True}

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
        max_results=10  # Increased for more agent options
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


# Response model for multi-agent design
class MultiAgentDesignResponse(BaseModel):
    """Response from multi-agent orchestration"""
    success: bool
    control_params: Dict[str, Any]
    reasoning: str
    product_justification: str
    agent_outputs: Dict[str, Any]
    confidence_scores: Dict[str, float]
    error: Optional[str] = None


@app.post("/agent/design/multi", response_model=MultiAgentDesignResponse)
async def generate_design_with_multi_agent(request: DesignRequest):
    """ Multi-Agent Design Orchestration Pipeline
    
    Uses 5-agent architecture:
    1. Lead Orchestrator (Claude Opus 4) - coordinates workflow
    2. Style Analysis Agent (Claude Sonnet 4) - extracts aesthetic preferences  
    3. Product Recommendation Agent (Claude Sonnet 4) - selects furniture from PKG
    4. Layout Optimization Agent (Claude Sonnet 4) - spatial planning
    5. Budget Management Agent (Claude Sonnet 4) - cost optimization
    
    This endpoint demonstrates the orchestrator-worker pattern recommended by Anthropic
    for complex, multi-step reasoning tasks.
    """
    try:
        # Step 1: Get products from PKG
        products = pkg_service.get_compatible_products(
            room_type=request.room_type.value,
            room_size=request.room_size,
            style_preference="modern",
            max_results=10
        )
        
        if not products:
            raise HTTPException(status_code=404, detail="No compatible products found in PKG")
        
        # Step 2: Mock image URL (in production, this comes from upload endpoint)
        mock_image_url = "https://i.ibb.co/placeholder.png"
        
        # Step 3: Convert request to dict for orchestrator
        user_request = {
            "prompt": request.prompt,
            "room_type": request.room_type.value,
            "room_size": request.room_size,
            "style_preferences": request.style_preferences or [],
            "budget_max": request.budget_max
        }
        
        # Step 4: Call the orchestrator to coordinate all agents
        print("\n" + "="*60)
        print("STARTING MULTI-AGENT ORCHESTRATION")
        print("="*60 + "\n")
        
        products_dict = [prod.model_dump() for prod in products]

        design_result = orchestrator.orchestrate_design(
            user_request=user_request,
            control_image_url=mock_image_url,
            available_products=products_dict
        )
        
        print("\n" + "="*60)
        print("ORCHESTRATION COMPLETE")
        print("="*60 + "\n")
        
        if not design_result.get("success", False):
            raise HTTPException(
                status_code=500, 
                detail=f"Orchestration failed: {design_result.get('error', 'Unknown error')}"
            )
        
        return design_result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Design generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Design generation failed: {str(e)}")


# Keep the old single-agent endpoint for comparison
@app.post("/agent/design/single")
async def generate_design_single_agent(request: DesignRequest):
    """
    Legacy single-agent endpoint (for comparison)
    Uses the original AnthropicDesignAgent
    """
    from agents.anthropic_agent import design_agent
    
    products = pkg_service.get_compatible_products(
        room_type=request.room_type.value,
        room_size=request.room_size,
        style_preference="modern",
        max_results=5
    )
    
    if not products:
        raise HTTPException(status_code=404, detail="No compatible products found")
    
    mock_image_url = "https://i.ibb.co/placeholder.png"
    
    try:
        design_response = design_agent.generate_design(
            user_request=request,
            control_image_url=mock_image_url,
            available_products=products
        )
        
        return design_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent failed: {str(e)}")


@app.get("/agent/test")
async def test_agent_connections():
    """Test if all agents are properly initialized"""
    from agents.style_agent import style_agent
    from agents.product_agent import product_agent
    from agents.layout_agent import layout_agent
    from agents.budget_agent import budget_agent
    
    return {
        "orchestrator": "initialized",
        "workers": {
            "style_agent": style_agent.agent_name,
            "product_agent": product_agent.agent_name,
            "layout_agent": layout_agent.agent_name,
            "budget_agent": budget_agent.agent_name
        },
        "status": "operational",
        "architecture": "Multi-Agent Orchestrator Pattern"
    }
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
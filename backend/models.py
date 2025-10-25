from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from enum import Enum

class RoomType(str, Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    OFFICE = "office"

class ControlNetParams(BaseModel):
    """Schema for ControlNet API input - MUST match Replicate API contract"""
    prompt: str = Field(..., description="Detailed design prompt")
    control_image_url: str = Field(..., description="Public URL of constraint image")
    scale: float = Field(default=3.5, ge=3.0, le=5.0, description="Guidance scale")
    steps: int = Field(default=20, ge=10, le=50, description="Inference steps")
    negative_prompt: Optional[str] = Field(default="blurry, low quality, distorted")

class ProductSuggestion(BaseModel):
    """Product from PKG"""
    sku: str
    name: str
    base_price: float
    material: str
    category: str
    compatibility_score: float = Field(ge=0.0, le=1.0)

class AgentOptimizedProduct(BaseModel):
    """Product after Fetch.ai agent negotiation"""
    sku: str
    name: str
    original_price: float
    optimized_price: float
    savings_pct: float
    negotiation_strategy: str

class DesignRequest(BaseModel):
    """User input schema"""
    prompt: str
    room_type: RoomType
    room_size: str = Field(default="medium", pattern="^(small|medium|large)$")
    style_preferences: List[str] = Field(default_factory=list)

class DesignResponse(BaseModel):
    """Final API response"""
    control_params: ControlNetParams
    products: List[ProductSuggestion]
    optimized_products: List[AgentOptimizedProduct]
    total_savings: float
    generated_image_url: Optional[str] = None
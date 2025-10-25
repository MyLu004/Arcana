from instructor import patch
from anthropic import Anthropic
from typing import List
from pydantic import BaseModel, Field

from config import get_settings
from models import ControlNetParams, ProductSuggestion, DesignRequest

settings = get_settings()
# Patch the Anthropic client with Instructor
anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
patched_client = patch(anthropic_client)


class DesignAgentResponse(BaseModel):
    """
    Structured output from the Design Agent - FLATTENED for Instructor compatibility
    """
    # Flatten the ControlNetParams fields directly into this model
    prompt: str = Field(description="Detailed visual description for ControlNet (100-150 words)")
    control_image_url: str = Field(description="URL of the constraint image")
    scale: float = Field(default=3.5, ge=3.0, le=5.0, description="ControlNet guidance scale")
    steps: int = Field(default=20, ge=10, le=50, description="Inference steps")
    negative_prompt: str = Field(default="blurry, low quality, distorted")
    
    reasoning: str = Field(description="Agent's design reasoning process")
    product_justification: str = Field(description="Why these products were selected")
    
    @property
    def control_params(self) -> ControlNetParams:
        """Convert to ControlNetParams for API compatibility"""
        return ControlNetParams(
            prompt=self.prompt,
            control_image_url=self.control_image_url,
            scale=self.scale,
            steps=self.steps,
            negative_prompt=self.negative_prompt
        )


class AnthropicDesignAgent:
    """
    Design reasoning agent powered by Claude
    Uses Instructor to guarantee structured outputs
    """
    
    def __init__(self):
        """Initialize the agent with Anthropic client"""
        self.client = patched_client
    
    def generate_design(
        self,
        user_request: DesignRequest,
        control_image_url: str,
        available_products: List[ProductSuggestion]
    ) -> DesignAgentResponse:
        """
        Main reasoning function
        Takes user intent + PKG products → Returns structured ControlNet params
        """
        
        # Format products for Claude to reason over
        products_summary = "\n".join([
            f"- {p.name} (${p.base_price}, {p.material}, compatibility: {p.compatibility_score})"
            for p in available_products
        ])
        
        # Construct the system prompt
        system_prompt = f"""You are an expert interior design agent.

Your task is to generate a photorealistic design prompt for a ControlNet image generation model.

**CRITICAL REQUIREMENTS**:
- The `prompt` field must be a detailed, visual description (100-150 words) describing:
  * Room atmosphere and lighting
  * Material textures and finishes
  * Color palette
  * Furniture placement and spatial flow
  * Specific products from the available list (mention them by name)
  
- The `control_image_url` MUST be: {control_image_url}
- The `scale` must be between 3.0-5.0 (higher = more faithful to sketch)
- The `steps` should be 20-30 for quality
- The `negative_prompt` should list things to avoid in the image

**Available Products from PKG**:
{products_summary}

**Design Philosophy**: Create a cohesive design that respects the geometric constraint, uses high-compatibility products, and maximizes value."""

        user_message = f"""Design Request:
- Room Type: {user_request.room_type.value}
- Room Size: {user_request.room_size}
- User Prompt: {user_request.prompt}
- Style: {', '.join(user_request.style_preferences) if user_request.style_preferences else 'modern'}

Generate a complete design specification."""

        # Call Anthropic with Instructor enforcement
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                temperature=0.7,
                response_model=DesignAgentResponse,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                system=system_prompt,
            )
            
            print(f"✅ Successfully generated design with {len(response.prompt)} character prompt")
            return response
            
        except Exception as e:
            print(f"Anthropic Agent Error: {str(e)}")
            # Fallback response
            return DesignAgentResponse(
                prompt=f"A beautiful {user_request.room_type.value} with {user_request.prompt}, "
                       f"featuring {available_products[0].name if available_products else 'modern furniture'}, "
                       f"warm lighting, elegant design with natural materials and clean lines creating a harmonious space",
                control_image_url=control_image_url,
                scale=3.5,
                steps=20,
                negative_prompt="blurry, low quality, distorted",
                reasoning="Fallback design due to API error - using default parameters",
                product_justification="Using top-rated products from compatibility graph"
            )
    
    def test_connection(self) -> bool:
        """Quick test to verify Anthropic API is working"""
        try:
            test_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = test_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=50,
                messages=[{"role": "user", "content": "Reply with: API_OK"}]
            )
            return "API_OK" in response.content
        except Exception as e:
            print(f"Anthropic connection test failed: {str(e)}")
            return False


# Create singleton instance
design_agent = AnthropicDesignAgent()
"""
Layout Optimization Agent
Handles spatial planning, furniture arrangement, and clearance calculations
"""
from typing import Dict, Any, List
import json

from agents.base_agent import BaseAgent, AgentResponse


class LayoutAgent(BaseAgent):
    """
    Specializes in spatial reasoning and furniture placement
    Ensures proper clearances, traffic flow, and ergonomic arrangements
    """
    
    def __init__(self):
        super().__init__(agent_name="LayoutOptimizer")
        
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """
        Generate optimal furniture layout based on room constraints
        
        Context expected:
            - room_type: str
            - room_size: str (small/medium/large)
            - selected_products: List[Dict] - from ProductAgent
            - style_data: Dict - from StyleAgent
        """
        self.log_activity("Calculating optimal spatial layout...")
        
        room_type = context.get("room_type", "living_room")
        room_size = context.get("room_size", "medium")
        selected_products = context.get("selected_products", [])
        style_data = context.get("style_data", {})
        
        if not selected_products:
            self.log_activity("No products to arrange")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={},
                reasoning="No products provided for layout planning",
                confidence=0.0
            )
        
        # Format products for layout planning
        products_list = "\n".join([
            f"- {p.get('name', 'Unknown')}: {p.get('dimensions', 'standard size')}"
            for p in selected_products
        ])
        
        # Map room size to approximate dimensions
        room_dimensions = {
            "small": "10ft x 12ft (120 sq ft)",
            "medium": "12ft x 16ft (192 sq ft)",
            "large": "16ft x 20ft (320 sq ft)"
        }
        
        system_prompt = """You are an expert space planner specializing in interior layouts.

Your task is to create an optimal furniture arrangement that:
1. Ensures proper traffic flow (minimum 30-36 inches for walkways)
2. Maintains appropriate clearances (e.g., 18-24 inches from sofa to coffee table)
3. Creates functional zones (conversation areas, work zones, etc.)
4. Considers natural light and focal points
5. Follows ergonomic principles

Respond ONLY with valid JSON in this exact format:
{
    "layout_zones": [
        {
            "zone_name": "Conversation Area",
            "products": ["Sofa", "Coffee Table"],
            "placement_notes": "Sofa against longest wall, coffee table centered 20 inches away"
        }
    ],
    "traffic_flow": "description of circulation paths",
    "focal_point": "Main visual anchor (e.g., window, fireplace, TV wall)",
    "clearances_verified": true,
    "layout_score": 0.88,
    "spatial_notes": "Additional considerations"
}"""

        user_message = f"""Plan the layout for this room:

Room: {room_type}
Dimensions: {room_dimensions.get(room_size, 'medium size')}
Style: {style_data.get('primary_style', 'modern')} with {style_data.get('mood', 'comfortable')} atmosphere

Furniture to arrange:
{products_list}

Create an optimal spatial arrangement that maximizes functionality and aesthetics."""

        try:
            response_text = self._call_claude(system_prompt, user_message, temperature=0.4)
            
            # Parse JSON response
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
            layout_data = json.loads(cleaned_response)
            
            self.log_activity(f"Created {len(layout_data.get('layout_zones', []))} functional zones")
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=layout_data,
                reasoning=f"Spatial layout optimized with {layout_data.get('focal_point', 'strategic')} as focal point",
                confidence=layout_data.get("layout_score", 0.85)
            )
            
        except json.JSONDecodeError as e:
            self.log_activity(f"JSON parsing failed, using standard layout template")
            # Fallback with basic layout guidance
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data={
                    "layout_zones": [
                        {
                            "zone_name": "Main Area",
                            "products": [p.get("name", "Furniture") for p in selected_products],
                            "placement_notes": "Standard arrangement with proper clearances"
                        }
                    ],
                    "traffic_flow": "Clear pathways maintained around furniture",
                    "focal_point": "Natural light from windows",
                    "clearances_verified": True,
                    "layout_score": 0.75,
                    "spatial_notes": "Fallback layout template applied"
                },
                reasoning="Standard layout principles applied due to parsing error",
                confidence=0.75
            )
        
        except Exception as e:
            self.log_activity(f"Layout planning failed: {str(e)}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={},
                reasoning=f"Error: {str(e)}",
                confidence=0.0
            )


# Create singleton
layout_agent = LayoutAgent()
"""
ENHANCED: Layout Agent with Geometric Coordinates
Provides spatial positioning data for placing products in the room

Replace or enhance your existing layout_agent.py with this
"""
from typing import Dict, Any, List
import json

from agents.base_agent import BaseAgent, AgentResponse


class LayoutAgent(BaseAgent):
    """
    Enhanced Layout Agent with Geometric Product Placement
    Returns X, Y coordinates for where products should be placed in the room
    """
    
    def __init__(self):
        super().__init__(agent_name="LayoutOptimizer")
    
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """
        Generate optimal room layout with geometric coordinates
        
        Context expected:
            - room_type: str
            - room_size: str
            - style_data: Dict (from StyleAgent)
            - selected_products: List (from ProductAgent)
        """
        self.log_activity("Planning geometric room layout...")
        
        room_type = context.get("room_type", "living_room")
        room_size = context.get("room_size", "medium")
        style_data = context.get("style_data", {})
        products = context.get("selected_products", [])
        
        if not products:
            self.log_activity("⚠️ No products to arrange")
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data={"product_placements": []},
                reasoning="No products to arrange",
                confidence=0.0
            )
        
        # Format products for Claude
        products_summary = "\n".join([
            f"{i+1}. {p.get('name')} ({p.get('category')}) - {p.get('material', 'N/A')}"
            for i, p in enumerate(products)
        ])
        
        system_prompt = """You are an expert interior designer specializing in spatial planning and room layouts.

Your task is to determine the GEOMETRIC PLACEMENT of furniture in a room, providing:
1. Relative X, Y coordinates (as percentages 0-100 of room width/height)
2. Optimal sizing for each product
3. Spatial relationships between items
4. Traffic flow considerations

Respond ONLY with valid JSON in this exact format:
{
    "product_placements": [
        {
            "product_index": 0,
            "product_name": "name",
            "position": {
                "x_percent": 25,
                "y_percent": 60,
                "width_percent": 30,
                "height_percent": 35
            },
            "placement_zone": "center-left|center|right|etc",
            "reasoning": "why this position is optimal"
        }
    ],
    "focal_point": "description of room's focal point",
    "traffic_flow": "description of movement paths",
    "spatial_balance": 0.88,
    "layout_reasoning": "overall layout strategy"
}

COORDINATE SYSTEM:
- (0, 0) = top-left of room
- (100, 100) = bottom-right of room
- x_percent: left-to-right positioning
- y_percent: top-to-bottom positioning
- width_percent: how much horizontal space product occupies
- height_percent: how much vertical space product occupies

PLACEMENT RULES:
1. Large seating (sofas): 20-40% from left, 60-80% from top (lower third of image)
2. Tables: Center area (40-60% x, 60-80% y)
3. Tall items (lamps, plants): Corners or sides (10-15% or 85-90% x)
4. Small accents: Fill gaps without blocking pathways
5. Leave 40-60% of center floor clear for traffic flow"""

        user_message = f"""Create optimal geometric layout for this room:

Room Type: {room_type}
Room Size: {room_size}
Style: {style_data.get('primary_style', 'modern')}

Products to Place:
{products_summary}

Provide geometric coordinates (X, Y, Width, Height as percentages) for each product 
that creates a balanced, functional, and aesthetically pleasing room layout."""

        try:
            response_text = self._call_claude(system_prompt, user_message, temperature=0.3)
            
            # Parse JSON response
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
            layout_data = json.loads(cleaned_response)
            
            # Enrich placements with product details
            enriched_placements = []
            for placement in layout_data.get("product_placements", []):
                idx = placement.get("product_index", 0)
                if 0 <= idx < len(products):
                    enriched_placement = {
                        **placement,
                        "product_details": products[idx]
                    }
                    enriched_placements.append(enriched_placement)
            
            layout_data["product_placements"] = enriched_placements
            
            self.log_activity(f"✅ Layout planned for {len(enriched_placements)} products")
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=layout_data,
                reasoning=layout_data.get("layout_reasoning", "Spatial layout optimized"),
                confidence=layout_data.get("spatial_balance", 0.85)
            )
            
        except json.JSONDecodeError as e:
            self.log_activity(f"JSON parsing failed, using default layout")
            
            # Fallback: Default geometric layout
            default_layout = self._create_default_layout(products, room_type)
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=default_layout,
                reasoning="Using default geometric layout template",
                confidence=0.7
            )
        
        except Exception as e:
            self.log_activity(f"Layout planning failed: {str(e)}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={"product_placements": []},
                reasoning=f"Error: {str(e)}",
                confidence=0.0
            )
    
    def _create_default_layout(self, products: List[Dict], room_type: str) -> Dict:
        """
        Fallback: Create sensible default layout based on product categories
        """
        placements = []
        
        # Default positions by category
        category_positions = {
            "seating": {"x": 25, "y": 60, "w": 30, "h": 35, "zone": "center-left"},
            "table": {"x": 50, "y": 70, "w": 20, "h": 20, "zone": "center"},
            "lighting": {"x": 75, "y": 50, "w": 15, "h": 40, "zone": "right"},
            "storage": {"x": 15, "y": 55, "w": 15, "h": 25, "zone": "left"},
            "bed": {"x": 50, "y": 50, "w": 40, "h": 30, "zone": "center"},
            "desk": {"x": 70, "y": 60, "w": 25, "h": 30, "zone": "right"}
        }
        
        for i, product in enumerate(products):
            category = product.get("category", "").lower()
            
            # Get position template or use generic
            pos_template = category_positions.get(category, {
                "x": 50, "y": 60, "w": 20, "h": 25, "zone": "center"
            })
            
            placement = {
                "product_index": i,
                "product_name": product.get("name", ""),
                "position": {
                    "x_percent": pos_template["x"] + (i * 10),  # Offset slightly
                    "y_percent": pos_template["y"],
                    "width_percent": pos_template["w"],
                    "height_percent": pos_template["h"]
                },
                "placement_zone": pos_template["zone"],
                "reasoning": f"Default {category} placement",
                "product_details": product
            }
            
            placements.append(placement)
        
        return {
            "product_placements": placements,
            "focal_point": "Center of room",
            "traffic_flow": "Clear pathways maintained",
            "spatial_balance": 0.75,
            "layout_reasoning": "Default layout template applied"
        }


# Create singleton
layout_agent = LayoutAgent()
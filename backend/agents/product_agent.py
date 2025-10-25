"""
Product Recommendation Agent
Queries the Product Knowledge Graph (PKG) and uses Claude to select optimal furniture
"""
from typing import Dict, Any, List
import json

from agents.base_agent import BaseAgent, AgentResponse


class ProductAgent(BaseAgent):
    """
    Specializes in furniture selection and product recommendations
    Uses PKG data + Claude reasoning to choose compatible products
    """
    
    def __init__(self):
        super().__init__(agent_name="ProductRecommender")
        
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """
        Select furniture products based on style analysis and constraints
        
        Context expected:
            - available_products: List[ProductSuggestion] - from PKG query
            - style_data: Dict - from StyleAgent
            - room_type: str
            - room_size: str
            - budget_max: float (optional)
        """
        self.log_activity("Analyzing product compatibility...")
        
        available_products = context.get("available_products", [])
        style_data = context.get("style_data", {})
        room_type = context.get("room_type", "living_room")
        room_size = context.get("room_size", "medium")
        budget_max = context.get("budget_max", None)
        
        if not available_products:
            self.log_activity("⚠️ No products available from PKG")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={"selected_products": []},
                reasoning="No products available in PKG",
                confidence=0.0
            )
        
        # Format products for Claude
        products_summary = "\n".join([
            f"Product {i+1}: {p.get('name', 'Unknown')} - ${p.get('base_price', 0)} "
            f"({p.get('material', 'N/A')}, compatibility: {p.get('compatibility_score', 0):.2f})"
            for i, p in enumerate(available_products)
        ])
        
        system_prompt = """You are an expert furniture curator and interior design consultant.

Your task is to select the BEST products for a specific room design based on:
1. Style compatibility with user preferences
2. Budget constraints
3. Spatial appropriateness for room size
4. Complementary materials and finishes
5. Product compatibility scores from our knowledge graph

Respond ONLY with valid JSON in this exact format:
{
    "selected_products": [
        {
            "product_index": 0,
            "product_name": "name",
            "selection_reason": "why this product was chosen",
            "priority": "essential|recommended|optional"
        }
    ],
    "total_estimated_cost": 5000.50,
    "style_coherence_score": 0.92,
    "reasoning": "Overall explanation of product selection strategy"
}

Select 3-7 products that create a cohesive design."""

        style_summary = f"""
Style Preferences:
- Primary Style: {style_data.get('primary_style', 'modern')}
- Mood: {style_data.get('mood', 'comfortable')}
- Color Palette: {', '.join(style_data.get('color_palette', ['neutral']))}
- Materials: {', '.join(style_data.get('materials', ['mixed']))}
"""

        user_message = f"""Select optimal furniture for this design:

Room: {room_type} ({room_size} size)
Budget: {'$' + str(budget_max) if budget_max else 'Flexible'}

{style_summary}

Available Products:
{products_summary}

Select the best products that maximize style coherence and value."""

        try:
            response_text = self._call_claude(system_prompt, user_message, temperature=0.5)
            
            # Parse JSON response
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
            product_data = json.loads(cleaned_response)
            
            # Enrich with full product details
            selected_products = []
            for selection in product_data.get("selected_products", []):
                idx = selection.get("product_index", 0)
                if 0 <= idx < len(available_products):
                    full_product = available_products[idx].copy()
                    full_product["selection_reason"] = selection.get("selection_reason", "")
                    full_product["priority"] = selection.get("priority", "recommended")
                    selected_products.append(full_product)
            
            product_data["selected_products"] = selected_products
            
            self.log_activity(f"Selected {len(selected_products)} products, total: ${product_data.get('total_estimated_cost', 0):.2f}")
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=product_data,
                reasoning=product_data.get("reasoning", "Products selected for optimal style coherence"),
                confidence=product_data.get("style_coherence_score", 0.85)
            )
            
        except json.JSONDecodeError as e:
            self.log_activity(f"JSON parsing failed, using top-rated products")
            # Fallback: select top 3 by compatibility score
            sorted_products = sorted(
                available_products, 
                key=lambda p: p.get("compatibility_score", 0), 
                reverse=True
            )[:3]
            
            total_cost = sum(p.get("base_price", 0) for p in sorted_products)
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data={
                    "selected_products": sorted_products,
                    "total_estimated_cost": total_cost,
                    "style_coherence_score": 0.7,
                    "reasoning": "Fallback: Selected top products by compatibility score"
                },
                reasoning="Used compatibility-based fallback selection",
                confidence=0.7
            )
        
        except Exception as e:
            self.log_activity(f"Product selection failed: {str(e)}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={"selected_products": []},
                reasoning=f"Error: {str(e)}",
                confidence=0.0
            )


# Create singleton
product_agent = ProductAgent()
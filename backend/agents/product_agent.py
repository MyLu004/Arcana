"""
Product Recommendation Agent
Queries the Product Knowledge Graph (PKG) and uses Claude to select optimal furniture
"""
"""
STEP 1: Enhanced Product Agent with Image URLs
Replace your existing product_agent.py with this version
"""
from typing import Dict, Any, List
import json

from agents.base_agent import BaseAgent, AgentResponse


class ProductAgent(BaseAgent):
    """
    Enhanced Product Recommendation Agent with Image URLs
    """
    
    # Product image mapping (you can expand this or use Unsplash API)
    PRODUCT_IMAGES = {
        "LR-SOFA-001": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80",  # Modern sofa
        "LR-TABLE-001": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=800&q=80",  # Glass coffee table
        "LR-LAMP-001": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80",  # Arc floor lamp
        "LR-SIDE-001": "https://images.unsplash.com/photo-1565191999001-551c187427bb?w=800&q=80",  # Side table
        "BR-BED-001": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80",  # Platform bed
        "BR-NIGHT-001": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800&q=80",  # Nightstand
        "BR-LAMP-001": "https://images.unsplash.com/photo-1543198126-a8505c2e1b3c?w=800&q=80",  # Table lamp
        "OF-DESK-001": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=800&q=80",  # Standing desk
        "OF-CHAIR-001": "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=800&q=80",  # Office chair
        "OF-SHELF-001": "https://images.unsplash.com/photo-1594620302200-9a762244a156?w=800&q=80",  # Bookshelf
        "SS-SOFA-001": "https://images.unsplash.com/photo-1550226891-ef816aed4a98?w=800&q=80",  # Loveseat
        "SS-TABLE-001": "https://images.unsplash.com/photo-1532372576444-dda954194ad0?w=800&q=80",  # Nesting tables
    }
    
    def __init__(self):
        super().__init__(agent_name="ProductRecommender")
        
    def _get_product_image_url(self, product_id: str) -> str:
        """Get image URL for product"""
        return self.PRODUCT_IMAGES.get(
            product_id, 
            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80"  # Default furniture image
        )
    
    def _get_product_purchase_url(self, product_id: str, product_name: str) -> str:
        """Generate purchase URL (mock for demo)"""
        # In production, this would link to your e-commerce platform
        encoded_name = product_name.replace(" ", "+")
        return f"https://www.wayfair.com/keyword.php?keyword={encoded_name}"
        
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """
        Select furniture products with IMAGE URLS
        """
        self.log_activity("Analyzing product compatibility...")
        
        available_products = context.get("available_products", [])
        style_data = context.get("style_data", {})
        room_type = context.get("room_type", "living_room")
        room_size = context.get("room_size", "medium")
        budget_max = context.get("budget_max", None)
        
        if not available_products:
            self.log_activity("No products available from PKG")
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
            
            # ✨ NEW: Enrich with full product details + IMAGE URLS + PURCHASE LINKS
            selected_products = []
            for selection in product_data.get("selected_products", []):
                idx = selection.get("product_index", 0)
                if 0 <= idx < len(available_products):
                    full_product = available_products[idx].copy()
                    product_id = full_product.get("sku", "")
                    
                    # Add visual elements
                    full_product["selection_reason"] = selection.get("selection_reason", "")
                    full_product["priority"] = selection.get("priority", "recommended")
                    full_product["image_url"] = self._get_product_image_url(product_id)  
                    full_product["purchase_url"] = self._get_product_purchase_url(  
                        product_id, 
                        full_product.get("name", "")
                    )
                    
                    selected_products.append(full_product)
            
            product_data["selected_products"] = selected_products
            
            self.log_activity(f"Selected {len(selected_products)} products with images, total: ${product_data.get('total_estimated_cost', 0):.2f}")
            
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
            
            # Add image URLs to fallback products
            for product in sorted_products:
                product_id = product.get("sku", "")
                product["image_url"] = self._get_product_image_url(product_id)
                product["purchase_url"] = self._get_product_purchase_url(
                    product_id, 
                    product.get("name", "")
                )
            
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
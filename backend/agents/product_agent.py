"""
Product Recommendation Agent - COMPLETE FIXED

Replicate FileOutput handling FIXED

Budget enforcement works

Unique images (Replicate AI or Unsplash fallback)
"""
from typing import Dict, Any, List
import json
import urllib.parse
import hashlib
import os

from agents.base_agent import BaseAgent, AgentResponse


class ProductAgent(BaseAgent):
    """
    Specializes in furniture selection with BUDGET DISCIPLINE
    """
    
    def __init__(self):
        super().__init__(agent_name="ProductRecommender")
    
    def _get_unique_image_url(self, product_name: str, category: str) -> str:
        """
        
        Generate UNIQUE Unsplash URL that BYPASSES CORB
        Uses product name hash as seed for unique images
        """
        # Map categories to better search terms
        search_terms = {
            'seating': 'chair,armchair,sofa,furniture',
            'table': 'table,furniture,wood',
            'lighting': 'lamp,light,fixture,interior',
            'storage': 'shelf,cabinet,storage,furniture',
            'bed': 'bed,bedroom,furniture',
            'desk': 'desk,workspace,office',
            'decor': 'decor,decoration,home,interior'
        }
        
        query = search_terms.get(category, 'furniture,interior')
        
        # Add style hints from product name
        name_lower = product_name.lower()
        if 'modern' in name_lower or 'minimalist' in name_lower:
            query += ',modern,minimalist'
        if 'industrial' in name_lower:
            query += ',industrial,metal'
        if 'colorful' in name_lower:
            query += ',colorful,vibrant'
        if 'wood' in name_lower or 'wooden' in name_lower:
            query += ',wood,natural'
        
        # 
        # KEY FIX: Use product name hash as unique seed
        product_hash = hashlib.md5(product_name.encode()).hexdigest()[:8]
        
        encoded_query = urllib.parse.quote(query)
        
        # 
        # CRITICAL: Use source.unsplash.com to bypass CORB
        return f"https://source.unsplash.com/800x600/?{encoded_query}&sig={product_hash}"
    
    def _get_purchase_url(self, product_name: str) -> str:
        """Generate purchase URL"""
        encoded_name = urllib.parse.quote(product_name)
        return f"https://www.wayfair.com/keyword.php?keyword={encoded_name}"
    
    def _generate_ai_image(self, prompt: str, product_name: str) -> str:
        """
        
        FIXED: Generate AI product image using Replicate
        Properly handles FileOutput/generator objects
        """
        try:
            import replicate
            
            self.log_activity(f"Generating AI image for: {product_name}")
            
            # Run Stable Diffusion XL
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": f"professional product photography of {prompt}, white background, studio lighting, high quality, 4k, sharp focus",
                    "negative_prompt": "blurry, low quality, distorted, text, watermark, logo, hands, people",
                    "width": 800,
                    "height": 600,
                    "num_outputs": 1,
                    "scheduler": "K_EULER",
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5
                }
            )
            
            # 
            # FIX: Handle Replicate's different output types
            image_url = None
            
            # Try different ways to extract URL
            try:
                # Method 1: Iterator/generator (most common in new SDK)
                if hasattr(output, '__iter__') and not isinstance(output, (str, bytes)):
                    output_list = list(output)
                    if output_list and len(output_list) > 0:
                        first_item = output_list[0]
                        # Could be FileOutput object or string
                        if hasattr(first_item, 'url'):
                            image_url = first_item.url
                        elif hasattr(first_item, 'read'):
                            # File-like object, get URL another way
                            image_url = str(first_item)
                        else:
                            image_url = str(first_item)
                # Method 2: Direct string URL
                elif isinstance(output, str):
                    image_url = output
                # Method 3: FileOutput object with url attribute
                elif hasattr(output, 'url'):
                    image_url = output.url
                # Method 4: Convert to string
                else:
                    image_url = str(output)
            except Exception as parse_error:
                self.log_activity(f"Parse error: {str(parse_error)}")
                raise
            
            if not image_url or image_url == "None":
                raise ValueError("No valid image URL extracted from Replicate")
            
            self.log_activity(f"AI image generated: {image_url[:60]}...")
            return image_url
            
        except Exception as e:
            self.log_activity(f"Image generation failed: {str(e)}")
            raise  # Re-raise to trigger fallback
        
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """Select products with STRICT BUDGET ENFORCEMENT"""
        
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
        
        self.log_activity(f"Available products: {len(available_products)}")
        
        # 
        # FIX: Calculate usable budget (reserve for tax & shipping)
        TAX_RATE = 0.0825
        SHIPPING_THRESHOLD = 1000
        
        if budget_max:
            # Reserve budget for tax and potentially shipping
            usable_budget = budget_max / (1 + TAX_RATE)
            if usable_budget < SHIPPING_THRESHOLD:
                usable_budget -= 150  # Reserve $150 for shipping
            
            self.log_activity(f"Budget: ${budget_max:.2f} total → ${usable_budget:.2f} for products")
        else:
            usable_budget = None
            self.log_activity("No budget constraint")
        
        # 
        # NEW: Adapt strategy for small product pools
        if len(available_products) < 5:
            self.log_activity(f"Small product pool ({len(available_products)} items)")
        
        # Format products
        products_summary = "\n".join([
            f"Product {i}: {p.get('name', 'Unknown')} - ${p.get('base_price', 0)} "
            f"({p.get('material', 'N/A')}, {p.get('category', 'furniture')}, score: {p.get('compatibility_score', 0):.2f})"
            for i, p in enumerate(available_products)
        ])
        
        # 
        # FIX: Enhanced system prompt with BUDGET ENFORCEMENT
        system_prompt = f"""You are an expert furniture curator with ABSOLUTE BUDGET DISCIPLINE.

CRITICAL RULES:
{"1. MAXIMUM PRODUCT SUBTOTAL: $" + f"{usable_budget:.2f}" if usable_budget else "1. No budget limit"}
{"2. You MUST select products where SUM of base_price is UNDER this limit" if usable_budget else ""}
{"3. Tax (8.25%) and shipping will be added later, so stay WELL UNDER!" if usable_budget else ""}

BUDGET STRATEGY:
{"- TIGHT BUDGET (<$500): Select ONLY 2-3 ESSENTIAL items under $" + f"{usable_budget:.2f}" if usable_budget and usable_budget < 450 else ""}
{"- MODERATE BUDGET ($500-$2000): Select 3-5 balanced items" if usable_budget and 450 <= usable_budget < 1800 else ""}
{"- COMFORTABLE BUDGET (>$2000): Select 5-7 items for complete design" if not usable_budget or usable_budget >= 1800 else ""}

PRODUCT POOL SIZE: {len(available_products)} products available
{"LIMITED OPTIONS: Work with what's available, prioritize essentials" if len(available_products) < 5 else ""}

Respond ONLY with valid JSON:
{{
    "selected_products": [
        {{
            "product_index": 0,
            "product_name": "name",
            "selection_reason": "why chosen",
            "priority": "essential|recommended|optional"
        }}
    ],
    "total_estimated_cost": 350.00,
    "style_coherence_score": 0.92,
    "reasoning": "Overall selection strategy"
}}"""

        style_summary = f"""Style Preferences:
- Primary: {style_data.get('primary_style', 'modern')}
- Mood: {style_data.get('mood', 'comfortable')}
- Colors: {', '.join(style_data.get('color_palette', ['neutral']))}
- Materials: {', '.join(style_data.get('materials', ['mixed']))}"""

        # 
        # FIX: Add explicit budget warning
        budget_warning = ""
        if budget_max and budget_max < 500:
            budget_warning = f"\n\nCRITICAL: This is a VERY TIGHT budget of ${budget_max}. You MUST select ONLY 2-3 essential items that cost UNDER ${usable_budget:.2f} total. DO NOT exceed this limit!"

        user_message = f"""Select furniture for this design:

Room: {room_type} ({room_size} size)
Budget: {'$' + str(budget_max) + " (strict limit)" if budget_max else 'Flexible'}
{budget_warning}

{style_summary}

Available Products:
{products_summary}

{"SELECT ONLY PRODUCTS THAT FIT BUDGET!" if budget_max else "Select best products for coherent design."}"""

        try:
            response_text = self._call_claude(system_prompt, user_message, temperature=0.4)
            
            # Parse JSON
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
            product_data = json.loads(cleaned_response)
            
            # Check if Replicate is configured
            replicate_token = os.getenv("REPLICATE_API_TOKEN")
            use_ai_images = replicate_token is not None and replicate_token.strip() != ""
            
            if use_ai_images:
                self.log_activity("DEBUG: Replicate API token found: Yes")
            else:
                self.log_activity("DEBUG: No Replicate token, using Unsplash")
            
            # Enrich products with full details + images
            selected_products = []
            actual_total = 0
            
            for selection in product_data.get("selected_products", []):
                idx = selection.get("product_index", 0)
                if 0 <= idx < len(available_products):
                    full_product = available_products[idx].copy()
                    
                    # 
                    # Try AI image generation, fall back to Unsplash
                    if use_ai_images:
                        try:
                            product_prompt = f"{full_product.get('name', 'furniture')}, {full_product.get('material', '')}, {full_product.get('category', 'furniture')}"
                            ai_image_url = self._generate_ai_image(product_prompt, full_product.get('name', 'furniture'))
                            full_product["image_url"] = ai_image_url
                            full_product["image_source"] = "ai_generated"
                        except Exception as e:
                            # Fall back to Unsplash
                            self.log_activity(f"⚠️ AI image failed, using Unsplash fallback")
                            full_product["image_url"] = self._get_unique_image_url(
                                full_product.get("name", "furniture"),
                                full_product.get("category", "furniture")
                            )
                            full_product["image_source"] = "unsplash_fallback"
                    else:
                        # Use Unsplash directly
                        full_product["image_url"] = self._get_unique_image_url(
                            full_product.get("name", "furniture"),
                            full_product.get("category", "furniture")
                        )
                        full_product["image_source"] = "unsplash"
                    
                    full_product["purchase_url"] = self._get_purchase_url(
                        full_product.get("name", "furniture")
                    )
                    
                    full_product["selection_reason"] = selection.get("selection_reason", "")
                    full_product["priority"] = selection.get("priority", "recommended")
                    selected_products.append(full_product)
                    actual_total += full_product.get("base_price", 0)
            
            # 
            # FIX: Validate budget constraint
            if usable_budget and actual_total > usable_budget:
                self.log_activity(f"Budget exceeded! {actual_total:.2f} > {usable_budget:.2f}, enforcing constraint...")
                # Remove optional items until within budget
                selected_products = self._enforce_budget(selected_products, usable_budget)
                actual_total = sum(p.get("base_price", 0) for p in selected_products)
            
            product_data["selected_products"] = selected_products
            product_data["total_estimated_cost"] = actual_total
            
            self.log_activity(f"Selected {len(selected_products)} products, subtotal: ${actual_total:.2f}")
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=product_data,
                reasoning=product_data.get("reasoning", "Products selected for optimal design"),
                confidence=product_data.get("style_coherence_score", 0.85)
            )
            
        except json.JSONDecodeError as e:
            self.log_activity(f"JSON parsing failed: {e}")
            # Fallback: budget-aware selection
            return self._fallback_selection(available_products, usable_budget)
        
        except Exception as e:
            self.log_activity(f"Error: {str(e)}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={"selected_products": []},
                reasoning=f"Error: {str(e)}",
                confidence=0.0
            )
    
    def _enforce_budget(self, products: List[Dict], max_budget: float) -> List[Dict]:
        """Remove optional items until within budget"""
        # Sort by priority: essential > recommended > optional
        priority_order = {"essential": 0, "recommended": 1, "optional": 2}
        sorted_products = sorted(
            products,
            key=lambda p: (priority_order.get(p.get("priority", "recommended"), 1), -p.get("base_price", 0))
        )
        
        # Keep adding until budget reached
        selected = []
        running_total = 0
        
        for product in sorted_products:
            price = product.get("base_price", 0)
            if running_total + price <= max_budget:
                selected.append(product)
                running_total += price
        
        return selected
    
    def _fallback_selection(self, products: List[Dict], max_budget: float) -> AgentResponse:
        """Budget-aware fallback selection"""
        # Sort by compatibility score
        sorted_products = sorted(
            products,
            key=lambda p: p.get("compatibility_score", 0),
            reverse=True
        )
        
        # Select products within budget
        selected = []
        running_total = 0
        
        for product in sorted_products:
            price = product.get("base_price", 0)
            if max_budget is None or running_total + price <= max_budget:
                # Add unique image (bypasses CORB)
                product["image_url"] = self._get_unique_image_url(
                    product.get("name", "furniture"),
                    product.get("category", "furniture")
                )
                product["purchase_url"] = self._get_purchase_url(
                    product.get("name", "furniture")
                )
                product["priority"] = "recommended"
                product["image_source"] = "unsplash_fallback"
                selected.append(product)
                running_total += price
                
                if len(selected) >= 3:  # Minimum 3 products
                    break
        
        total_cost = sum(p.get("base_price", 0) for p in selected)
        
        return AgentResponse(
            agent_name=self.agent_name,
            success=True,
            data={
                "selected_products": selected,
                "total_estimated_cost": total_cost,
                "style_coherence_score": 0.7,
                "reasoning": "Fallback: Selected by compatibility score within budget"
            },
            reasoning="Used compatibility-based fallback",
            confidence=0.7
        )


# Create singleton
product_agent = ProductAgent()
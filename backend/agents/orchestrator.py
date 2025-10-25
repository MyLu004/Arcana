"""
Orchestrator Agent
Lead coordinator that manages worker agents and synthesizes their outputs
Uses Claude Opus 4 with extended thinking for complex multi-step reasoning
"""
from typing import Dict, Any, List
import json
from anthropic import Anthropic

from agents.base_agent import BaseAgent, AgentResponse
from agents.style_agent import style_agent
from agents.product_agent import product_agent
from agents.layout_agent import layout_agent
from agents.budget_agent import budget_agent

from config import get_settings

settings = get_settings()


class OrchestratorAgent:
    """
    Lead agent that coordinates specialized worker agents
    Demonstrates the orchestrator-worker pattern recommended by Anthropic
    Uses Claude Opus 4 for deep reasoning
    """
    
    def __init__(self):
        self.agent_name = "LeadOrchestrator"
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-opus-4-20250514"  # Opus for orchestrator's deep reasoning
        
        # Register worker agents
        self.workers = {
            "style": style_agent,
            "product": product_agent,
            "layout": layout_agent,
            "budget": budget_agent
        }
    
    def orchestrate_design(
        self,
        user_request: Dict[str, Any],
        control_image_url: str,
        available_products: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Main orchestration method
        Coordinates all agents to produce complete design recommendation
        
        Args:
            user_request: User's design requirements
            control_image_url: URL of the constraint sketch/image
            available_products: Furniture items from PKG
        
        Returns:
            Complete design specification with agent outputs
        """
        self.log_activity("Beginning multi-agent design orchestration...")
        
        # Extract user request details
        user_prompt = user_request.get("prompt", "")
        room_type = user_request.get("room_type", "living_room")
        room_size = user_request.get("room_size", "medium")
        style_preferences = user_request.get("style_preferences", [])
        budget_max = user_request.get("budget_max", None)
        
        # Storage for agent results
        agent_results = {}
        
        try:
            # ============================================
            # PHASE 1: Style Analysis
            # ============================================
            self.log_activity("Phase 1: Analyzing user style preferences...")
            
            style_context = {
                "user_prompt": user_prompt,
                "room_type": room_type,
                "room_size": room_size,
                "style_preferences": style_preferences
            }
            
            style_response = self.workers["style"].process(style_context)
            agent_results["style"] = style_response
            
            if not style_response.success:
                self.log_activity("Style analysis failed, continuing with defaults...")
            
            # ============================================
            # PHASE 2: Product Recommendation
            # ============================================
            self.log_activity("Phase 2: Selecting optimal furniture products...")
            
            product_context = {
                "available_products": available_products,
                "style_data": style_response.data,
                "room_type": room_type,
                "room_size": room_size,
                "budget_max": budget_max
            }
            
            product_response = self.workers["product"].process(product_context)
            agent_results["product"] = product_response
            
            if not product_response.success:
                raise Exception("Product recommendation failed - cannot proceed")
            
            selected_products = product_response.data.get("selected_products", [])
            
            # ============================================
            # PHASE 3: Layout Optimization (Parallel with Budget)
            # ============================================
            self.log_activity("Phase 3: Optimizing spatial layout...")
            
            layout_context = {
                "room_type": room_type,
                "room_size": room_size,
                "selected_products": selected_products,
                "style_data": style_response.data
            }
            
            layout_response = self.workers["layout"].process(layout_context)
            agent_results["layout"] = layout_response
            
            # ============================================
            # PHASE 4: Budget Management
            # ============================================
            self.log_activity("Phase 4: Analyzing budget and costs...")
            
            budget_context = {
                "selected_products": selected_products,
                "budget_max": budget_max,
                "available_products": available_products
            }
            
            budget_response = self.workers["budget"].process(budget_context)
            agent_results["budget"] = budget_response
            
            # ============================================
            # PHASE 5: Orchestrator Synthesis
            # ============================================
            self.log_activity("Phase 5: Synthesizing final design recommendation...")
            
            final_design = self._synthesize_outputs(
                agent_results=agent_results,
                control_image_url=control_image_url,
                user_request=user_request
            )
            
            self.log_activity("Design orchestration complete!")
            
            return final_design
            
        except Exception as e:
            self.log_activity(f"Orchestration failed: {str(e)}")
            # Return error response with partial results
            return {
                "success": False,
                "error": str(e),
                "partial_results": agent_results
            }
    
    def _synthesize_outputs(
        self,
        agent_results: Dict[str, AgentResponse],
        control_image_url: str,
        user_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesize all agent outputs into final design recommendation
        Uses Claude Opus for high-quality narrative generation
        """
        self.log_activity("Synthesizing agent outputs into cohesive design...")
        
        # Extract key data from agent responses
        style_data = agent_results.get("style", AgentResponse(
            agent_name="style", success=False, data={}, reasoning="", confidence=0
        )).data
        
        product_data = agent_results.get("product", AgentResponse(
            agent_name="product", success=False, data={}, reasoning="", confidence=0
        )).data
        
        layout_data = agent_results.get("layout", AgentResponse(
            agent_name="layout", success=False, data={}, reasoning="", confidence=0
        )).data
        
        budget_data = agent_results.get("budget", AgentResponse(
            agent_name="budget", success=False, data={}, reasoning="", confidence=0
        )).data
        
        selected_products = product_data.get("selected_products", [])
        
        # Generate ControlNet prompt using Opus
        controlnet_prompt = self._generate_controlnet_prompt(
            style_data=style_data,
            selected_products=selected_products,
            layout_data=layout_data,
            user_request=user_request
        )
        
        # Assemble final response
        return {
            "success": True,
            "control_params": {
                "prompt": controlnet_prompt,
                "control_image_url": control_image_url,
                "scale": 3.8,
                "steps": 25,
                "negative_prompt": self._generate_negative_prompt(style_data)
            },
            "reasoning": self._generate_reasoning_summary(agent_results),
            "product_justification": product_data.get("reasoning", "Products selected for optimal design coherence"),
            "agent_outputs": {
                "style_analysis": style_data,
                "product_recommendations": product_data,
                "layout_optimization": layout_data,
                "budget_analysis": budget_data
            },
            "confidence_scores": {
                "style": agent_results.get("style", AgentResponse(
                    agent_name="style", success=False, data={}, reasoning="", confidence=0
                )).confidence,
                "product": agent_results.get("product", AgentResponse(
                    agent_name="product", success=False, data={}, reasoning="", confidence=0
                )).confidence,
                "layout": agent_results.get("layout", AgentResponse(
                    agent_name="layout", success=False, data={}, reasoning="", confidence=0
                )).confidence,
                "budget": agent_results.get("budget", AgentResponse(
                    agent_name="budget", success=False, data={}, reasoning="", confidence=0
                )).confidence
            }
        }
    
    def _generate_controlnet_prompt(
        self,
        style_data: Dict[str, Any],
        selected_products: List[Dict[str, Any]],
        layout_data: Dict[str, Any],
        user_request: Dict[str, Any]
    ) -> str:
        """Generate photorealistic prompt for ControlNet image generation"""
        
        primary_style = style_data.get("primary_style", "modern")
        mood = style_data.get("mood", "comfortable")
        colors = ", ".join(style_data.get("color_palette", ["neutral tones"]))
        materials = ", ".join(style_data.get("materials", ["mixed materials"]))
        
        # Get product names
        product_names = [p.get("name", "furniture piece") for p in selected_products[:5]]
        
        # Get layout focal point
        focal_point = layout_data.get("focal_point", "natural lighting")
        
        room_type = user_request.get("room_type", "living room")
        
        # Use Claude Opus to generate refined prompt
        system_prompt = """You are an expert at writing photorealistic scene descriptions for image generation models.

Generate a detailed, visual prompt (100-150 words) that describes an interior design scene with:
- Specific lighting and atmosphere
- Texture and material details
- Color palette
- Furniture placement and spatial flow
- Professional photography aesthetic

Write in a flowing, descriptive style that guides image generation."""

        user_message = f"""Generate a photorealistic prompt for:

Room: {room_type}
Style: {primary_style}
Mood: {mood}
Colors: {colors}
Materials: {materials}
Focal Point: {focal_point}

Featured Products: {', '.join(product_names)}

Create a vivid, detailed scene description."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            self.log_activity(f"Opus prompt generation failed, using template")
            # Fallback template
            return f"A beautifully designed {primary_style} {room_type} with {mood} atmosphere, featuring {', '.join(product_names)}. The space is bathed in warm natural light with {colors} color palette. Materials include {materials}, creating elegant harmony. {focal_point} serves as the visual anchor. Professional interior photography, high-end residential design, architectural digest quality."
    
    def _generate_negative_prompt(self, style_data: Dict[str, Any]) -> str:
        """Generate negative prompt for ControlNet"""
        return "cluttered, dark, cramped, outdated furniture, harsh lighting, busy patterns, oversized furniture, low quality, blurry, distorted"
    
    def _generate_reasoning_summary(self, agent_results: Dict[str, AgentResponse]) -> str:
        """Generate human-readable summary of the orchestration process"""
        
        summaries = []
        
        for agent_name, response in agent_results.items():
            if response.success:
                summaries.append(f"{agent_name.capitalize()}: {response.reasoning}")
            else:
                summaries.append(f"{agent_name.capitalize()}: {response.reasoning}")
        
        return " | ".join(summaries)
    
    def log_activity(self, message: str):
        """Log orchestrator activity"""
        print(f"[{self.agent_name}] {message}")


# Create singleton
orchestrator = OrchestratorAgent()
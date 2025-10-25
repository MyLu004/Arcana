"""
Style Analysis Agent
Analyzes user input to extract style preferences, color palettes, and aesthetic requirements
"""
from typing import Dict, Any, List
import json

from agents.base_agent import BaseAgent, AgentResponse


class StyleAgent(BaseAgent):
    """
    Specializes in understanding user aesthetic preferences
    Extracts style keywords, color palettes, and design direction
    """
    
    def __init__(self):
        super().__init__(agent_name="StyleAnalyst")
        
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """
        Analyze user input to extract style preferences
        
        Context expected:
            - user_prompt: str
            - room_type: str
            - room_size: str
            - style_preferences: List[str] (optional)
        """
        self.log_activity("Analyzing user style preferences...")
        
        user_prompt = context.get("user_prompt", "")
        room_type = context.get("room_type", "living_room")
        room_size = context.get("room_size", "medium")
        existing_styles = context.get("style_preferences", [])
        
        system_prompt = """You are an expert interior design style analyst.

Your task is to analyze user descriptions and extract:
1. Primary design style (e.g., modern, traditional, minimalist, bohemian, industrial)
2. Secondary style influences (e.g., Scandinavian, mid-century, coastal)
3. Color palette preferences (specific colors mentioned or implied)
4. Mood/atmosphere (e.g., cozy, elegant, vibrant, serene)
5. Material preferences (e.g., wood, metal, glass, natural textiles)

Respond ONLY with valid JSON in this exact format:
{
    "primary_style": "style name",
    "secondary_styles": ["style1", "style2"],
    "color_palette": ["color1", "color2", "color3"],
    "mood": "mood description",
    "materials": ["material1", "material2"],
    "key_descriptors": ["descriptor1", "descriptor2"],
    "confidence_score": 0.85
}"""

        user_message = f"""Analyze this design request:

Room Type: {room_type}
Room Size: {room_size}
User Prompt: "{user_prompt}"
Explicitly Mentioned Styles: {', '.join(existing_styles) if existing_styles else 'None'}

Extract and structure the style preferences."""

        try:
            response_text = self._call_claude(system_prompt, user_message, temperature=0.3)
            
            # Parse JSON response
            # Claude sometimes wraps JSON in markdown, so clean it
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
            style_data = json.loads(cleaned_response)
            
            self.log_activity(f"Identified primary style: {style_data['primary_style']}")
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=style_data,
                reasoning=f"Analyzed user input and identified {style_data['primary_style']} style "
                          f"with {style_data['mood']} mood and {len(style_data['color_palette'])} color preferences",
                confidence=style_data.get("confidence_score", 0.8)
            )
            
        except json.JSONDecodeError as e:
            self.log_activity(f"JSON parsing failed, using fallback style analysis")
            # Fallback with reasonable defaults
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data={
                    "primary_style": existing_styles[0] if existing_styles else "modern",
                    "secondary_styles": existing_styles[1:] if len(existing_styles) > 1 else [],
                    "color_palette": ["neutral", "warm"],
                    "mood": "comfortable",
                    "materials": ["wood", "fabric"],
                    "key_descriptors": ["clean", "functional"],
                    "confidence_score": 0.6
                },
                reasoning="Fallback style analysis used due to parsing error",
                confidence=0.6
            )
        
        except Exception as e:
            self.log_activity(f"Style analysis failed: {str(e)}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={},
                reasoning=f"Error: {str(e)}",
                confidence=0.0
            )


# Create singleton
style_agent = StyleAgent()
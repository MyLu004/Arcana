"""
This uses Replicate's Interior Design ControlNet model
"""
import os
import replicate
import base64
from typing import Optional, Dict, Any

class ImageTransformationService:
    """
    Transforms room images using AI (Replicate ControlNet)
    """
    
    def __init__(self):
        # Set API key
        self.api_key = os.getenv("REPLICATE_API_TOKEN")
        if self.api_key:
            os.environ["REPLICATE_API_TOKEN"] = self.api_key
    
    def transform_room(
        self,
        image_url: str,
        style_prompt: str,
        room_type: str = "living room"
    ) -> Optional[str]:
        """
        Transform a room image with new interior design
        
        Args:
            image_url: Public URL of the room image (from ImgBB)
            style_prompt: Design transformation prompt (from StyleAgent)
            room_type: Type of room
            
        Returns:
            URL of transformed image
        """
        try:
            # Interior Design ControlNet Model
            # This model preserves room structure while changing style
            output = replicate.run(
                "jagilley/controlnet-interior-design:5207b74e91c9da0ac1aaecb7b06dc677c41c3a62ec3c14bb0bb35477a2ccc68f",
                input={
                    "image": image_url,
                    "prompt": self._create_transformation_prompt(style_prompt, room_type),
                    "structure": "depth",  # Preserves room layout
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5,
                    "seed": 42  # For reproducibility in demos
                }
            )
            
            # Output is a list with image URL
            if isinstance(output, list) and len(output) > 0:
                transformed_url = output[0]
                print(f"Room transformed successfully: {transformed_url}")
                return transformed_url
            
            return None
            
        except Exception as e:
            print(f"Image transformation failed: {str(e)}")
            return None
    
    def _create_transformation_prompt(self, style_data: str, room_type: str) -> str:
        """
        Create detailed prompt for image generation
        Based on StyleAgent output
        """
        # If style_data is a dict from StyleAgent
        if isinstance(style_data, dict):
            style = style_data.get('primary_style', 'modern')
            mood = style_data.get('mood', 'comfortable')
            colors = ', '.join(style_data.get('color_palette', ['neutral']))
            
            prompt = f"A beautiful {style} {room_type} interior with {mood} atmosphere, " \
                    f"featuring {colors} color palette, professional interior design photography, " \
                    f"high quality, well-lit, elegant and sophisticated"
        else:
            # Fallback if style_data is a string
            prompt = f"A beautiful {style_data} {room_type}, professional interior design photography, " \
                    f"high quality, well-lit"
        
        return prompt


# Singleton instance
image_transformer = ImageTransformationService()
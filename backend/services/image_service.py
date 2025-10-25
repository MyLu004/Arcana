import base64
import requests
from pathlib import Path
from typing import Optional
import uuid
from PIL import Image
import io

from config import get_settings

settings = get_settings()

class ImageService:
    """Handles image upload and URL generation"""
    
    @staticmethod
    def upload_to_imgbb(image_data: bytes, filename: str) -> str:
        """
        Upload image to ImgBB and return public URL
        This is the CRITICAL function for ControlNet compatibility
        """
        # Convert bytes to base64 (ImgBB requirement)
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # ImgBB API endpoint
        url = "https://api.imgbb.com/1/upload"
        
        payload = {
            'key': settings.IMGBB_API_KEY,
            'image': base64_image,
            'name': filename
        }
        
        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('success'):
                public_url = result['data']['url']
                print(f"Image uploaded successfully: {public_url}")
                return public_url
            else:
                raise Exception(f"ImgBB upload failed: {result}")
                
        except requests.exceptions.RequestException as e:
            print(f"ImgBB upload error: {str(e)}")
            # FALLBACK: Save locally and return localhost URL (won't work with Replicate but good for testing)
            return ImageService._save_local_fallback(image_data, filename)
    
    @staticmethod
    def _save_local_fallback(image_data: bytes, filename: str) -> str:
        """Fallback: Save to local uploads folder"""
        upload_path = Path(settings.upload_dir) / filename
        with open(upload_path, 'wb') as f:
            f.write(image_data)
        
        local_url = f"{settings.base_url}/uploads/{filename}"
        print(f"⚠️ Using local fallback URL: {local_url}")
        return local_url
    
    @staticmethod
    def validate_and_resize(image_data: bytes, max_size: int = 1024) -> bytes:
        """
        Validate image and resize if needed
        ControlNet works best with 512x512 or 1024x1024
        """
        try:
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed (remove alpha channel)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize maintaining aspect ratio
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            output = io.BytesIO()
            img.save(output, format='PNG', optimize=True)
            return output.getvalue()
            
        except Exception as e:
            print(f"Image validation failed: {str(e)}")
            raise ValueError(f"Invalid image data: {str(e)}")
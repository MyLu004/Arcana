from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    REPLICATE_API_TOKEN: str
    IMGBB_API_KEY: str
    upload_dir: str = "./uploads"
    base_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False  

@lru_cache()
def get_settings():
    return Settings()
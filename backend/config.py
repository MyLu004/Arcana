from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    anthropic_api_key: str
    replicate_api_token: str
    imgbb_api_key: str
    upload_dir: str = "./uploads"
    base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
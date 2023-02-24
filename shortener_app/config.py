from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    env_name: str = "dev"
    db_url: str="sqlite:///./shortener.db"
    base_url: str="http://localhost:8000/"
    class Config:
        env_file = ".env"
@lru_cache
def get_settings() -> BaseSettings:
    settings=Settings()
    print(f"Loading... {settings.env_name} settings")
    return settings








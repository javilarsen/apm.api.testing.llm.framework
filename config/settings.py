import os
from pydantic import BaseModel

class Settings(BaseModel):
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://10.201.14.90:8000")
    REQUEST_TIMEOUT_SECONDS: int = 6000
    POLL_INTERVAL_SECONDS: int = 2
    
    @property
    def HEALTH_URL(self) -> str:
        return f"{self.API_BASE_URL}/api/v1/health"
        
    @property
    def SUBMIT_URL(self) -> str:
        return f"{self.API_BASE_URL}/api/v1/templates"

    @property
    def DEFAULT_HEADERS(self) -> dict:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

settings = Settings()
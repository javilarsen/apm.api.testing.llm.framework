from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from .advice import advice

class cause(BaseModel):
    causeId: str
    name: str
    description: str
    advice: list[advice]
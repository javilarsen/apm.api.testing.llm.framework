from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class advice(BaseModel):
    adviceId: str
    description: str
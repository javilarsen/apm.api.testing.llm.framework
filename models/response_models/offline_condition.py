from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class offline_condition(BaseModel):
    name: str
    description: Optional[Any] = None
    expression: Optional[str]
    extendHours: Optional[Any] = None

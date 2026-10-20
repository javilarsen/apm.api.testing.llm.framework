from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class strem_properties(BaseModel):
    name: str
    description: str
    expression: str
    property_Methods: Optional[Any] = None
    outputProperties: Optional[str]
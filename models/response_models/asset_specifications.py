from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class asset_specifications(BaseModel):
    name: str
    description: str
    uom: str
    value: Optional[Any] = None
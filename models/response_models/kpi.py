from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class kpi(BaseModel):
    name: str
    description: str
    expression: str
    uom: str
    convert_uom: bool
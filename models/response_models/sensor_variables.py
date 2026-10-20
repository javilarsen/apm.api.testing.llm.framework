from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class sensor_variable(BaseModel):
    name: str
    description: str
    uom : str
    convert_uom: Optional[str] = None
    expression: Optional[str] = None
    # ¿what kind of variable are?   ¿is deterministic test or unit test?
    floor: Optional[float] = None
    lolo: Optional[float] = None
    low: Optional[float] = None
    high: Optional[float] = None
    hihi: Optional[float] = None
    ceiling: Optional[float] = None   
    
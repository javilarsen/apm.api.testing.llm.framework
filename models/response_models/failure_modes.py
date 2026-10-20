from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from .cause import cause

class failure_modes(BaseModel):
    libraryFailureMode: str
    name: str
    description: str
    expression: str
    core_sensors: List[str]
    extra_sensors: List[str]
    causes: List[cause]

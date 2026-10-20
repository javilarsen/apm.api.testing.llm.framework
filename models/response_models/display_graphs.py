from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class display_graphs(BaseModel):
    name: str
    description: str
    expression: str
    xLabel: str
    xUom: str
    yLabel: str
    yUom: str
    fixedRowCount: bool
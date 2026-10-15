from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class SensorVariable(BaseModel):
    name: str
    description: Optional[str] = None
    uom: Optional[str] = None
    convertUoM: Optional[Any] = None
    expression: Optional[Any] = None
    floor: Optional[Any] = None
    lolo: Optional[Any] = None
    lo: Optional[Any] = None
    hi: Optional[Any] = None
    hihi: Optional[Any] = None
    ceiling: Optional[Any] = None

class AssetTemplateResponse(BaseModel):
    templateName: str
    templateDescription: Optional[str] = ""
    graphic: Optional[str] = ""
    sensorRoles: Optional[Any] = None
    sensorVariables: List[SensorVariable] = []
    KPIs: Optional[Any] = None
    assetSpecifications: Optional[Any] = None
    displayGraphs: Optional[Any] = None
    streamProperties: Optional[Any] = None
    offlineCondition: Optional[Any] = None
    failureModes: Optional[Any] = None
    Version: str

class KPIResponse(BaseModel):
    name: str
    description: str
    expression: str
    uom: str
    convertUoM: bool

class DisplayGraphResponse(BaseModel):
    name: str
    description: str
    expression: str
    xLabel: str
    xUoM: str
    yLabel: str
    yUoM: str
    fixedRowCount: bool

class FailureModeResponse(BaseModel):
    libraryFailureModeId: str
    name: str
    description: str
    extended: List[Any]
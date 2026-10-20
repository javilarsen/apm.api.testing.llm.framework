from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from .sensor_variables import sensor_variable

class asset_template(BaseModel):
    templateName: str
    templateDescription: Optional[str] = ""
    graphic: Optional[str] = ""
    sensorRoles: Optional[Any] = None
    sensorVariables: List[sensor_variable] = []
    KPIs: Optional[Any] = None
    assetSpecifications: Optional[Any] = None
    displayGraphs: Optional[Any] = None
    streamProperties: Optional[Any] = None
    offlineCondition: Optional[Any] = None
    failureModes: Optional[Any] = None
    Version: str
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class AssetTemplateRequest(BaseModel):
    equipment_name: str = Field(..., alias="equipment_name")
    phase_text: Optional[str] = Field(None, alias="phase_text")

    @field_validator("equipment_name")
    @classmethod
    def validate_equipment_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("ASSET_NAME must not be empty")
        return v.strip()

    def to_payload(self) -> dict:
        payload = {"equipment_name": self.equipment_name}
        if self.phase_text and self.phase_text.strip():
            payload["phase_text"] = self.phase_text.strip()
        return payload
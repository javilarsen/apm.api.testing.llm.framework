from pydantic import BaseModel

class UserPayload(BaseModel):
    name: str
    job: str

class UserResponse(BaseModel):
    id: str
    name: str
    job: str
    createdAt: str
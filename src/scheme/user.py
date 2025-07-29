from pydantic import BaseModel
from uuid import UUID


class CreateProfileRequest(BaseModel):
    username: str
    phone: str


class CreateProfileResponse(BaseModel):
    id: UUID



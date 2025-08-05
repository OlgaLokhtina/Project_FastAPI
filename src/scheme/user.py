from pydantic import BaseModel
from uuid import UUID


class CreateProfileRequest(BaseModel):
    username: str
    lastname: str
    firstname: str
    surname: str
    phone: str


class CreateProfileResponse(BaseModel):
    id: UUID


class PatchProfileRequest(BaseModel):
    lastname: str
    firstname: str
    surname: str
    phone: str


class GetProfileResponse(BaseModel):
    username: str
    phone: str
    lastname: str
    firstname: str
    surname: str
    id: UUID

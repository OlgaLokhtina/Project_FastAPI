from uuid import UUID

from pydantic import BaseModel


class CreateProfileRequest(BaseModel):
    username: str
    lastname: str
    firstname: str
    surname: str
    phone: str


class CreateProfileResponse(BaseModel):
    id: UUID


class PatchProfileRequest(BaseModel):
    lastname: str = None
    firstname: str = None
    surname: str = None
    phone: str = None


class GetProfileResponse(BaseModel):
    username: str
    phone: str
    lastname: str
    firstname: str
    surname: str
    id: UUID

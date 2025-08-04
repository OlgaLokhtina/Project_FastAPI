from pydantic import BaseModel
from uuid import UUID
from dataclasses import dataclass


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


@dataclass
class DeleteProfileRequest:
    id: UUID

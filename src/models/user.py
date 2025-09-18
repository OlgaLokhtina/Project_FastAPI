import re
from dataclasses import field
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Profile(BaseModel):
    username: str = Field(
        default=None, min_length=3, max_length=10, pattern="^[A-Za-z][0-9A-Za-z]+$"
    )
    phone: str = Field(default=None, pattern=r"^[+]\d{11}")
    lastname: str = Field(default=None, max_length=10, pattern=r"[A-Za-zА-Яа-я]+")
    firstname: str = Field(default=None, max_length=10, pattern="[A-Za-zА-Яа-я]+")
    surname: str = Field(default=None, max_length=10, pattern="[A-Za-zА-Яа-я]+")
    id: UUID = field(default_factory=uuid4)

    @field_validator("lastname")
    @classmethod
    def check_lastname(cls, lastname: str) -> str:
        if re.search(r"\d", lastname):
            raise UserValidationError()
        else:
            return lastname


class UserValidationError(Exception):
    def __str__(self):
        return "Incorrect data!"

from dataclasses import field
from uuid import UUID, uuid4

from pydantic import BaseModel


class Profile(BaseModel):
    username: str = None
    phone: str = None
    lastname: str = None
    firstname: str = None
    surname: str = None
    id: UUID = field(default_factory=uuid4)

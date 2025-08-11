from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Profile:
    username: str = None
    phone: str = None
    lastname: str = None
    firstname: str = None
    surname: str = None
    id: UUID = field(default_factory=uuid4)

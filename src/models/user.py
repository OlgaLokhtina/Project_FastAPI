from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Profile:
    username: str
    phone: str
    id: UUID = field(default_factory=uuid4)






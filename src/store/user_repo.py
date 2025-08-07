from abc import ABC, abstractmethod
from uuid import UUID

from models.user import Profile


class BaseUserRepository(ABC):
    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def save(self, profile):
        pass

    @abstractmethod
    def delete(self, profile):
        pass


class UserRepository(BaseUserRepository):
    def __init__(self):
        self.repos: list[Profile] = []

    def get(self, id: UUID) -> Profile | None:
        for rep in self.repos:
            if id == rep.id:
                return rep

    def save(self, profile: Profile):
        self.repos.append(profile)

    def delete(self, id: UUID):
        for rep in self.repos:
            if id == rep.id:
                self.repos.remove(rep)


repo = UserRepository()
repo.save(
    Profile(
        id=UUID("f3082ffd-474f-4dcb-8777-3141ad1b463c"),
        username="Katty",
        phone="45678",
        lastname="Smith",
        firstname="Katerine",
        surname="John",
    )
)

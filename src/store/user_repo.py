from abc import ABC, abstractmethod
from uuid import UUID

from models.user import Profile


class BaseUserRepository(ABC):
    @abstractmethod
    def get(self, profile_id: UUID):
        pass

    @abstractmethod
    def save(self, profile: Profile):
        pass

    @abstractmethod
    def delete(self, profile_id: UUID):
        pass


class UserRepository(BaseUserRepository):
    def __init__(self):
        self.repos: list[Profile] = []

    def get(self, profile_id: UUID) -> Profile | None:
        for rep in self.repos:
            if profile_id == rep.id:
                return rep

    def save(self, profile: Profile):
        if profile in self.repos:
            self.repos = [profile if p.id == profile.id else p for p in self.repos]
        else:
            self.repos.append(profile)

    def delete(self, profile_id: UUID) -> UUID | None:
        for rep in self.repos:
            if profile_id == rep.id:
                self.repos.remove(rep)
                return profile_id


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

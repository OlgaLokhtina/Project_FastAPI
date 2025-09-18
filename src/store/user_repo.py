from typing import Iterable
from uuid import UUID

from models.user import Profile
from store.base import BaseUserRepository, UserNotFound


class UserRepository(BaseUserRepository):
    def __init__(self):
        self.repos: list[Profile] = []

    def get(self, profile_id: UUID) -> Profile:
        for rep in self.repos:
            if profile_id == rep.id:
                return rep
        raise UserNotFound(profile_id)

    def list(self) -> Iterable[Profile]:
        return self.repos

    def save(self, profile: Profile) -> None:
        try:
            repo.get(profile.id)
            self.repos = [profile if p.id == profile.id else p for p in self.repos]
        except UserNotFound:
            self.repos.append(profile)

    def delete(self, profile_id: UUID) -> None:
        for rep in self.repos:
            if profile_id == rep.id:
                self.repos.remove(rep)
                return None
        raise UserNotFound(profile_id)


repo = UserRepository()
repo.save(
    Profile(
        id=UUID("f3082ffd-474f-4dcb-8777-3141ad1b463c"),
        username="Katty",
        phone="+45678987654",
        lastname="Smith",
        firstname="Katerine",
        surname="John",
    )
)

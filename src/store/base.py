from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

from models.user import Profile


class BaseUserRepository(ABC):
    @abstractmethod
    def get(self, profile_id: UUID) -> Profile:
        pass

    @abstractmethod
    def list(self) -> Iterable[Profile]:
        pass

    @abstractmethod
    def save(self, profile: Profile) -> None:
        pass

    @abstractmethod
    def delete(self, profile_id: UUID) -> None:
        pass


class UserNotFound(Exception):
    def __init__(self, profile_id: UUID):
        self.profile_id = profile_id

    def __str__(self):
        return f"User with {self.profile_id} not found"

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from scheme.user import (
    CreateProfileRequest,
    CreateProfileResponse,
    GetProfileResponse,
    PatchProfileRequest,
)
from store.base import BaseUserRepository


class BaseUserUsecase(ABC):
    def __init__(self, repo: BaseUserRepository):
        self.repo = repo

    @abstractmethod
    def get(self, profile_id: UUID) -> GetProfileResponse:
        pass

    @abstractmethod
    def list(self, page, size) -> List[GetProfileResponse]:
        pass

    @abstractmethod
    def create(self, data: CreateProfileRequest) -> CreateProfileResponse:
        pass

    @abstractmethod
    def update(self, profile_id: UUID, data: PatchProfileRequest) -> None:
        pass

    @abstractmethod
    def delete(self, profile_id: UUID) -> None:
        pass

from typing import List
from uuid import UUID

from models.user import Profile
from scheme.user import (
    CreateProfileRequest,
    CreateProfileResponse,
    GetProfileResponse,
    PatchProfileRequest,
)
from usecases.base import BaseUserUsecase


class UserUsecase(BaseUserUsecase):
    def get(self, profile_id: UUID) -> GetProfileResponse:
        profile = self.repo.get(profile_id)
        return GetProfileResponse(
            username=profile.username,
            phone=profile.phone,
            lastname=profile.lastname,
            firstname=profile.firstname,
            surname=profile.surname,
            id=profile.id,
        )

    def list(self, page: int, size: int) -> List[GetProfileResponse]:
        profiles = self.repo.list()
        profile_resp = [
            GetProfileResponse(
                username=user.username,
                phone=user.phone,
                lastname=user.lastname,
                firstname=user.firstname,
                surname=user.surname,
                id=user.id,
            )
            for user in profiles
        ]
        start = (page - 1) * size
        end = page * size
        return profile_resp[start:end]

    def create(self, data: CreateProfileRequest) -> CreateProfileResponse:
        profile = Profile(**data.model_dump())
        self.repo.save(profile)
        return CreateProfileResponse(id=profile.id)

    def update(self, profile_id: UUID, data: PatchProfileRequest) -> None:
        profile = self.repo.get(profile_id)
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(profile, k, v)
        self.repo.save(profile)

    def delete(self, profile_id: UUID) -> None:
        self.repo.delete(profile_id)

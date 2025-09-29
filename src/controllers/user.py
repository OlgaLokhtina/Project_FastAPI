from typing import List
from uuid import UUID

from fastapi import APIRouter

from scheme.user import (
    CreateProfileRequest,
    CreateProfileResponse,
    GetProfileResponse,
    PatchProfileRequest,
)
from store.user_repo import repo
from usecases.user_usecase import UserUsecase

user_router = APIRouter(prefix="/user")


@user_router.post("/")
def create_profile(data: CreateProfileRequest) -> CreateProfileResponse:
    usecase = UserUsecase(repo)
    return usecase.create(data)


@user_router.get("/")
def get_all_profile(page: int, size: int) -> List[GetProfileResponse]:
    usecase = UserUsecase(repo)
    return usecase.list(page, size)


@user_router.get("/{profile_id}")
def get_profile(profile_id: UUID) -> GetProfileResponse:
    usecase = UserUsecase(repo)
    return usecase.get(profile_id)


@user_router.patch("/{profile_id}")
def edit_profile(profile_id: UUID, data: PatchProfileRequest) -> None:
    usecase = UserUsecase(repo)
    usecase.update(profile_id, data)


@user_router.delete("/{profile_id}")
def delete_profile(profile_id: UUID) -> None:
    usecase = UserUsecase(repo)
    usecase.delete(profile_id)

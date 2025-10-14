from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from scheme.user import (
    CreateProfileRequest,
    CreateProfileResponse,
    GetProfileResponse,
    PatchProfileRequest,
)
from store.sql_user_repo import SQLiteUserRepository
from usecases.user_usecase import UserUsecase

user_router = APIRouter(prefix="/user")


def common_parameters() -> UserUsecase:
    sql_repo = SQLiteUserRepository("sql_users.db")
    return UserUsecase(sql_repo)


@user_router.post("/")
def create_profile(
    data: CreateProfileRequest, usecase: UserUsecase = Depends(common_parameters)
) -> CreateProfileResponse:
    return usecase.create(data)


@user_router.get("/")
def get_all_profile(
    page: int, size: int, usecase: UserUsecase = Depends(common_parameters)
) -> List[GetProfileResponse]:
    return usecase.list(page, size)


@user_router.get("/{profile_id}")
def get_profile(
    profile_id: UUID, usecase: UserUsecase = Depends(common_parameters)
) -> GetProfileResponse:
    return usecase.get(profile_id)


@user_router.patch("/{profile_id}")
def edit_profile(
    profile_id: UUID,
    data: PatchProfileRequest,
    usecase: UserUsecase = Depends(common_parameters),
) -> None:
    usecase.update(profile_id, data)


@user_router.delete("/{profile_id}")
def delete_profile(
    profile_id: UUID, usecase: UserUsecase = Depends(common_parameters)
) -> None:
    usecase.delete(profile_id)

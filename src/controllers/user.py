from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends

from scheme.user import (
    CreateProfileRequest,
    CreateProfileResponse,
    GetProfileResponse,
    PatchProfileRequest,
)
from store.user_repo import repo
from usecases.user_usecase import UserUsecase

user_router = APIRouter(prefix="/user")


def common_parameters(
    profile_id: UUID | None = None,
    c_data: CreateProfileRequest | None = None,
    p_data: PatchProfileRequest | None = None,
):
    return {"profile_id": profile_id, "c_data": c_data, "p_data": p_data}


CommonsDep = Annotated[dict, Depends(common_parameters)]


@user_router.post("/")
def create_profile(commons: CommonsDep) -> CreateProfileResponse:
    usecase = UserUsecase(repo)
    return usecase.create(commons["c_data"])


@user_router.get("/")
def get_all_profile(page: int, size: int) -> List[GetProfileResponse]:
    usecase = UserUsecase(repo)
    return usecase.list(page, size)


@user_router.get("/{profile_id}")
def get_profile(commons: CommonsDep) -> GetProfileResponse:
    usecase = UserUsecase(repo)
    return usecase.get(commons["profile_id"])


@user_router.patch("/{profile_id}")
def edit_profile(commons: CommonsDep) -> None:
    usecase = UserUsecase(repo)
    usecase.update(commons["profile_id"], commons["p_data"])


@user_router.delete("/{profile_id}")
def delete_profile(commons: CommonsDep) -> None:
    usecase = UserUsecase(repo)
    usecase.delete(commons["profile_id"])

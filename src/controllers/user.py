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


def common_parameters(profile_id: UUID | None = None, usecase=UserUsecase(repo)):
    return {"profile_id": profile_id, "usecase": usecase}


CommonsDep = Annotated[dict, Depends(common_parameters)]


@user_router.post("/")
def create_profile(
    commons: CommonsDep, data: CreateProfileRequest
) -> CreateProfileResponse:
    usecase = commons["usecase"]
    return usecase.create(data)


@user_router.get("/")
def get_all_profile(
    page: int, size: int, commons: CommonsDep
) -> List[GetProfileResponse]:
    usecase = commons["usecase"]
    return usecase.list(page, size)


@user_router.get("/{profile_id}")
def get_profile(commons: CommonsDep) -> GetProfileResponse:
    usecase = commons["usecase"]
    return usecase.get(commons["profile_id"])


@user_router.patch("/{profile_id}")
def edit_profile(data: PatchProfileRequest, commons: CommonsDep) -> None:
    usecase = commons["usecase"]
    usecase.update(commons["profile_id"], data)


@user_router.delete("/{profile_id}")
def delete_profile(commons: CommonsDep) -> None:
    usecase = commons["usecase"]
    usecase.delete(commons["profile_id"])

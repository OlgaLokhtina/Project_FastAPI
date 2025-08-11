from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from models.user import Profile
from scheme.user import (
    CreateProfileRequest,
    CreateProfileResponse,
    GetProfileResponse,
    PatchProfileRequest,
)
from store.user_repo import repo

user_router = APIRouter(prefix="/user")


@user_router.post("/")
def create_profile(data: CreateProfileRequest) -> CreateProfileResponse:
    profile = Profile(**data.model_dump())
    repo.save(profile)
    return CreateProfileResponse(id=profile.id)


@user_router.get("/")
def get_all_profile() -> List[GetProfileResponse]:
    profiles = repo.list()
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
    return profile_resp


@user_router.get("/{profile_id}")
def get_profile(profile_id: UUID) -> GetProfileResponse | None:
    profile = repo.get(profile_id)
    if profile:
        return GetProfileResponse(
            username=profile.username,
            phone=profile.phone,
            lastname=profile.lastname,
            firstname=profile.firstname,
            surname=profile.surname,
            id=profile.id,
        )
    raise HTTPException(status_code=404, detail=f"User with {profile_id} not found")


@user_router.patch("/{profile_id}")
def edit_profile(profile_id: UUID, data: PatchProfileRequest):
    profile = repo.get(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"User with {profile_id} not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(profile, k, v)
    repo.save(profile)
    return profile


@user_router.delete("/{profile_id}")
def delete_profile(profile_id: UUID):
    if repo.delete(profile_id):
        return f"User with {profile_id} was deleted"
    else:
        raise HTTPException(status_code=404, detail=f"User with {profile_id} not found")

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
    profile_response = []
    for user in repo.repos:
        profile_response.append(
            GetProfileResponse(
                username=user.username,
                phone=user.phone,
                lastname=user.lastname,
                firstname=user.firstname,
                surname=user.surname,
                id=user.id,
            )
        )
    return profile_response


@user_router.get("/{id}")
def get_profile(id: UUID) -> GetProfileResponse | None:
    person = repo.get(id)
    if person:
        return GetProfileResponse(
            username=person.username,
            phone=person.phone,
            lastname=person.lastname,
            firstname=person.firstname,
            surname=person.surname,
            id=person.id,
        )
    raise HTTPException(status_code=404, detail=f"User with {id} not found")


@user_router.patch("/{id}")
def edit_profile(id: UUID, data: PatchProfileRequest) -> Profile | None:
    for person in repo.repos:
        if person.id == id:
            for k, v in data.model_dump().items():
                setattr(person, k, v)
            return person
    return None


@user_router.delete("/{id}")
def delete_profile(id: UUID):
    repo.delete(id)

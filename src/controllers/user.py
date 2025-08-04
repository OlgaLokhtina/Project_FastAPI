from typing import List
from fastapi import APIRouter, HTTPException
from models.user import Profile
from scheme.user import (CreateProfileRequest, CreateProfileResponse, PatchProfileRequest,
                         DeleteProfileRequest)
from uuid import UUID
from store.user_repo import repo


user_router = APIRouter(prefix="/user")


@user_router.post("/")
def create_profile(data: CreateProfileRequest) -> CreateProfileResponse:
    profile = Profile(**data.model_dump())
    repo.append(profile)
    return CreateProfileResponse(id=profile.id)


@user_router.get("/")
def get_all_profile() -> List[Profile]:
    return repo


@user_router.get("/{id}")
def get_profile(id: UUID) -> Profile | None:
    if not isinstance(id, UUID):
        raise HTTPException(status_code=404, detail="ID not!!")
    for person in repo:
        if person.id == id:
            return person
    raise HTTPException(status_code=404, detail="ID not found")


@user_router.patch("/{id}")
def edit_profile(id: UUID, data: PatchProfileRequest) -> Profile | None:
    for person in repo:
        if person.id == id:
            for k, v in data.model_dump().items():
                setattr(person, k, v)
            return person
    return None


@user_router.delete("/{id}")
def delete_profile(id: UUID) -> DeleteProfileRequest | None:
    for person in repo:
        if person.id == id:
            repo.remove(person)
            return DeleteProfileRequest(id=id)
    return None




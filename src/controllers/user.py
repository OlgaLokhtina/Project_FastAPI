from fastapi import APIRouter
from models.user import Profile
from scheme.user import CreateProfileRequest, CreateProfileResponse
from uuid import UUID
from store.user_repo import repo

user_router = APIRouter(prefix="/user")


@user_router.post("/")
def create_profile(data: CreateProfileRequest) -> CreateProfileResponse:
    profile = Profile(**data.model_dump())
    repo.append(profile)
    return CreateProfileResponse(id=profile.id)


@user_router.get("/")
def show_all_profile():
    return repo


@user_router.get("/{name}")
def show_profile(name: str):
    for person in repo:
        if person.username == name:
            return person
    return None

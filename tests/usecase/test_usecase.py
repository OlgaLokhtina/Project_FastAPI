from unittest.mock import patch
from uuid import UUID

from models.user import Profile
from scheme.user import CreateProfileRequest, GetProfileResponse, PatchProfileRequest
from store.sql_user_repo import SQLiteUserRepository
from usecases.user_usecase import UserUsecase


def test_create():
    repo = SQLiteUserRepository("test.db")
    usecase = UserUsecase(repo)
    scheme = CreateProfileRequest(
        username="username",
        lastname="lastname",
        firstname="firstname",
        surname="surname",
        phone="+76565454323",
    )
    with patch.object(usecase.repo, "save"):
        response = usecase.create(scheme)
        assert response.id is not None


def test_get():
    repo = SQLiteUserRepository("test.db")
    usecase = UserUsecase(repo)
    user = Profile(
        id=UUID("95362ffd-474f-4dcb-8777-3141ad1b463c"),
        username="Mary",
        phone="+45777777777",
        lastname="Smith",
        firstname="Marianna",
        surname="Mark",
    )
    with patch.object(repo, "get") as mock_get:
        mock_get.return_value = user
        prof = usecase.get(user.id)
        get_user = GetProfileResponse(**user.model_dump())
        assert prof == get_user


def test_list():
    repo = SQLiteUserRepository("test.db")
    usecase = UserUsecase(repo)
    user = Profile(
        id=UUID("95362ffd-474f-4dcb-8777-3141ad1b463c"),
        username="Mary",
        phone="+45777777777",
        lastname="Smith",
        firstname="Marianna",
        surname="Mark",
    )
    with patch.object(repo, "list") as mock_list:
        mock_list.return_value = [
            user,
        ]
        prof_list = usecase.list(1, 1)
        list_user = [
            GetProfileResponse(**user.model_dump()),
        ]
        assert prof_list == list_user


@patch("store.sql_user_repo.SQLiteUserRepository")
def test_update(mock_repo):
    repo = mock_repo("test.db")
    usecase = UserUsecase(repo)
    user = Profile(
        id=UUID("95362ffd-474f-4dcb-8777-3141ad1b463c"),
        username="Mary",
        phone="+45777777777",
        lastname="Smith",
        firstname="Marianna",
        surname="Mark",
    )
    repo.get.return_value = user
    usecase.update(
        user.id,
        PatchProfileRequest(
            phone="+45777777777", lastname="Smith", firstname="Marianna", surname="Mark"
        ),
    )
    assert repo.get(user.id) == user


@patch("store.sql_user_repo.SQLiteUserRepository")
def test_delete(mock_repo):
    repo = mock_repo("test.db")
    usecase = UserUsecase(repo)
    pr_id = UUID("95362ffd-474f-4dcb-8777-3141ad1b463c")
    r = usecase.delete(pr_id)
    assert r is None

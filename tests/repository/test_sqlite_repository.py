import sqlite3
from uuid import UUID

import pytest

from models.user import Profile
from store.sql_user_repo import SQLiteUserRepository


@pytest.fixture
def user():
    return Profile(
        id=UUID("95362ffd-474f-4dcb-8777-3141ad1b463c"),
        username="Shon",
        phone="+45678987654",
        lastname="Smith",
        firstname="Katerine",
        surname="John",
    )


@pytest.fixture
def user2():
    return Profile(
        id=UUID("95362ffd-474f-4dcb-8777-3141ad1b4637"),
        username="Mary",
        phone="+45777777777",
        lastname="Smith",
        firstname="Marianna",
        surname="Mark",
    )


@pytest.fixture()
def repo():
    rep = SQLiteUserRepository("sql.db")
    con = sqlite3.connect("sql.db")
    cur = con.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id TEXT NOT NULL,
                    username TEXT,
                    lastname TEXT,
                    firstname TEXT,
                    surname TEXT,
                    phone TEXT
                )
            """)
    con.commit()
    return rep


def test_exist_repo(repo, user):
    repo.save(user)
    assert repo.exist(UUID("95362ffd-474f-4dcb-8777-3141ad1b463c"))
    assert not repo.exist(UUID("95362ffd-474f-4dcb-8777-3141ad1b4637"))


def test_get_repo(repo, user):
    assert repo.get(user.id) == user


def test_list_repo(repo, user):
    repo.save(user)
    assert repo.list() == [user]


def test_save_repo(repo, user2):
    repo.save(user2)
    assert repo.get(user2.id) == user2


def test_delete_repo(repo, user, user2):
    repo.delete(user2.id)
    assert repo.list() == [user]

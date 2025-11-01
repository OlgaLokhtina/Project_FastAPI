import sqlite3
import uuid
from uuid import UUID

import pytest

from models.user import Profile
from store.sql_user_repo import SQLiteUserRepository

DB_NAME = "sql.db"


@pytest.fixture
def user():
    user = Profile(
        id=UUID("95362ffd-474f-4dcb-8777-3141ad1b463c"),
        username="Mary",
        phone="+45777777777",
        lastname="Smith",
        firstname="Marianna",
        surname="Mark",
    )
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO Users (id, username, lastname, "
        "firstname, surname, phone) VALUES (?, ?, ?, ?, ?, ?)",
        (
            str(user.id),
            user.username,
            user.lastname,
            user.firstname,
            user.surname,
            user.phone,
        ),
    )
    con.commit()
    yield user
    cur.execute("DELETE FROM Users WHERE id = ?", (str(user.id),))
    con.commit()


@pytest.fixture()
def repo():
    with sqlite3.connect(DB_NAME) as con:
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

    rep = SQLiteUserRepository(DB_NAME)
    return rep


def test_exist_repo(repo: SQLiteUserRepository, user: Profile):
    stat = repo.exist(UUID("95362ffd-474f-4dcb-8777-3141ad1b463c"))
    assert stat


def test_get_repo(repo: SQLiteUserRepository, user: Profile):
    person = repo.get(user.id)
    assert person == user


def test_list_repo(repo: SQLiteUserRepository, user: Profile):
    list_per = repo.list()
    assert len(list_per) == 1


def test_save_repo(repo: SQLiteUserRepository):
    user = Profile(
        id=uuid.uuid4(),
        username="Ann",
        phone="+45432543456",
        lastname="Bart",
        firstname="Anastasia",
        surname="Bob",
    )
    repo.save(user)
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE id = ?", (str(user.id),))
    person = cur.fetchone()
    user_dict = {
        "id": UUID(person[0]),
        "username": str(person[1]),
        "lastname": str(person[2]),
        "firstname": str(person[3]),
        "surname": str(person[4]),
        "phone": str(person[5]),
    }
    assert user_dict == user.model_dump()
    cur.execute("DELETE FROM Users WHERE id = ?", (str(user.id),))
    con.commit()


def test_delete_repo(repo: SQLiteUserRepository, user: Profile):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    repo.delete(user.id)
    cur.execute("SELECT * FROM Users WHERE id = ?", (str(user.id),))
    person = cur.fetchone()
    assert person is None

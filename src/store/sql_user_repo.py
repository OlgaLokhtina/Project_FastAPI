import sqlite3
from typing import Iterable
from uuid import UUID, uuid4

from models.user import Profile
from store.base import BaseUserRepository, UserNotFound


class SQLiteUserRepository(BaseUserRepository):
    def __init__(self, name: str):
        self.name = name
        connection = sqlite3.connect(name)
        connection.close()

    def get(self, profile_id: UUID) -> Profile:
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE id = ?", (str(profile_id),))
        user = cursor.fetchone()
        if user:
            user_dict = {
                "id": UUID(user[0]),
                "username": str(user[1]),
                "lastname": str(user[2]),
                "firstname": str(user[3]),
                "surname": str(user[4]),
                "phone": str(user[5]),
            }
            return Profile(**user_dict)
        else:
            connection.commit()
            connection.close()
            raise UserNotFound(profile_id)

    def list(self) -> Iterable[Profile]:
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        users_list = []
        for user in users:
            user_dict = {
                "id": UUID(user[0]),
                "username": str(user[1]),
                "lastname": str(user[2]),
                "firstname": str(user[3]),
                "surname": str(user[4]),
                "phone": str(user[5]),
            }
            users_list.append(user_dict)
        list_pr = [Profile(**u) for u in users_list]
        connection.close()
        return list_pr

    def save(self, profile: Profile) -> None:
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        ss = (profile.lastname, profile.firstname, profile.surname, profile.phone)
        try:
            self.get(profile.id)
            cursor.execute(
                "UPDATE Users SET lastname = ?, "
                "firstname =?, surname = ?, phone = ? WHERE id = ?",
                (*ss, str(profile.id)),
            )
        except UserNotFound:
            cursor.execute(
                "INSERT INTO Users (id, username, lastname, "
                "firstname, surname, phone) VALUES (?, ?, ?, ?, ?, ?)",
                (str(profile.id), profile.username, *ss),
            )
        finally:
            connection.commit()
            connection.close()

    def delete(self, profile_id) -> None:
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE id = ?", (str(profile_id),))
        user = cursor.fetchone()
        if user:
            cursor.execute("DELETE FROM Users WHERE id = ?", (str(profile_id),))
            connection.commit()
            connection.close()
        else:
            connection.commit()
            connection.close()
            raise UserNotFound(profile_id)


sql_repo = SQLiteUserRepository("sql_users.db")
con = sqlite3.connect("sql_users.db")
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
con.close()
sql_repo.save(
    Profile(
        id=uuid4(),
        username="Katty",
        phone="+45678987654",
        lastname="Smith",
        firstname="Katerine",
        surname="John",
    )
)

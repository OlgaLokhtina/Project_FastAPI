import sqlite3
from typing import Iterable
from uuid import UUID

from models.user import Profile
from store.base import BaseUserRepository, UserNotFound


class SQLiteUserRepository(BaseUserRepository):
    def __init__(self, name: str):
        self.name = name
        self.connection = sqlite3.connect(name, check_same_thread=False)

    def exist(self, profile_id: UUID) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE id = ?", (str(profile_id),))
        user = cursor.fetchone()
        return True if user else False

    def get(self, profile_id: UUID) -> Profile:
        if self.exist(profile_id):
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Users WHERE id = ?", (str(profile_id),))
            user = cursor.fetchone()
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
            raise UserNotFound(profile_id)

    def list(self) -> Iterable[Profile]:
        cursor = self.connection.cursor()
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
        return list_pr

    def save(self, profile: Profile) -> None:
        print("ooooo!")
        cursor = self.connection.cursor()
        ss = (profile.lastname, profile.firstname, profile.surname, profile.phone)
        if self.exist(profile.id):
            cursor.execute(
                "UPDATE Users SET lastname = ?, "
                "firstname =?, surname = ?, phone = ? WHERE id = ?",
                (*ss, str(profile.id)),
            )
        else:
            cursor.execute(
                "INSERT INTO Users (id, username, lastname, "
                "firstname, surname, phone) VALUES (?, ?, ?, ?, ?, ?)",
                (str(profile.id), profile.username, *ss),
            )
        self.connection.commit()

    def delete(self, profile_id) -> None:
        cursor = self.connection.cursor()
        if self.exist(profile_id):
            cursor.execute("DELETE FROM Users WHERE id = ?", (str(profile_id),))
            self.connection.commit()
        else:
            raise UserNotFound(profile_id)

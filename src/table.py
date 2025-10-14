import sqlite3

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

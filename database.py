import asyncio
import secrets

import asqlite

class DataManager:
    @classmethod
    async def initialise(cls) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            """CREATE TABLE IF NOT EXISTS auth_keys (
                key TEXT PRIMARY KEY,
                user TEXT
            )"""
        )
        await cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                user TEXT PRIMARY KEY,
                password TEXT
            )"""
        )
        await db.commit()
        await db.close()

    @classmethod
    async def add_column(cls, column_name, column_type) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            f"""ALTER TABLE auth_keys ADD COLUMN {column_name} {column_type}"""
        )
        await db.commit()
        await db.close()

    @classmethod
    async def create_auth_key(cls, user) -> None:
        key = secrets.token_urlsafe(16)
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            """INSERT INTO auth_keys (key, user) VALUES (?, ?)""", (key, user)
        )
        await db.commit()
        return key

    @classmethod
    async def delete_auth_key(cls, key) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""DELETE FROM auth_keys WHERE key=?""", (key,))
        await db.commit()
        await db.close()

    @classmethod
    async def check_user_from_keys(cls, user) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT * FROM auth_keys WHERE user=?""", (user,))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return False
        else:
            return True
        
    @classmethod
    async def check_user_from_users(cls, user) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT * FROM users WHERE user=?""", (user,))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return False
        else:
            return True

    @classmethod
    async def get_key(cls, user) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT * FROM auth_keys WHERE user=?""", (user,))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return None
        else:
            return result[0]

    @classmethod
    async def check_key(cls, key) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT * FROM auth_keys WHERE key=?""", (key,))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return False
        else:
            return True
        
    @classmethod
    async def sign_up(cls, user, password) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        if await cls.check_user_from_users(user):
            return False
        else:
            await cursor.execute("""INSERT INTO users (user, password) VALUES (?, ?)""", (user, password))
            await db.commit()
            await db.close()
            return True

    @classmethod
    async def log_in(cls, user, password) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT * FROM users WHERE user=?""", (user,))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return False
        else:
            if result[1] == password:
                return True
            else:
                return False

async def main():
    await DataManager.initialise()

if __name__ == "__main__":
    asyncio.run(main())
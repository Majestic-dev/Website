import asyncio
import secrets
import json
import os

import asqlite

class DataManager:

    @classmethod
    async def create_config_file(cls):
        if not os.path.exists('data/config.json'):
            config = {"host": ""}
            with open('config.json', 'w') as f:
                json.dump(config, f)

    @classmethod
    async def initialise(cls) -> None:
        await cls.create_config_file()

        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                user TEXT PRIMARY KEY,
                password TEXT,
                authentication_key TEXT
            )"""
        )
        await db.commit()
        await db.close()

    @classmethod
    async def add_column(cls, column_name: str, column_type: str) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            f"""ALTER TABLE users ADD COLUMN {column_name} {column_type}"""
        )
        await db.commit()
        await db.close()

    @classmethod
    async def check_if_user_exists(cls, user: str) -> bool:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT * FROM users WHERE user=?""", (user,))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return False # User does not exist
        else:
            return True # User exists

    @classmethod
    async def register_user(cls, user: str, password: str) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        if await cls.check_if_user_exists(user):
            return False # User already exists
        else:
            await cursor.execute(
                """INSERT INTO users (user, password) VALUES (?, ?)""", (user, password)
            )
            await db.commit()
            await db.close()
            return True # User registered
        
    @classmethod
    async def login_user(cls, user: str, password: str) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT * FROM users WHERE user=? AND password=?""", (user, password))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return False # Account details are incorrect
        else:
            return True # Account details are correct

    @classmethod
    async def create_authentication_key(cls, user: str, password: str) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        key = secrets.token_hex(16)

        if await DataManager.check_if_user_exists(user):
            if await DataManager.login_user(user, password):
                await cursor.execute(
                    """UPDATE users SET authentication_key = ? WHERE user = ? AND password = ?""", (key, user, password)
                )
                await db.commit()
                await db.close()
                return key
            else:
                return None
        else:
            return None

    @classmethod
    async def delete_authentication_key(cls, key) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""DELETE FROM users WHERE key=?""", (key,))
        await db.commit()
        await db.close()

    @classmethod
    async def get_authentication_key(cls, user) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT authentication_key FROM users WHERE user=?""", (user,))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return None
        else:
            return result[0]  # Extract the value from the Row object

    @classmethod
    async def check_key(cls, key) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute("""SELECT * FROM users WHERE key=?""", (key,))
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return False # Key does not exist
        else:
            return True # Key exists

async def main():
    await DataManager.initialise()

if __name__ == "__main__":
    asyncio.run(main())
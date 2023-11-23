import asqlite
import os
import asyncio
import secrets

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
    async def delete_column(cls, column_name) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            f"""ALTER TABLE auth_keys DROP COLUMN {column_name}"""
            )
        await db.commit()
        await db.close()

    @classmethod
    async def create_auth_key(cls, user) -> None:
        key = secrets.token_urlsafe(16)
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            """INSERT INTO auth_keys (key, user) VALUES (?, ?)""",
            (key, user)
        )
        await db.commit()
        return key
    
    @classmethod
    async def delete_auth_key(cls, key) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            """DELETE FROM auth_keys WHERE key=?""",
            (key,)
        )
        await db.commit()
        await db.close()
    
    @classmethod
    async def check_user(cls, user) -> None:
        db = await asqlite.connect("data/data.db")
        cursor = await db.cursor()
        await cursor.execute(
            """SELECT * FROM auth_keys WHERE user=?""",
            (user,)
        )
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
        await cursor.execute(
            """SELECT * FROM auth_keys WHERE user=?""",
            (user,)
        )
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
        await cursor.execute(
            """SELECT * FROM auth_keys WHERE key=?""",
            (key,)
        )
        result = await cursor.fetchone()
        await db.close()
        if result is None:
            return False
        else:
            return True

async def main():
    await DataManager.initialise()

if __name__ == "__main__":
    asyncio.run(main())
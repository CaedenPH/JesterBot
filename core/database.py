from __future__ import annotations

import typing as t
import aiosqlite


class Database:
    def __init__(self):
        self.db: aiosqlite.Connection

    @classmethod
    async def create(cls: t.Type[Database]) -> Database:
        self = cls()
        self.db = await aiosqlite.connect("./db/database.db")

        with open("./schema.sql") as file:
            await self.db.executescript(file.read())
        return self

    async def execute(self, query: str, *args: t.Any) -> str:
        async with self.db.cursor() as cur:
            return await cur.execute(query, *args)

    async def update(self, query: str, *args: t.Any) -> str:
        async with self.db.cursor() as cur:
            resp = await cur.execute(query, *args)
            await self.db.commit()
            return resp

    async def fetchone(self, query: str, *args: t.Any) -> t.Tuple:
        async with self.db.cursor() as cur:
            return await (await cur.execute(query, *args)).fetchone()

    async def fetchall(self, query: str, *args: t.Any) -> t.Tuple:
        async with self.db.cursor() as cur:
            return await (await cur.execute(query, *args)).fetchall()

from __future__ import annotations

import aiohttp
import os
import asyncio
import datetime
import aiosqlite

from typing import List
from disnake import Activity, ActivityType, Intents, Message
from disnake.ext.commands import Bot, when_mentioned_or
from disnake.ext.tasks import loop

from .utils.commands.eval import run_eval
from .utils import run_channel_send, run_check, run_executed, run_precheck
from .constants import BOT_TOKEN, WEATHER_KEY, POLICE_KEY, COORDS_KEY, CHATBOT_KEY
from .errors import error_handler
from .context import Context


class JesterBot(Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix,
            intents=Intents.all(),
            case_insensitive=True,
            strip_after_prefix=True,
            owner_ids=[298043305927639041],
            help_command=None,
        )

        self.launch_time = datetime.datetime.utcnow()
        self.COGS: list = list()
        self.time_limit: int = 120
        self.disnakecolor = 0x36393F
        self.hiber = False
        self.data = {}

        self.WEATHER_KEY = WEATHER_KEY
        self.POLICE_KEY = POLICE_KEY
        self.COORDS_KEY = COORDS_KEY
        self.CHATBOT_KEY = CHATBOT_KEY

        self.add_check(self.bot_check)
        self.after_invoke(self.after_command)
        self.loop.create_task(self.connect_database())

        for file in os.listdir(f"./cogs/"):
            if not file.startswith("_"):
                self.COGS.append(f"cogs.{file}")

    async def find_prefix(self, user_id: int) -> List[str]:
        cursor = await self.db.cursor()
        await cursor.execute(
            "SELECT prefixes FROM prefix WHERE user_id = ?", (user_id,)
        )
        result = await cursor.fetchone()

        if not result:
            return ["j."]
        return result[0].split(" | ")

    async def insert_prefix(self, user_id: int, prefixes: List[str]) -> None:
        prefixes = " | ".join(prefixes)

        cursor = await self.db.cursor()
        await cursor.execute(
            "SELECT prefixes FROM prefix WHERE user_id = ?", (user_id,)
        )
        result = await cursor.fetchone()
        if not result:
            await cursor.execute(
                "INSERT INTO prefix VALUES (?, ?)", (user_id, prefixes)
            )
            return await self.db.commit()
        await cursor.execute(
            "UPDATE prefix SET prefixes = ? where user_id = ?", (prefixes, user_id)
        )
        await self.db.commit()

    async def get_prefix(self, message: Message) -> List[str]:
        prefixes = await self.find_prefix(message.author.id)
        return when_mentioned_or(*prefixes)(self, message)

    async def process_commands(self, message: Message) -> None:
        ctx = await self.get_context(message, cls=Context)
        await self.invoke(ctx)

    def setup(self) -> None:
        print("Cogs:\n-----------------------------------")
        print(", ".join(self.COGS))
        for filename in self.COGS:
            if filename.endswith("py"):
                self.load_extension(f"{filename[:-3]}")
            else:
                self.load_extension(filename)
        self.load_extension("jishaku")
        self.load_extension("disnake-debug")
        print(
            f"Loaded Cogs Successfully! Total Cogs: {len(self.COGS)}\n-----------------------------------"
        )

    @loop(seconds=3600.0)
    async def chansend(self) -> None:
        await run_channel_send(self)

    @loop(seconds=540)
    async def update_presence(self) -> None:
        await self.change_presence(
            activity=Activity(
                type=ActivityType.listening, name="ping me for prefix // j.help"
            )
        )
        await asyncio.sleep(180)
        await self.change_presence(
            activity=Activity(
                type=ActivityType.watching,
                name=f"ping me for prefix // {len(self.users)} Members in {len(self.guilds)} Servers!",
            )
        )
        await asyncio.sleep(180)
        await self.change_presence(
            activity=Activity(
                type=ActivityType.playing,
                name=f"ping me for prefix // {len([e for e in self.commands if not e.hidden])} commands",
            )
        )
        await asyncio.sleep(180)

    def run(self) -> None:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("Setting up...")
        print("-----------------------------------")
        self.setup()
        print("Running the bot...")
        print("-----------------------------------")
        super().run(BOT_TOKEN, reconnect=True)

    async def connect_database(self):
        self.db = await aiosqlite.connect("./db/database.db")

    async def on_connect(self) -> None:
        print(f"Connected to bot. Latency: {self.latency * 1000:,.0f} ms")

    async def on_disconnect(self) -> None:
        print("Client Disconnected.")

    async def on_ready(self) -> None:
        self.update_presence.start()
        print("Client Ready!")
        self.chansend.start()
        print("Guilds:\n-----------------------------------")
        guild_ids = [guild.id for guild in self.guilds]
        print(guild_ids)

        selected_channel = self.get_guild(830161446523371540).get_channel(
            830161446523371545
        )
        self.chan = selected_channel
        self.dev = await self.fetch_user(298043305927639041)
        guild = self.get_guild(830161446523371540)
        role = guild.get_role(857347445398044704)
        print("Admins:\n-----------------------------------")
        for k in role.members:
            print(k)
            self.owner_ids.append(k.id)
        self.client: aiohttp.ClientSession = aiohttp.ClientSession()

    async def on_message_edit(self, before: Message, after: Message) -> None:
        if before.author.bot:
            return
        if before.content == after.content:
            return
        time_difference = after.edited_at - before.created_at
        if time_difference.seconds > self.time_limit:
            return
        ctx = await self.get_context(after)
        if ctx.command:
            if before in self.data:
                if ctx.command.name in ["eval", "evaldir", "evalreturn"]:
                    code = " ".join(after.content.split(" ")[1:])
                    msg = await run_eval(ctx, code, eval=ctx.command.name)
                    try:
                        bot_msg = self.data[before]["bot"]
                        return await bot_msg.edit(content=msg)
                    except Exception as e:
                        return print(e)
            await self.process_commands(after)

    async def on_command_error(self, context, exception) -> None:
        await error_handler(context, exception)

    async def on_guild_remove(self, guild) -> None:
        selected_channel1 = self.get_guild(830161446523371540).get_channel(
            865309892776951808
        )
        await selected_channel1.send(f"I have left {guild.name}.")

    async def bot_check(self, ctx) -> bool:
        return await run_check(self, ctx)

    async def on_message(self, message) -> None:
        await run_precheck(self, message)
        return await super().on_message(message)

    async def after_command(self, ctx):
        await run_executed(ctx)

    async def close(self) -> None:
        await self.client.close()
        return await super().close()

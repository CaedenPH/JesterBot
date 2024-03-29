from __future__ import annotations

import asyncio
import datetime
import os
from typing import List

import aiohttp
from disnake import (
    Activity,
    ActivityType,
    AllowedMentions,
    Intents,
    Message,
    __version__,
)
from disnake.ext.commands import Bot, when_mentioned_or
from disnake.ext.tasks import loop

from .constants import (
    BOT_TOKEN,
    CHATBOT_KEY,
    COORDS_KEY,
    RAPID_API_KEY,
    REDDIT,
    WEATHER_KEY,
)
from .context import Context
from .database import Database
from .errors import error_handler
from .utils import run_check, run_executed, run_precheck, send_embed
from .utils.comedy import fact, joke, pickup, quote
from .utils.commands.eval import run_eval


class JesterBot(Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix,
            intents=Intents.all(),
            case_insensitive=True,
            strip_after_prefix=True,
            owner_ids=[298043305927639041],
            allowed_mentions=AllowedMentions.none(),
            help_command=None,
        )

        self.launch_time = datetime.datetime.utcnow()
        self.COGS: list = list()
        self.time_limit: int = 120
        self.discord_colour = 0x36393F
        self.hiber = False
        self.data = {}

        self.WEATHER_KEY = WEATHER_KEY
        self.COORDS_KEY = COORDS_KEY
        self.CHATBOT_KEY = CHATBOT_KEY
        self.RAPID_API_KEY = RAPID_API_KEY

        self.add_check(self.bot_check)
        self.after_invoke(self.after_command)
        self.loop.create_task(self.connect_database())

        for file in os.listdir("./cogs/"):
            if not file.startswith("_"):
                self.COGS.append(f"cogs.{file}")

    async def connect_database(self):
        self.db = await Database.create()

    async def find_prefix(self, user_id: int) -> List[str]:
        result = await self.db.fetchone(
            "SELECT prefixes FROM prefix WHERE user_id = ?", (user_id,)
        )

        if not result:
            return ["j."]
        return result[0].split(" | ")

    async def insert_prefix(self, user_id: int, prefixes: List[str]) -> None:
        prefixes = " | ".join(prefixes)

        result = await self.db.fetchone(
            "SELECT prefixes FROM prefix WHERE user_id = ?", (user_id,)
        )
        if not result:
            return await self.db.update(
                "INSERT INTO prefix VALUES (?, ?)", (user_id, prefixes)
            )
        await self.db.update(
            "UPDATE prefix SET prefixes = ? where user_id = ?", (prefixes, user_id)
        )

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

    @loop(seconds=60)
    async def log_data(self) -> None:
        await self.db.update(
            "INSERT INTO general_data VALUES (?, ?, ?, ?, ?, ?)",
            (
                datetime.datetime.utcnow().isoformat(),
                self.latency * 1000,
                len(self.users),
                len(self.guilds),
                len([c for c in self.get_all_channels()]),
                __version__,
            ),
        )

    @log_data.before_loop
    async def log_data_pre(self) -> None:
        await self.wait_until_ready()

    @loop(seconds=3600)
    async def cache_memes(self) -> None:
        subreddit = await REDDIT.subreddit("memes")
        self.meme_list = [p async for p in subreddit.hot(limit=200)]

    @loop(seconds=3600)
    async def send_comedy(self) -> None:
        result = await self.db.fetchall(
            "SELECT channel_id, channel_types FROM channels_config"
        )

        for channel_id, channel_types in result:
            channel = self.get_channel(channel_id)

            types = channel_types.split(" | ")
            for _type in types:
                if _type == "joke":
                    response = await joke()
                if _type == "pickup":
                    response = await pickup(self)
                if _type == "fact":
                    response = await fact()
                if _type == "quote":
                    response = await quote(self)
                try:
                    await send_embed(channel, _type, response)
                except AttributeError:
                    return

    @send_comedy.before_loop
    async def send_comedy_pre_loop(self) -> None:
        await self.wait_until_ready()

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

    async def on_ready(self) -> None:
        self.update_presence.start()
        print("Client Ready!")
        self.send_comedy.start()
        self.cache_memes.start()
        self.log_data.start()
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
        self.client = aiohttp.ClientSession()

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
                    except Exception:
                        return
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

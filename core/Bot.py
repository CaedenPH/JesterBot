import aiohttp
import disnake
import os
import asyncio
import datetime
import aiosqlite

from disnake.ext import commands, tasks
from core.utils.commands.eval import run_eval
from core.Context import Context
from core.Error import error_handler
from core.main.check import *
from core.main.prefix import get_prefix
from core.utils.HIDDEN import *

class JesterBot(commands.Bot):
    def __init__(self):
        super().__init__(

            command_prefix=get_prefix, 
            intents=disnake.Intents.all(),
            case_insensitive=True,
            strip_after_prefix=True,
            owner_ids=[298043305927639041],
            help_command=None

        )
        
        self.launch_time = datetime.datetime.utcnow()
        self.COGS:list = list()
        self.time_limit:int = 120
        self.disnakecolor = 0x36393F
        self.hiber = False
        self.data = {}

        self.WEATHER_KEY = weather_key
        self.POLICE_KEY = police_key
        self.COORDS_KEY = coords_key
        self.CHATBOT_KEY = chatbot_key

        self.add_check(self.bot_check)
        self.after_invoke(self.after_command)
        self.loop.create_task(self.connect_database())
        
        for files in os.listdir(f"./cogs/"):
            if not files.startswith('__'):
                if files.endswith(".py"):
                    self.COGS.append(f"cogs.{files}")

                

    async def process_commands(self, message: disnake.Message) -> None:
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is None:
            return
        await self.invoke(ctx)

    def setup(self) -> None:
        print("Cogs:\n-----------------------------------")
        print(", ".join(self.COGS))
        for filename in self.COGS:
            self.load_extension(f"{filename[:-3]}")
        self.load_extension('jishaku')
        print(f"Loaded Cogs Successfully! Total Cogs: {len(self.COGS)}\n-----------------------------------")

    @tasks.loop(seconds=3600.0)
    async def chansend(self) -> None:
        await run_channel_send(self) 

    @tasks.loop(seconds=540)
    async def update_presence(self) -> None:
        x:int = 0
        for guild in self.guilds:
            for k in guild.members:
                x += 1
        await self.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening, name="ping me for prefix // j.help"))
        await asyncio.sleep(180)
        await self.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name=f"ping me for prefix // {x} Members in {len(self.guilds)} Servers!"))
        await asyncio.sleep(180)
        await self.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=f"ping me for prefix // {len([e for e in self.commands if not e.hidden])} commands"))
        await asyncio.sleep(180)
    
    def run(self) -> None:
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print('Setting up...')
        print('-----------------------------------')
        self.setup()
        print('Running the bot...')
        print('-----------------------------------')
        super().run(TOKEN, reconnect=True)

    async def connect_database(self):
        self.db = await aiosqlite.connect('./db/database.db')

    async def on_connect(self) -> None:
        print(f"Connected to bot. Latency: {self.latency * 1000:,.0f} ms")

    async def on_disconnect(self) -> None:
        print("Client Disconnected.")
    
    async def on_ready(self) -> None:
        self.update_presence.start()
        print("Client Ready!")
        self.chansend.start()
        print("Guilds:\n-----------------------------------")
        guild_ids = []
        for guild1 in self.guilds:
            guild_ids.append(guild1.id)
        print(guild_ids)

        selected_channel = self.get_guild(830161446523371540).get_channel(830161446523371545)
        self.chan = selected_channel
        self.dev = await self.fetch_user(298043305927639041)
        guild = self.get_guild(830161446523371540)
        role = guild.get_role(857347445398044704)
        print("Admins:\n-----------------------------------")
        for k in role.members:
            print(k)
            self.owner_ids.append(k.id)

        self.client = aiohttp.ClientSession()

    async def process_commands(self, message: disnake.Message) -> None:
        ctx = await self.get_context(message, cls=Context)
        await self.invoke(ctx)

    async def on_message_edit(self, before: disnake.Message, after: disnake.Message) -> None:
        if before.author.bot:
            return
        if before.content == after.content:
            return
        time_difference = after.edited_at - before.created_at
        if time_difference.seconds > self.time_limit:
            return
        ctx = await self.get_context(after)
        pref = await self.get_prefix(ctx.message)
        if ctx.command:
            if before in self.data:
                if ctx.command.name in ['eval', 'evaldir', 'evalreturn']:
                    code = " ".join(after.content.split(' ')[1:])
                    msg = await run_eval(ctx, code, eval=ctx.command.name)
                    try:
                        bot_msg = self.data[before]['bot']
                        return await bot_msg.edit(content=msg)
                    except Exception as e:
                        return print(e)

            await self.process_commands(after)

    async def on_command_error(self, context, exception) -> None:
        await error_handler(self, context, exception)
    
    async def on_guild_remove(self, guild) -> None:
        selected_channel1 = self.get_guild(830161446523371540).get_channel(865309892776951808)
        await selected_channel1.send(f'I have left {guild.name}.')
    
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

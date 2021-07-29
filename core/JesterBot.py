import discord, os, requests, json, asyncio, datetime
from discord.ext import commands 
from discord.ext import tasks
from discord import Intents

from core.utils.utils import thecolor, Json, thebed
from core.Context import Context
from core.Error import error_handler
from core.main.prefix import get_prefix

from dislash import *

class JesterBot(commands.Bot):
    def __init__(self):
        
        super().__init__(

            command_prefix=get_prefix, 
            intents=discord.Intents.all(),
            case_insensitive=True,
            strip_after_prefix=True,
            owner_ids=[298043305927639041, 521226389559443461],
            help_command=None

        )
        
        self.launch_time = datetime.datetime.utcnow()
        self.COGS:list = list()
        self.time_limit:int = 120
        self.discordcolor = 0x36393F
        self.hiber = False
        self.suglist = []
           
        
        
        for files in os.listdir(f"./cogs/"):
            if not files.startswith('__'):
                if files.endswith(".py"):
                    self.COGS.append(f"cogs.{files}")

    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is None:
            return

    def setup(self) -> None:
        print(" ~ ".join(self.COGS))
        for filename in self.COGS:
            self.load_extension(f"{filename[:-3]}")
        print(f"Loaded Cogs Successfully! Total Cogs: {len(self.COGS)}")

    @tasks.loop(seconds=3600.0)
    async def chansend(self):
        await run_channel_send(self) 

    @tasks.loop(seconds=540)
    async def update_presence(self):
        x:int = 0
        for guild in self.guilds:
            for k in guild.members:
                x += 1
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ping me for prefix // j.help"))
        await asyncio.sleep(180)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ping me for prefix // {x} Members in {len(self.guilds)} Servers!"))
        await asyncio.sleep(180)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"ping me for prefix // {len([e for e in self.commands if not e.hidden])} commands"))
        await asyncio.sleep(180)
    
    def run(self) -> None:

        print('Setting up...')
        self.setup()
        TOKEN = 'ODI4MzYzMTcyNzE3MTMzODc0.YGofUg.LNFtFiYeyTKfgPDcDdUpvGjDXbg'
        print('Running the bot...')
        super().run(TOKEN, reconnect=True)

    async def on_connect(self) -> None:
        print(f"Connected to bot. Latency: {self.latency * 1000:,.0f} ms")

    async def on_disconnect(self) -> None:
        print("Client Disconnected.")

    async def on_ready(self) -> None:
        print('Started')
        self.update_presence.start()
        print("Client Ready!")
        self.chansend.start()

        guild_ids = []
        for guild1 in self.guilds:
            guild_ids.append(guild1.id)
        print(guild_ids)
        slash = SlashClient(self)

        selected_channel = self.get_guild(830161446523371540).get_channel(830161446523371545)
        self.chan = selected_channel
        self.dev = await self.fetch_user(298043305927639041)

    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=Context)
        await self.invoke(ctx)

    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        if before.author.bot:
            return
        if before.content == after.content:
            return
        time_diff = after.edited_at - before.created_at
        if time_diff.seconds > self.time_limit:
            return
        await self.process_commands(after)

    async def on_command_error(self, context, exception):
        await error_handler(self, context, exception)
    
    async def on_guild_remove(self, guild):
        selected_channel1 = self.get_guild(830161446523371540).get_channel(865309892776951808)
        await selected_channel1.send(f'I have left {guild.name}.')
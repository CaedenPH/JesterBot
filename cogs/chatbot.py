import typing

import disnake
from disnake.ext import commands

from core import Context, JesterBot
from core.constants import CHATBOT_KEY, RAPID_API_KEY


class ChatBot(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot: JesterBot = bot

    async def find_or_insert_channel(self, channel_id: int, **kwargs) -> bool:
        insert = kwargs.get("insert", False)
        remove = kwargs.get("remove", False)

        result = await self.bot.db.fetchone(
            "Select * from chatbot where channel_id = ?", (channel_id,)
        )
        if not result:
            if not insert:
                return False
            await self.bot.db.execute("Insert into chatbot values (?)", (channel_id,))
        if remove:
            await self.bot.db.execute(
                "Delete from chatbot where channel_id = ?", (channel_id,)
            )
        return True

    async def get_response(self, message: str, user_id: int) -> typing.Optional[str]:
        async with self.bot.client.get(
            url="https://random-stuff-api.p.rapidapi.com/ai",
            headers={
                "authorization": CHATBOT_KEY,
                "x-rapidapi-key": RAPID_API_KEY,
                "x-rapidapi-host": "random-stuff-api.p.rapidapi.com",
            },
            params={"msg": message, "id": user_id},
        ) as response:
            json = await response.json()

        if "error" in json:
            return None
        return json["AIResponse"]

    @commands.command(aliases=["setup", "setup_ai"])
    async def setup_chatbot(self, ctx: Context, channel: disnake.TextChannel) -> None:
        await ctx.em(f"Setting up my ai capabilites in {channel.name}...")

        await self.find_or_insert_channel(channel.id, insert=True)
        await channel.send(embed=disnake.Embed(description="Chatbot is setup!"))

        await ctx.em("All set up!")

    @commands.command(aliases=["remove"])
    async def remove_ai(self, ctx: Context, channel: disnake.TextChannel) -> None:
        await ctx.em(f"Removing my ai capabilites in {channel.name}...")

        await self.find_or_insert_channel(channel.id, remove=True)
        await channel.send(embed=disnake.Embed(description="Chatbot is removed!"))

        await ctx.em("All removed!")

    @commands.command(aliases=["ai"])
    async def chatbot(self, ctx: Context, *, message: str) -> None:
        response = await self.get_response(message, ctx.author.id)
        await ctx.reply(response)

    @commands.Cog.listener("on_message")
    async def chatbot_on_message(self, message: disnake.Message) -> None:
        active_channel = await self.find_or_insert_channel(message.channel.id)
        if not active_channel:
            return
        if message.author.bot:
            return

        response = await self.get_response(message.content, message.author.id)
        await message.channel.send(response)


def setup(bot: JesterBot) -> None:
    bot.add_cog(ChatBot(bot))

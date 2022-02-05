import typing
import disnake

from disnake.ext import commands
from core.Context import Context
from core.Bot import JesterBot
from core.utils.HIDDEN import ai_key, rapid_key


class ChatBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: JesterBot = bot

    async def find_or_insert_channel(self, channel_id: int, **kwargs):
        insert = kwargs.get("insert", False)
        remove = kwargs.get("remove", False)

        cursor = await self.bot.db.cursor()

        await cursor.execute(
            "Select * from chatbot where channel_id = ?", (channel_id,)
        )
        result = await cursor.fetchone()

        if not result:
            if not insert:
                return False
            await cursor.execute("Insert into chatbot values (?)", (channel_id,))

        if remove:
            await cursor.execute(
                "Delete from chatbot where channel_id = ?", (channel_id,)
            )

        return True

    async def get_response(self, message: str, ctx: Context) -> typing.Optional[str]:
        async with self.bot.client.get(
            url=f"https://random-stuff-api.p.rapidapi.com/ai",
            headers={
                "authorization": ai_key,
                "x-rapidapi-host": "random-stuff-api.p.rapidapi.com",
                "x-rapidapi-key": rapid_key,
            },
            params={"msg": message, "id": ctx.author.id},
        ) as resp:
            json = await resp.json()

        if "error" in json:
            return None
        return json["AIResponse"]

    async def send_ai(self, channel: Context, message: str, avatar_url=None) -> None:
        response = await self.get_response(message, channel)

        embed = disnake.Embed(description="").set_author(
            icon_url=avatar_url or disnake.Embed.Empty, name="Chatbot"
        )
        if not response:
            embed.description = "Something went wrong!"
            return await channel.send(embed=embed)

        embed.description = f"```yaml\n{response}```"
        await channel.send(embed=embed)

    @commands.command(aliases=["ai"])
    async def chatbot(self, ctx: Context, *, message: str) -> None:
        await self.send_ai(ctx.channel, message)

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

    @commands.Cog.listener("on_message")
    async def chatbot_on_message(self, message: disnake.Message) -> None:
        is_channel = await self.find_or_insert_channel(message.channel.id)

        if not is_channel:
            return
        if message.author.bot:
            return
        await self.send_ai(message.channel, message.content)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ChatBot(bot))

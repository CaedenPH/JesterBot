import disnake
from disnake.ext import commands
from random import choice, randint

from core.utils import get_colour, send_embed
from core.utils.comedy import fact, quote, joke, pickup
from core import Context
from core.utils.comedy import joke


class JesterJokes(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command(
        aliases=["ranfact", "rf", "randomfact"],
        description="""Returns a random fact [ranfact, rf]""",
    )
    async def fact(self, ctx: Context):
        fact_string = await fact()
        await send_embed(ctx, "Fact", fact_string)

    @commands.command(description="""Returns a random quote""")
    async def quote(self, ctx: Context):
        quote_string = await quote(self.bot)
        await send_embed(ctx, "Quote", quote_string)

    @commands.command(
        aliases=["pl", "pickup", "pickline"],
        description="""Returns a random Pickup Line.""",
    )
    async def pickup_line(self, ctx: Context):
        pickup_line = await pickup()
        await send_embed(ctx, "Pickup line", pickup_line)

    @commands.command(
        aliases=["insultme", "Mean", "Insult_Me"],
        description="The specified member gets insulted",
    )
    async def insult(self, ctx: Context, user: disnake.Member = ""):

        m = self.bot.get_user(828363172717133874)
        if user == "":
            user = self.bot.get_user(ctx.author.id)

        if user == m:
            embed = disnake.Embed(colour=get_colour())
            user = self.bot.get_user(ctx.author.id)
            embed = disnake.Embed(title="You shmuck...I am god")
            await ctx.reply(embed=embed)
        else:
            async with self.bot.client.get(url="https://insult.mattbas.org/api/insult.json") as response:
                fox = await response.json()
            foxupdate = fox["insult"]
            embed = disnake.Embed(description=f"{user.mention} {foxupdate}", colour=get_colour())
            await ctx.reply(embed=embed)

    @commands.command(aliases=["dis", "Diss"], description="The specified member gets dissed")
    async def disthem(self, ctx: Context, user: disnake.Member = ""):
        if user == "":
            user = self.bot.get_user(ctx.author.id)
        async with self.bot.client.get(url="https://evilinsult.com/generate_insult.php?lang=en&type=json") as response:
            fox = await response.json()
        foxupdate = fox["insult"]

        embed = disnake.Embed(description=f"{user.mention} {foxupdate}", colour=get_colour())
        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["Chuck_norris", "Chucky", "norris"],
        description="Sends a random chuck norris joke/fact",
    )
    async def chuck(self, ctx: Context, user: disnake.Member = ""):
        if user == "":
            user = self.bot.get_user(ctx.author.id)
        async with self.bot.client.get(url="https://api.chucknorris.io/jokes/random") as response:
            fox = await response.json()
        foxupdate = fox["value"]

        embed = disnake.Embed(description=f"{foxupdate}", colour=get_colour())
        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["adj", "random_adj", "randadj", "Rand_Adj", "random_adjective"],
        description="Sends a random adjective",
    )
    async def adjective(self, ctx: Context):

        async with self.bot.client.get(
            url="https://raw.githubusercontent.com/dariusk/corpora/master/data/words/adjs.json"
        ) as response:
            fox = await response.json()
        foxupdate = fox["adjs"]

        embed = disnake.Embed(title=f"{foxupdate[randint(1, 950)]}", colour=get_colour())

        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["smck", "slap", "BitchSlap", "Hit", "Spank"],
        description="The specified member gets slapped - Sends a random giffy",
    )
    async def smack(self, ctx: Context, user: disnake.Member = ""):
        if user == "":
            user = self.bot.get_user(ctx.author.id)

        url = [
            "https://media.giphy.com/media/l5JdQaCUXTGy7AIGHq/giphy.gif",
            "https://media.giphy.com/media/11N2zX8Swp3csg/giphy.gif",
            "https://media.giphy.com/media/xUA7b9Wc1uaT52QfO8/giphy.gif",
            "https://media.giphy.com/media/3oEduOWVxygmeDIKPu/giphy.gif",
            "https://media.giphy.com/media/Qumf2QovTD4QxHPjy5/giphy.gif",
            "https://media.giphy.com/media/uqSU9IEYEKAbS/giphy.gif",
            "https://media.giphy.com/media/lX03hULhgCYQ8/giphy.gif",
            "https://media.giphy.com/media/mEtSQlxqBtWWA/giphy.gif",
            "https://media.giphy.com/media/gSIz6gGLhguOY/giphy.gif",
            "https://media.giphy.com/media/uG3lKkAuh53wc/giphy.gif",
            "https://media.giphy.com/media/P1EomtpqQW34c/giphy.gif",
            "https://media.giphy.com/media/vxvNnIYFcYqEE/giphy.gif",
            "",
        ]

        embed = disnake.Embed(description=f"{user.mention} got smacked", colour=get_colour())
        embed.set_image(url=choice(url))
        await ctx.reply(embed=embed)

    @commands.command(aliases=["jokes"], description="Sends a random joke")
    async def joke(self, ctx: Context):
        await send_embed(ctx, "Joke", await joke())


def setup(bot):
    bot.add_cog(JesterJokes(bot))

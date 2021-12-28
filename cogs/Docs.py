import disnake
import itertools

from disnake.ext import commands
from docs import cog 
from core.utils.docs import *
from core.Context import Context

class Docs(cog.Docs, RTFM):
    BASE_PYPI_URL = "https://pypi.org"
    URL = f"{BASE_PYPI_URL}/pypi/{{package}}/json"
    PYPI_ICON = "https://cdn.discordapp.com/emojis/766274397257334814.png"
    PYPI_COLOURS = itertools.cycle((Colours.yellow, Colours.blue, Colours.white))
    
    def __init__(self, bot):
        super().__init__(
            bot
        )
        self.items = (
            ('disnake', 'https://disnake.readthedocs.io/en/latest/'),
            ('python', 'https://docs.python.org/3/'),
            ('aiohttp', 'https://aiohttp.readthedocs.io/en/stable/'),
        )
        self.bot = bot

    @commands.command()
    async def rtfm(self, ctx: Context, query):
        await self.do_rtfm(ctx, 'latest', query)

    @commands.command()
    async def pypi(self, ctx: Context, package):
        embed = disnake.Embed(
            title="",
            description=""
        ).set_thumbnail(
            url=self.PYPI_ICON
        )
        async with self.bot.client.get(self.URL.format(package=package)) as response:
            if response.status == 404:
                embed.description = "Package could not be found."
            elif response.status == 200 and response.content_type == "application/json":
                response_json = await response.json()

                info = response_json["info"]
                embed.title = f"{info['name']} v{info['version']}"
                embed.url = info["package_url"]
                embed.colour = next(self.PYPI_COLOURS)

                summary = disnake.utils.escape_markdown(info["summary"])

                if summary and not summary.isspace():
                    embed.description = summary
                else:
                    embed.description = "No summary provided."

            else:
                embed.description = "There was an error when fetching your PyPi package."

        await ctx.send(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Docs(bot))
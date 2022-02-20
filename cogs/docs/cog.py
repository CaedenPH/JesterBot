import disnake
import itertools
import os

from disnake.ext import commands
from fuzzywuzzy import fuzz
from docs import cog

from core import Context
from core.constants import ZEN_OF_PYTHON
from . import Paginator, RTFM, Colours


class Docs(cog.Docs, RTFM):
    BASE_PYPI_URL = "https://pypi.org"
    URL = f"{BASE_PYPI_URL}/pypi/{{package}}/json"
    PYPI_ICON = "https://cdn.discordapp.com/emojis/766274397257334814.png"
    PYPI_COLOURS = itertools.cycle((Colours.yellow, Colours.blue, Colours.white))
    TAGS = [k[:-3] for k in os.listdir("./resources/tags")]

    def __init__(self, bot):
        super().__init__(bot)
        self.items = (
            ("disnake", "https://disnake.readthedocs.io/en/latest/"),
            ("python", "https://docs.python.org/3/"),
            ("aiohttp", "https://aiohttp.readthedocs.io/en/stable/"),
        )
        self.bot = bot

    def get_tag_embed(self, author: disnake.Member, tag: str):
        tag = max([(_tag, fuzz.ratio(tag, _tag)) for _tag in self.TAGS], key=lambda m: m[1])[0]

        return (
            disnake.Embed(
                title=tag.capitalize(), description=open(f"./resources/tags/{tag}.md", encoding="utf-8").read()
            )
            .set_author(name=author.name, icon_url=author.avatar.url)
            .set_footer(text="Use tag_list command to see all tags")
        )

    @commands.command()
    async def rtfm(self, ctx: Context, query):
        await self.do_rtfm(ctx, "latest", query)

    @commands.command()
    async def pypi(self, ctx: Context, package):
        embed = disnake.Embed(title="", description="").set_thumbnail(url=self.PYPI_ICON)
        async with self.bot.client.get(self.URL.format(package=package)) as response:
            if response.status == 404:
                embed.description = "Package could not be found."
            elif response.status == 200 and response._type == "application/json":
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
        await ctx.reply(embed=embed)

    @commands.command(name="tag", aliases=["tags"])
    async def _tag(self, ctx: Context, tag: str = None) -> None:
        if not tag:
            return await self.tag_list(ctx)

        tag = tag.lower()
        if tag == "list":
            return await self.tag_list(ctx)

        embed = self.get_tag_embed(ctx.author, tag)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["tags_list"])
    async def tag_list(self, ctx: Context) -> None:
        lines = sorted([f"» `{name}`" for name in self.TAGS])
        paginator = Paginator(ctx, lines, per_page=10, title=f"All tags (`{len(lines)}` total)")
        await paginator.start()

    @commands.command()
    async def zen(self, ctx: Context, search: int = None) -> None:
        embed = disnake.Embed(title="The Zen of Python", description=ZEN_OF_PYTHON)

        if not search:
            return await ctx.reply(embed=embed)

        lines = ZEN_OF_PYTHON.splitlines()
        if len(lines) > search:
            return await ctx.reply(
                embed=disnake.Embed(title=f"The Zen of Python - Line {search}", description=lines[search])
            )

        await ctx.reply(embed=embed.set_footer(text=f"lines {search} is not in the zen lines!"))


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Docs(bot))

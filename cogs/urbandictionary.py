from disnake.ext import commands

from core import Context, JesterBot


class UrbanDictionary(commands.Cog):
    RANDOM_URL = "http://api.urbandictionary.com/v0/random"
    SPECIFIC_URL = "http://api.urbandictionary.com/v0/define?term={}"

    def __init__(self, bot) -> None:
        self.bot = bot

    def parse_dict(self, dictionary: dict) -> str:
        return """```yaml\n{content}```"""

    @commands.command(aliases=["search", "usearch"])
    async def urban_search(self, ctx: Context, *, query: str) -> None:
        async with self.bot.client.get(url=self.SPECIFIC_URL + query) as resp:
            json = await resp.json()
            try:
                output = self.parse_dict(json["list"][0])
            except Exception:
                output = "That doesnt exist in the urban dictionary"

        await ctx.reply(output)

    @commands.command(aliases=["randomsearch", "rsearch"])
    async def random_urban_search(self, ctx: Context) -> None:
        async with self.bot.client.get(url=self.RANDOM_URL) as resp:
            json = await resp.json()
            output = self.parse_dict(json["list"][0])

        await ctx.reply(output)


def setup(bot: JesterBot) -> None:
    bot.add_cog(UrbanDictionary(bot))

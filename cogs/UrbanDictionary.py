import re
import disnake
import aiohttp
from disnake.ext import commands

from core.Context import Context

class UrbanDictionary(commands.Cog): 
    RANDOM_URL = "http://api.urbandictionary.com/v0/random"
    SPECIFIC_URL = "http://api.urbandictionary.com/v0/define?term={}"

    def __init__(self, bot) -> None:
        self.bot = bot

    def parse_dict(self, dictionary: dict) -> str:
        content = f"""
        ++ -- urban search for word {dictionary['word']} -- ++

Definition(s): {dictionary['definition']}

Author: {dictionary['author']}
Upvotes: {dictionary['thumbs_up']}
Downvotes: {dictionary['thumbs_down']}
{"Example: " + dictionary['example'] if dictionary['example'] else ''}

Link: {dictionary['permalink']}"""

        return f"""```yaml\n{content}```"""


    @commands.command(aliases=['search', 'usearch'])
    async def urban_search(
        self, ctx: Context, *, query: str
    ) -> None:
        async with aiohttp.ClientSession() as client:
            async with client.get(url=self.SPECIFIC_URL+query) as resp:
                json = await resp.json()
                try:
                    output = self.parse_dict(json['list'][0]) 
                except:
                    output = "That doesnt exist in the urban dictionary"

        await ctx.send(output)


    @commands.command(aliases=['randomsearch', 'rsearch'])
    async def random_urban_search(
        self, ctx: Context
    ) -> None:
        async with aiohttp.ClientSession() as client:
            async with client.get(url=self.RANDOM_URL) as resp:
                json = await resp.json()
                output = self.parse_dict(json['list'][0])
                
        await ctx.send(output)
    


def setup(bot: commands.Bot) -> None:
    bot.add_cog(UrbanDictionary(bot))
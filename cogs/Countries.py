import re
import discord, aiohttp, pprint
from discord.ext import commands

from core.utils.utils import thebed

class Countries(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def country(self, ctx, *, name):
        name = name.split(' ')
        name = '%20'.join(name)
        async with aiohttp.ClientSession().get(f"https://restcountries.eu/rest/v2/name/{name}") as resp:
            response = await resp.json()
            if 'status' in response:
                return await ctx.expected_error(error='That is not a valid **country** Try searching for full names, include spaces. Not capital-sensitive')
            result = pprint.pformat(response[0])
            result = result.replace("'", "")
            await thebed(ctx, '', result)
    @commands.command()
    async def findcountry(self, ctx, *, name):
        pass
    
    @commands.command()
    async def flag(self, ctx, *, country):
        async with aiohttp.ClientSession().get(f"https://restcountries.eu/rest/v2/name/{country}") as response:
            async with ctx.typing():
                z = response.content
                print(z)
                my_file = open('./images/flag.png', 'wb')
                my_file.write()
                my_file.close()



        await ctx.send(file=discord.File('./images/flag.png')) 
            
            


                                








def setup(bot):
    bot.add_cog(Countries(bot))
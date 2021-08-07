
from discord.errors import HTTPException
import requests
import discord, aiohttp, pprint, json
from discord.ext import commands
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from core.utils.utils import thebed

async def makeimg(ctx, url):
 
    try:
        async with ctx.typing():
            async with aiohttp.ClientSession() as client:
                async with client.get(url) as response:
                    my_file = open('./images/country.svg', 'wb')
                    my_file.write(await response.read())
                    my_file.close()
                    drawing = svg2rlg('./images/country.svg')
                    renderPM.drawToFile(drawing, './images/country.png', fmt='PNG')

        await ctx.send(file=discord.File('./images/country.png'))
        
        return True
    except Exception as e:
        return False


class Countries(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def country(self, ctx, *, name):
        name = name.split(' ')
        name = '%20'.join(name)
        async with aiohttp.ClientSession() as client:
            async with client.get(f"https://restcountries.eu/rest/v2/name/{name}") as resp:
                response = await resp.json()
                if 'status' in response:
                    return await ctx.expected_error(error='That is not a valid **country** Try searching for full names, include spaces. Not capital-sensitive')
                result = pprint.pformat(response[0])
                result = result.replace("'", "")
                await thebed(ctx, '', result)
    @commands.command()
    async def findcountry(self, ctx, *, name):
        y = []
        async with aiohttp.ClientSession() as client:
            async with client.get(f"https://restcountries.eu/rest/v2/all") as resp:
                x = await resp.json()
                for num, k in enumerate(x):
                    if x[num]['name'].lower().startswith(name[:1]):
                        y.append(x[num]['name'])
        await thebed(ctx, 'Countries relating to ' + name, ", ".join(y))
    
    @commands.command()
    async def flag(self, ctx, *, country):
        y = True
        x = await makeimg(ctx, f"https://restcountries.eu/data/{country}.svg")
        if not x:

            try:
                async with aiohttp.ClientSession() as client:
                    async with client.get(f"https://restcountries.eu/rest/v2/name/{country}") as resp:
                        js = await resp.json()
                        y = await makeimg(ctx, f"{js[0]['flag']}")

            except:
                return  await ctx.error(self.bot, error=f" That isnt recognised as a country! Type `j.findcountry {country}` to see all recognised countries basiced off of your search") 
        # async with aiohttp.ClientSession().get(f"https://restcountries.eu/rest/v2/name/{country}") as response:
        #     async with ctx.typing():
        #         pass



        # await ctx.send(file=discord.File('./images/flag.png')) 
            
            


                                








def setup(bot):
    bot.add_cog(Countries(bot))
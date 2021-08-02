import discord
import requests
import json
from core.utils.utils import Color, thecolor
from discord.ext import commands


class Cryptocurrency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ex"])
    async def exchange(self, ctx, amount:int,exchangefrom,exchangeto):
        await ctx.trigger_typing()
        url = "https://fixer-fixer-currency-v1.p.rapidapi.com/convert"

        querystring = {"amount": f"{amount}", "to": f"{exchangeto}", "from": f"{exchangefrom}"}

        headers = {
        'x-rapidapi-key': "1c0ae8ee8emsh7bd54f2151cc278p1a0f3djsn9212745a468e",
        'x-rapidapi-host': "fixer-fixer-currency-v1.p.rapidapi.com"
        }
        
        response = requests.request(
        "GET", url, headers=headers, params=querystring)
        url2 = "https://fixer-fixer-currency-v1.p.rapidapi.com/symbols"

        headers2 = {
            'x-rapidapi-key': "1c0ae8ee8emsh7bd54f2151cc278p1a0f3djsn9212745a468e",
            'x-rapidapi-host': "fixer-fixer-currency-v1.p.rapidapi.com"
        }

        response2 = requests.request("GET", url2, headers=headers2)
        embed = discord.Embed(title=f"Crypto exchange rate",color=thecolor())
        embed.add_field(name=f"exchanged from {exchangefrom} to {exchangeto}", value=response.json()["result"], inline=False)
        
        embed.add_field(name="Rate", value=response.json()["info"]["rate"], inline=False)
        
        data = response2.json()["symbols"]
        if exchangeto in data:
            embed.set_thumbnail(url=f"https://cryptoicons.org/api/icon/{exchangefrom}/200")
        else:
            
            embed.set_thumbnail(url=f"https://cryptoicons.org/api/icon/{exchangeto}/200")
            await ctx.send("https://cryptoicons.org/api/icon/{exchangeto}/200")
        await ctx.send(embed=embed)

    @commands.command(aliases=["Sym"])
    async def Symbols(self, ctx):
        await ctx.trigger_typing()
        url = "https://fixer-fixer-currency-v1.p.rapidapi.com/symbols"

        headers = {
            'x-rapidapi-key': "1c0ae8ee8emsh7bd54f2151cc278p1a0f3djsn9212745a468e",
            'x-rapidapi-host': "fixer-fixer-currency-v1.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers)    
        await ctx.send("2")

def setup(bot):
    bot.add_cog(Cryptocurrency(bot))

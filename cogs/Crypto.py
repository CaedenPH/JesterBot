import disnake
import requests
import json
import yfinance as yf

from core.utils.utils import Color, thecolor, thebed
from core.Context import Context

from disnake.ext import commands


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
        embed = disnake.Embed(title=f"Crypto exchange rate",color=thecolor())
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

    @commands.command(
        aliases=['stock', 'market'],
        description="Sends information about the stocks specified"
        ) 

    async def stocks(self, ctx:Context, stock=None):
        
        if not stock:
            embed = disnake.Embed(title="Type the stock symbol (e.g AAPL = apple)", description="[Stocks](https://swingtradebot.com/equities)", colour=thecolor())
            return await ctx.send(embed=embed)

        tickerData = yf.Ticker(stock)
        inf = tickerData.info
    
        if 'longName' not in inf:
            return await thebed(ctx, '', 'Not enough information')
        async with ctx.typing():
            embed = disnake.Embed(title=f"{inf['longName'] if inf['longName'] else 'No name data'}", colour=thecolor())
            embed.set_author(icon_url=ctx.author.avatar.url, name="Stock market")
            if 'fullTimeEmployees' in inf:
                embed.add_field(name="Employees", value=f"{inf['fullTimeEmployees']}", inline=False)
            if 'dividendRate': 
                embed.add_field(name="Employees", value=f"{inf['dividendRate']}", inline=False)   
            if 'country' in inf:
                embed.add_field(name="Location", value=f"{inf['country']}, {inf['state']}, {inf['city']}", inline=False)
            if 'sharesShort' in inf:
                embed.add_field(name="Shares", value=f"{inf['sharesShort']}", inline=False)
            if 'fiftyTwoWeekLow' in inf:
                embed.add_field(name="Value", value=f"Market Cap: *${inf['marketCap']}*\nLow: *${inf['fiftyTwoWeekLow']}*\nHigh: *${inf['fiftyTwoWeekHigh']}*", inline=False)
            if 'logo_url' in inf:
                embed.set_thumbnail(url=inf['logo_url'])
            
        await ctx.send(embed=embed)                
def setup(bot):
    bot.add_cog(Cryptocurrency(bot))

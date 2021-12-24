import disnake
import aiohttp
import pprint

from disnake.ext import commands
from core.Context import Context

class Random(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(aliases=['kanye'])
    async def kanye_quote(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://api.kanye.rest/") as resp:
            json = await resp.json()

        await ctx.em(f"**Kanye quote:** {json['quote']}")


    @commands.command()
    async def bored(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://www.boredapi.com/api/activity") as resp:
            json = await resp.json()

        await ctx.send(
            f"""yaml
    ++  --  **Are you bored?** -- ++
**Activity:** {json['activity']}
**Type:** {json['tpye']}
**Participants required:** {json['participants']}
**Price:** {json['price']}
{'**Link:**' + json['link'] if json['link'] else ''}
            """
        )
    
    @commands.command()
    async def age(self, ctx: Context, name: str) -> None:
        async with self.bot.client.get(url=f"https://api.agify.io/?name={name}") as resp:
            json = await resp.json()

        await ctx.em(f"The bot thinks you are {json['age']} years old!")    

    @commands.command()
    async def weather(self, ctx: Context, city: str) -> None:
        async with self.bot.client.get(url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.bot.WEATHER_KEY}") as resp:
            json = await resp.json()

        await ctx.send(
            f"""```yaml
    ++ -- Weather info for {city} -- ++
[Temperature:] 
    - temp : {json['main']['temp']}
    - temp_min : {json['main']['temp_min']}
    - temp_max : {json['main']['temp_max']}
[Wind:]
    - speed : {json['wind']['speed']}
    - deg : {json['wind']['deg']}
[Coordinates of dest:] 
    - longitude : {json['coord']['lon']}
    - latitude : {json['coord']['lat']}

[Pressure:] {json['main']['pressure']}
[Humidity:] {json['main']['humidity']}
[Visibility:] {json['visibility']}
[Rain:] {json['rain']['1h']}```
            """
        )

    @commands.command()
    async def spacex(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://api.spacexdata.com/v4/launches/latest") as resp:
            json = await resp.json()

        await ctx.send(
            f"""```yaml
    ++ --  Spacex latest info -- ++
{pprint.pformat(json)}
            ```"""
        )

    @commands.command()
    async def screenshot(self, ctx: Context, *, url):
        await ctx.send(f"https://image.thum.io/get/https://{url}")
        
    @commands.command()
    async def covid(self, ctx: Context, country=None):
        async with self.bot.client.get(url="https://api.spacexdata.com/v4/launches/latest") as resp:
            json = await resp.json()
            print(json)

        if country is None:...

            
            
    
        
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Random(bot))
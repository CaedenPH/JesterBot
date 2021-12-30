import os
import pprint
import random
import json
import disnake
from disnake.interactions.application_command import CmdInter
import yaml

from disnake.ext import commands
from core.Context import Context
from pathlib import Path


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
        async with self.bot.client.get(url="https://www.boredapi.com/api/activity", verify_ssl=False) as resp:
            json = await resp.json()

        await ctx.em(
            f"""```yaml
    ++  --  Are you bored? -- ++
[Activity:] {json['activity']}
[Type:] {json['type']}
[Participants required:] {json['participants']}
[Price:] {json['price']}
{'[Link:]' + json['link'] if json['link'] else ''}```
            """
        )
    
    @commands.command()
    async def age(self, ctx: Context, name: str) -> None:
        async with self.bot.client.get(url=f"https://api.agify.io/?name={name}") as resp:
            json = await resp.json()

        await ctx.em(f"The bot thinks you are {json['age']} years old!")    

    @commands.command()
    async def weather(self, ctx: Context, *, city: str) -> None:
        async with self.bot.client.get(url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.bot.WEATHER_KEY}") as resp:
            json = await resp.json()

        await ctx.em(
            f"""```yaml
    ++ -- Weather info for {city} -- ++
[Temperature:] 
    - temp : {json['main']['temp']}
    - temp_min : {json['main']['temp_min']}
    - temp_max : {json['main']['temp_max']}
[Wind:]
    - speed : {json['wind']['speed']}
    - deg : {json['wind']['deg']}
[Dest Coords:] 
    - longitude : {json['coord']['lon']}
    - latitude : {json['coord']['lat']}

[Pressure:] {json['main']['pressure']}
[Humidity:] {json['main']['humidity']}
[Visibility:] {json['visibility']}```
            """
        )

    @commands.command()
    async def spacex(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://api.spacexdata.com/v4/launches/latest", verify_ssl=False) as resp:
            json = await resp.json()

        await ctx.em(
            f"""```yaml
          ++ --  Spacex latest info -- ++
{pprint.pformat(json)}```"""
        )

    @commands.command()
    async def screenshot(self, ctx: Context, *, url):
        await ctx.send(f"https://image.thum.io/get/https://{url}")
        
    @commands.command()
    async def coffee(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://coffee.alexflipnote.dev/random.json") as resp:
            json = await resp.json()
        
        await ctx.send(json['file'])

    @commands.command()
    async def geek(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://geek-jokes.sameerkumar.website/api") as resp:
            json = await resp.json()

        await ctx.em(f"""```yaml
{json}```""")

    @commands.command()
    async def blank(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://chew.pw/api/trbmb") as resp:
            json = await resp.json()

        await ctx.em(f"```yaml\n{json[0]}```")

    @commands.command()
    async def bs(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://corporatebs-generator.sameerkumar.website/") as resp:
            json = await resp.json()

        await ctx.em(f"```yaml\n[BS corporate phase:] {json['phrase']}```")

    @commands.command()
    async def trump(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://api.whatdoestrumpthink.com/api/v1/quotes") as resp:
            json = await resp.json()

        await ctx.em(f"""```yaml
[Trump quote:] {random.choice(json['messages']['personalized'])}```
        """)

    @commands.command(name="fool")
    async def april_fools(self, ctx: Context) -> None:
        video = random.choice(json.loads(Path("./resources/seasonal/april_fools_videos.json").read_text("utf-8")))
        channel, url = video["channel"], video["url"]

        await ctx.send(f"Check out this April Fools' video by {channel}.\n\n{url}")

    @commands.command()
    async def topic(self, ctx: Context) -> None:
        with open("./resources/topic.yaml") as stream:
            out = yaml.load(stream, Loader=yaml.Loader) 
        await ctx.em(random.choice(out))

    @commands.command()
    async def date(self, ctx: Context) -> None:
        with open("./resources/seasonal/date_ideas.json", encoding="utf-8") as stream:
            data = json.load(stream)

        choice = random.choice(data['ideas'])
        embed = disnake.Embed(
            title=choice['name'],
            description=choice['description']
        ).set_author(
            name=ctx.author.name + "s' date",
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def planet(self, ctx: Context) -> None:
        with open("./resources/save_the_planet.json") as stream:
            data = json.load(stream)
        
        choice = random.choice(data)
        embed = disnake.Embed.from_dict(
            choice
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['colour'])
    async def color(self, ctx: Context) -> None:
        with open("./resources/colors.json") as stream:
            data = json.load(stream)
        x = list(data.items())
        hexcolor = random.choice(x)

        async with ctx.typing():
            async with self.bot.client.get(f"https://some-random-api.ml/canvas/colorviewer?hex={hexcolor[1]}") as response:
                file = open('./images/color.png', 'wb')
                file.write(await response.read())
                file.close()

        file = disnake.File(
            "./images/color.png", 
            filename="color.png"
        )
        embed = disnake.Embed(
            title="Random color",
            description="`Color name: {0[0]} - Hex color: {0[1]}`".format(hexcolor)
        ).set_footer(
            text=f"Out of {len(x)} colors!"
        ).set_image(
            url="attachment://color.png"
        )
        await ctx.send(embed = embed, file=file) 

    @commands.command()
    async def palette(self, ctx: Context) -> None:
        async with self.bot.client.get(url="https://palett.es/API/v1/palette", verify_ssl=False) as resp:
            json = await resp.json()

        await ctx.em(f"Your palette is `{', '.join(json)}`")

    @commands.command()
    async def snake(self, ctx: Context) -> None:
        with open('./resources/snake/snake_facts.json', encoding='utf-8') as stream:
            data = json.load(stream)

        choice = random.choice(data)
        await ctx.em(f"Snake fact: {choice['fact']}")
    
    @commands.command()
    async def snake_name(self, ctx: Context):
        with open('./resources/snake/snake_names.json', encoding='utf-8') as stream:
            data = json.load(stream)

        choice = random.choice(data)
        await ctx.em(f"Snake name: `{choice['name']}` || Scientific: `{choice['scientific']}`") 

    @commands.command(aliases=['star'])
    async def celebrity(self, ctx: Context):
        with open('./resources/celebrities.json', encoding='utf-8') as stream:
            data = json.load(stream)

        choice = random.choice(data)
        await ctx.em(f"Random celebrity: `{choice}`")
    
    @commands.command()
    async def food(self, ctx: Context):
        with open('./resources/foods.json', encoding='utf-8') as stream:
            data = json.load(stream)

        choice = random.choice(data)
        await ctx.em(f"Random food: `{choice}`")






def setup(bot: commands.Bot) -> None:
    bot.add_cog(Random(bot))
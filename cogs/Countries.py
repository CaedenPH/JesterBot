from disnake.errors import HTTPException
import requests
import disnake, aiohttp, pprint, json
from disnake.ext import commands
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from core.utils.utils import thebed


async def makeimg(ctx, url):
    try:
        async with ctx.typing():
            async with ctx.bot.client.get(url) as response:
                my_file = open("./images/country.svg", "wb")
                my_file.write(await response.read())
                my_file.close()
                drawing = svg2rlg("./images/country.svg")
                renderPM.drawToFile(drawing, "./images/country.png", fmt="PNG")
        await ctx.send(file=disnake.File("./images/country.png"))

        return True
    except Exception as e:
        return False


class Countries(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def country(self, ctx, *, name):
        name = name.split(" ")
        name = "%20".join(name)
        async with self.bot.client.get(
            f"https://restcountries.com/v3.1/name/{name}"
        ) as resp:
            response = await resp.json()
            if "status" in response:
                return await ctx.expected_error(
                    error="That is not a valid **country** Try searching for full names, include spaces. Not capital-sensitive"
                )
            result = pprint.pformat(response[0])
            result = result.replace("'", "")
            await thebed(ctx, "", result)

    @commands.command()
    async def findcountry(self, ctx, *, name):
        y = []
        async with self.bot.client.get(f"https://restcountries.eu/rest/v2/all") as resp:
            x = await resp.json()
            for num, k in enumerate(x):
                if x[num]["name"].lower().startswith(name[:1]):
                    y.append(x[num]["name"])
        await thebed(ctx, "Countries relating to " + name, ", ".join(y))

    @commands.command()
    async def flag(self, ctx, *, country):
        y = True
        x = await makeimg(ctx, f"https://restcountries.eu/data/{country}.svg")
        if not x:
            async with self.bot.client.get(
                f"https://restcountries.eu/rest/v2/name/{country}"
            ) as resp:
                js = await resp.json()
                y = await makeimg(ctx, f"{js[0]['flag']}")

    @commands.command(aliases=["ewh"])
    async def endworldhunger(self, ctx):
        embed = disnake.Embed(
            title="How to end world hunger",
            description="What are the ways to stop world hunger? Work tirelessly for an international organization? [Donate](https://borgenproject.org/donate/) old clothes and toys to our local Salvation Army? Or is it even possible? There are hundreds of theories on how we can end world hunger and activists debate many of them. Some have been effective and others not. One thing is certain, and that is that we must do something. Discussed below are 10 effective world hunger solutions.",
            color=0xFF0000,
        )
        embed.add_field(
            name="1. Sustainable Food",
            value="> Heifer International is an organization that helps transform agriculture. They fund projects so people can provide food for themselves in a sustainable way. This is very powerful, because ultimately we would like to see many impoverished areas not reliant on aid from foreign countries (which often causes debt) and able to create their own, steady, supply of food.",
            inline=False,
        )
        embed.add_field(
            name="2. Access to Credit",
            value="> Many organizations are helping people in poor countries to gain access to credit. Most of these credit loans are repaid, and they have created many industries, such as farms, that help create a sustainable provision for people and also develop nations economically. If these people do not have access to credit, they cannot start up industries that combat poverty.",
            inline=False,
        )
        embed.add_field(
            name="3. Food Donations",
            value="> Although ideally it would be better to get the entire world to a place of self-sustainability, it is not something that will happen overnight. In the meantime it is important to lend a helping hand. The impact of donations, both cash and food, have had an immense impact on world hunger. Organizations such as Food for All have customers donate $1-5 when checking out. Last year they raised a whopping $60 million to fight world hunger.",
            inline=False,
        )
        embed.add_field(
            name="4. Transitioning",
            value="> Many families dealing with poverty need help transitioning into a state of self-dependance. 15 Feeds Family is an organization that helps with this transition. They start by providing families with food, but then slowly find [solutions](https://borgenproject.org/innovative-solutions-to-poverty-and-hunger/) to empower families to be self-sufficient. This is important, because self-sufficiency allows for a certain food income, when relying on donations does not always guarantee food.",
            inline=False,
        )
        embed.add_field(
            name="5. Urban Farming",
            value="> Almost one-quarter of undernourished people live in an urban environment. Recently, there has been a big push for urban farming. Urban farming empowers families to gain control over their own food source.",
            inline=False,
        )
        embed.add_field(
            name="6. Access to Education",
            value="> Education is the best weapon against poverty and hunger. It is especially powerful in underdeveloped countries. Education means better opportunity and more access to income and food. Additionally, some countries have food-for-education programs where students are given free food for coming to school. This may seem like a basic idea in the United States, but it is life saving in many under developed nations.",
            inline=False,
        )
        embed.add_field(
            name="7. Social Change",
            value="> This is extremely hard and will not take place overnight. However, many social issues, such as war, pose a fundamental problem to halting world hunger. Ideally, this will happen when world powers, such as the United States and many western European nations, choose to focus on solving these issues instead of exacerbating them. However, this can only start when people in developed nations begin to care about those issues as well and pressure their governments to be productive in ending conflict.",
            inline=False,
        )
        embed.add_field(
            name="8. Government Intervention",
            value="> Aid to foreign nations needs to be more focused on government intervention, like programs that provide food to mothers and their children in poor areas. This is not much different from many programs available in the United States.",
            inline=False,
        )
        embed.add_field(
            name="9. Empowering Women",
            value="> There is a direct correlation with hunger and gender inequalities. Empowering women to gain access to food, be providers, and lead their families has had a major impact on food access and ability to change financial situations.",
            inline=False,
        )
        embed.add_field(
            name="10. Birth Control Education",
            value="> High birthrates pose a problem when trying to solve hunger. Many people are not educated on reproduction or do not have access to contraceptives. Gaining access to contraceptives allows for family planning and economic freedom",
            inline=False,
        )
        embed.add_field(
            name="Sources",
            value=":= |[WTP](http://www.wfp.org/stories/10-ways-feed-world) |[Millions of mouths](http://millionsofmouths.com/blog/2006/08/23/the-method-to-end-hunger/) |[huffington post](http://www.huffingtonpost.com/2011/06/15/seven-ways-to-solver-hung_n_872894.html)| =:",
        )
        embed.set_image(
            url="https://food.tomra.com/hubfs/Food%20for%20thought/2018/Q3/WFD18/EN_WebBanner.jpg"
        )

        embed.set_author(
            name="Hunger is not an issue of charity. It is an issue of justice. -Jacques Diouf",
            url="https://en.wikipedia.org/wiki/Jacques_Diouf ",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/2/2a/Jacques_Diouf.jpg",
        )
        embed.set_thumbnail(
            url="https://w7.pngwing.com/pngs/667/592/png-transparent-world-health-organization-united-nations-global-health-world-health-organization-logo-world-world-map.png"
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Countries(bot))

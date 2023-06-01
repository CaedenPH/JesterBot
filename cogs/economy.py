import asyncio
import json
from random import choice, randint

import disnake
from disnake.ext import commands

from core import Context
from core.utils import get_colour, send_embed, update_json

FALSCH = False


class Economy(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    async def cog_after_invoke(self, ctx: Context):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if str(ctx.author.id) not in data:
                data[str(ctx.author.id)] = {"Bal": 1, "Name": ctx.author.name}
            else:
                x = randint(1, 10)
                data[str(ctx.author.id)]["Bal"] += x
            update_json(k, data)

    @commands.group(
        aliases=["buy"],
        description="If `purchase` is empty, sends what can be bought, or if [`purchase`] is a purchasable you buy the item",
        invoke_without_command=True,
    )
    async def shop(self, ctx: Context, purchase=""):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if purchase is None:
                embed = disnake.Embed(colour=get_colour())
                embed.set_author(icon_url=ctx.author.display_avatar.url, name="Shop")
                embed.add_field(
                    name="\u200b",
                    value="""
                **What you can purchase...**

                - Custom role (`j.buy role`), you choose the name and colour! - `3000$.`
                - Lucky box! (`j.buy box`), you can buy and open a lucky box that can contain up to 300$! - `200$`
                - A gun (`j.buy gun`), you can use a gun to steal a huge chunk of someones money! - `2000$`
                - A bag (`j.buy bag`), the ability to rob someone for a small/medium ammount of money - `500$`
                - A portable corona virus (`j.buy corona`), gives someone covid for 5 hours - meaning that work is disabled - `300$`

                **How to get money?**
                Everytime you run a command you get money, and there are also other commands you can run to get money;
                    : `gamble`
                    : `beg`
                    : `work`
                    : every time you run an economy command you also get from `1-10`$

                Your balance is: **{data[str(ctx.author.id)]['Bal']}$**""",
                )
                await ctx.reply(embed=embed)

    @shop.command()
    async def role(self, ctx: Context):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if data[str(ctx.author.id)]["Bal"] > 1000:
                try:

                    embed1 = disnake.Embed(
                        description="What would you like the name of your role to be",
                        colour=get_colour(),
                    )
                    embed1.set_author(
                        name=ctx.author.name, icon_url=ctx.author.display_avatar.url
                    )
                    await ctx.reply(embed=embed1)
                    msg = str(
                        (
                            await self.bot.wait_for(
                                "message",
                                check=lambda m: m.author == ctx.author
                                and m.channel == ctx.channel,
                                timeout=60.0,
                            )
                        ).content
                    ).lower()
                    embed1 = disnake.Embed(
                        description="What would you like the colour of your role to be? [Refer to this](https://www.colour-hex.com/) \nAdd 0x infront of the colour, e.g 0x4b46cd",
                        colour=get_colour(),
                    )
                    embed1.set_author(
                        name=ctx.author.name, icon_url=ctx.author.display_avatar.url
                    )
                    await ctx.reply(embed=embed1)
                    msg1 = str(
                        (
                            await self.bot.wait_for(
                                "message",
                                check=lambda m: m.author == ctx.author
                                and m.channel == ctx.channel,
                                timeout=60.0,
                            )
                        ).content
                    ).lower()

                    role = await ctx.guild.create_role(name=msg, colour=int(msg1, 16))

                    await ctx.author.add_roles(role)

                    embed1 = disnake.Embed(title="Created!", colour=get_colour())
                    embed1.set_author(
                        name=ctx.author.name, icon_url=ctx.author.display_avatar.url
                    )
                    await ctx.reply(embed=embed1)
                    data[str(ctx.author.id)]["Bal"] -= 1000
                    update_json(k, data)
                except asyncio.TimeoutError:
                    embed = disnake.Embed(title="I gave up waiting", colour=get_colour())
                    await ctx.reply(embed=embed)
            else:
                embed = disnake.Embed(
                    title="You dont have enough money!", colour=get_colour()
                )
                await ctx.reply(embed=embed)

    @shop.command()
    async def box(ctx):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if str(ctx.author.id) in data:

                if data[str(ctx.author.id)]["Bal"] >= 150:

                    data[str(ctx.author.id)]["Bal"] -= 150
                    if "Box" in data[str(ctx.author.id)]:

                        data[str(ctx.author.id)]["Box"] += 1
                    else:
                        data[str(ctx.author.id)]["Box"] = 1

                    update_json(k, data)
                    embed = disnake.Embed(
                        description="You bought a **lucky box**, to use it write `j.open box`",
                        colour=get_colour(),
                    )
                    await ctx.reply(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="You dont have enough money!", colour=get_colour()
                    )
                    await ctx.reply(embed=embed)

            else:
                embed = disnake.Embed(
                    title="You dont have enough money!", colour=get_colour()
                )
                await ctx.reply(embed=embed)

    @shop.command()
    async def gun(ctx):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            i = str(ctx.author.id)
            if i in data and data[i]["Bal"] >= 2000:
                data[i]["Bal"] -= 2000
                if "Gun" in data[i]:

                    data[i]["Gun"] += 1
                else:
                    data[i]["Gun"] = 1
                await send_embed(
                    ctx,
                    "Success",
                    "you have purchased your **gun**, but be careful! To use it type `j.use gun`",
                )
                update_json(k, data)
            else:
                await send_embed(ctx, "You don't have enough money!")

    @shop.command()
    async def bag(ctx):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            i = str(ctx.author.id)
            if i in data and data[i]["Bal"] >= 500:
                data[i]["Bal"] -= 500
                if "Bag" in data[i]:
                    data[i]["Bag"] += 1
                else:
                    data[i]["Bag"] = 1
                await send_embed(
                    ctx,
                    "Success",
                    "you have purchased your **bag**, to use it type `j.use bag`",
                )
                update_json(k, data)
            else:
                await send_embed(ctx, "You don't have enough money!")

    @shop.command(alises=["covid", "cov"])
    async def corona(self, ctx: Context):
        with open("./dicts/Bal.json", "r+") as k:
            with open("./dicts/Bal.json", "r+") as k:
                data = json.load(k)
                i = str(ctx.author.id)
                if i in data and data[i]["Bal"] >= 300:
                    data[i]["Bal"] -= 300
                    if "covid" in data[i]:

                        data[i]["covid"] += 1
                    else:
                        data[i]["covid"] = 1
                    await send_embed(
                        ctx,
                        "Success",
                        "you have purchased your portable covid, to use it type `j.use corona`",
                    )
                    update_json(k, data)
                else:
                    await send_embed(ctx, "You don't have enough money!")

    @commands.command(
        aliases=["bal", "money"],
        description="Sends the JesterCoins `[user] has, if no user specified it sends authors bal",
    )
    async def balance(self, ctx: Context, user: disnake.Member = None):
        with open("./dicts/Bal.json") as k:
            data = json.load(k)

            if user is None:
                if str(ctx.author.id) in data:
                    embed = disnake.Embed(
                        description=f"**{data[str(ctx.author.id)]['Bal']}** JesterCoins",
                        colour=get_colour(),
                    )
                    embed.set_footer(
                        text="Every time you run an economy command you get money!"
                    )
                    embed.set_author(
                        icon_url=ctx.author.display_avatar.url, name="Balance"
                    )
                else:
                    embed = disnake.Embed(description="You have 0$", colour=get_colour())
                    embed.set_author(
                        icon_url=ctx.author.display_avatar.url, name="Balance"
                    )

            else:
                if str(user.id) in data:
                    embed = disnake.Embed(
                        description=f"{data[str(user.id)]['Bal']}$", colour=get_colour()
                    )
                else:
                    embed = disnake.Embed(
                        description="They have 0$", colour=get_colour()
                    )

        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["bet", "g"],
        description="Gambles the `<ammount>`, 1 in 3 chance to double money, 2 in 3 chance to lose the money you gambled...",
    )
    async def gamble(self, ctx: Context, money: int):
        if money <= 25:
            return await send_embed(ctx, "", "You must bet over **25** jestercoins!")
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if str(ctx.author.id) in data:

                if money <= data[str(ctx.author.id)]["Bal"]:
                    x = randint(1, 3)
                    if x == 1:

                        embed = disnake.Embed(
                            description=f"you gambled **{money}$** and got **{money * 2}$**",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            icon_url=ctx.author.display_avatar.url, name="You won!"
                        )
                        data[str(ctx.author.id)]["Bal"] += money * 2
                        update_json(k, data)
                    else:
                        embed = disnake.Embed(
                            description=f"you gambled **{money}$** and lost **{money}$**",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            icon_url=ctx.author.display_avatar.url, name="You lost!"
                        )
                        data[str(ctx.author.id)]["Bal"] -= money
                        update_json(k, data)
                else:
                    embed = disnake.Embed(
                        description="You do not have enough money! type `j.bal` to see your balance",
                        colour=get_colour(),
                    )
            else:
                embed = disnake.Embed(
                    title="You do not have enough money! type `j.bal` to see your balance",
                    colour=get_colour(),
                )

            await ctx.reply(embed=embed)

    @commands.command(
        description="You get a random ammount of JesterCoins - 60 second cooldown!"
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx: Context):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            x = randint(50, 200)
            data[str(ctx.author.id)]["Bal"] += x
            embed = disnake.Embed(
                description=f"You begged and got **{x}** jestercoins!",
                colour=get_colour(),
            )
            await ctx.reply(embed=embed)
            update_json(k, data)

    @commands.command(aliases=["balancetop"], description="Sends the richest members")
    async def baltop(self, ctx: Context):
        x1 = 0
        x = []
        y = "\n"
        with open("./dicts/Bal.json") as k:
            embed = disnake.Embed(colour=get_colour())
            embed.set_author(name="Baltop", icon_url=ctx.author.display_avatar.url)
            data = json.load(k)

            def get_key(item):
                return item[1]["Bal"]

            sorted_scores = sorted(data.items(), key=get_key, reverse=True)[:10]

            for item in sorted_scores:
                for datas in data:

                    if item[0] in datas:
                        x1 += 1
                        name = data[datas]["Name"]
                x.append(f"**__{x1}. {name}__:**\n JesterCoins: {item[1]['Bal']}$")

            embed.add_field(name="\u200b", value=f"{y.join(x)}", inline=False)

            await ctx.reply(embed=embed)

    @commands.command(
        aliases=["give"], description="Sends the <ammount> from your bank to their bank!"
    )
    async def gift(self, ctx: Context, user: disnake.Member, ammount: int):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if data[str(ctx.author.id)]["Bal"] >= ammount:

                if str(user.id) in data:
                    data[str(user.id)]["Bal"] += ammount

                    data[str(ctx.author.id)]["Bal"] -= ammount
                    update_json(k, data)
                    embed = disnake.Embed(
                        description=f"You sent to **{ammount}$** to {user.name}!",
                        colour=get_colour(),
                    )
                else:
                    data[str(user.id)] = {"Bal": ammount, "Name": user.name}
                    data[str(ctx.author.id)]["Bal"] -= ammount
                    update_json(k, data)
                    embed = disnake.Embed(
                        description=f"You sent to **{ammount}$** to {user.name}!",
                        colour=get_colour(),
                    )
            else:
                embed = disnake.Embed(
                    description=f"You don't have {ammount}! Type `j.bal` for your balance!",
                    colour=get_colour(),
                )
            await ctx.reply(embed=embed)

    @commands.command(
        aliases=["givehide"],
        description="Sends the <ammount> from your bank to their bank!",
        hidden=True,
    )
    async def gifthide(self, ctx: Context, user: int, ammount: int):

        user = self.bot.get_user(user)

        if user:
            with open("./dicts/Bal.json", "r+") as k:
                data = json.load(k)
                if data[str(ctx.author.id)]["Bal"] >= ammount:

                    if str(user.id) in data:
                        data[str(user.id)]["Bal"] += ammount
                        update_json(k, data)

                        embed = disnake.Embed(
                            description=f"You sent to {ammount}$ to {user.name}!",
                            colour=get_colour(),
                        )
                    else:
                        data[str(user.id)] = {"Bal": ammount, "Name": user.name}

                        update_json(k, data)
                        embed = disnake.Embed(
                            description=f"You sent to {ammount}$ to {user.name}!",
                            colour=get_colour(),
                        )
                else:
                    embed = disnake.Embed(
                        description=f"You don't have {ammount}! Type `j.bal` for your balance!",
                        colour=get_colour(),
                    )
                await ctx.reply(embed=embed)
        else:
            await ctx.reply("no")

    @commands.group(
        aliases=["open", "use"],
        description="unlocks your Lucky boxes!",
        invoke_without_command=True,
    )
    async def unlock(self, ctx: Context, what=""):
        await send_embed(
            ctx,
            "",
            "Type what you want to open! Type `j.inv` to see what you have available to unlock! To buy unlockable items type `j.shop`",
        )

    @unlock.group()
    async def box(self, ctx: Context):
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                if data[str(ctx.author.id)]["Box"] >= 1:
                    rand_prize = randint(200, 300)
                    data[str(ctx.author.id)]["Box"] -= 1
                    data[str(ctx.author.id)]["Bal"] += rand_prize
                    update_json(k, data)
                    embed = disnake.Embed(
                        description=f"You got **{rand_prize}**$!", colour=get_colour()
                    )
                    await ctx.reply(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="You dont have a lucky box! Type `j.shop box` to buy one!",
                        colour=get_colour(),
                    )
                    await ctx.reply(embed=embed)
            else:
                embed = disnake.Embed(
                    title="You dont have a lucky box! Type `j.shop box` to buy one!",
                    colour=get_colour(),
                )
                await ctx.reply(embed=embed)

    @unlock.group()
    async def bag(self, ctx: Context, user: disnake.Member = None):
        if not user and user != ctx.author:
            return await send_embed(ctx, "You need to mention someone to rob!")
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                if "Bag" in data[str(ctx.author.id)]:
                    if data[str(ctx.author.id)]["Bag"] >= 1:
                        data[str(ctx.author.id)]["Bag"] -= 1
                        if str(user.id) in data and data[str(user.id)]["Bal"] >= 100:
                            ran = randint(100, data[str(user.id)]["Bal"])

                            data[str(ctx.author.id)]["Bal"] += ran
                            data[str(user.id)]["Bal"] -= ran
                            update_json(k, data)
                            embed = disnake.Embed(
                                description=f"You robbed **{ran}**$!", colour=get_colour()
                            )
                            await ctx.reply(embed=embed)

                        else:
                            await send_embed(ctx, "They dont have enough in their bank!")

                    else:
                        embed = disnake.Embed(
                            title="You dont have a bag! Type `j.shop bag` to buy one!",
                            colour=get_colour(),
                        )
                        await ctx.reply(embed=embed)

                else:
                    embed = disnake.Embed(
                        title="You dont have a bag! Type `j.shop bag` to buy one!",
                        colour=get_colour(),
                    )
                    await ctx.reply(embed=embed)
            else:
                embed = disnake.Embed(
                    title="You dont have a bag! Type `j.shop bag` to buy one!",
                    colour=get_colour(),
                )
                await ctx.reply(embed=embed)

    @unlock.group()
    async def gun(self, ctx: Context, user: disnake.Member = None):
        if not user and user != ctx.author:
            await send_embed(ctx, "You need to mention someone to rob!")
        with open("./dicts/Bal.json", "r+") as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                if data[str(ctx.author.id)]["gun"] >= 1:
                    data[str(ctx.author.id)]["gun"] -= 1
                    if str(user.id) in data and data[str(user.id)]["Bal"] >= 300:
                        ran = randint(300, data[str(user.id)]["Bal"])

                        data[str(ctx.author.id)]["Bal"] += ran
                        data[str(user.id)]["Bal"] -= ran
                        update_json(k, data)
                        embed = disnake.Embed(
                            description=f"You robbed **{ran}**$!", colour=get_colour()
                        )
                        await ctx.reply(embed=embed)

                    else:
                        await send_embed(ctx, "They dont have enough in their bank!")

                else:
                    embed = disnake.Embed(
                        title="You dont have a gun! Type `j.shop gun` to buy one!",
                        colour=get_colour(),
                    )
                    await ctx.reply(embed=embed)
            else:
                embed = disnake.Embed(
                    title="You dont have a gun! Type `j.shop gun` to buy one!",
                    colour=get_colour(),
                )
                await ctx.reply(embed=embed)

    @commands.command(aliases=["inv"], description="Sends your current inventory")
    async def inventory(self, ctx: Context):
        with open("./dicts/Bal.json") as k:
            embed = disnake.Embed(
                title="Your inventory is currently:", colour=get_colour()
            )

            data = json.load(k)
            if str(ctx.author.id) in data:
                for b in data[str(ctx.author.id)]:
                    if b != "Name":

                        embed.add_field(
                            name=f"{b}",
                            value=f"{data[str(ctx.author.id)][b]}",
                            inline=False,
                        )

                await ctx.reply(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Your inv is empty currently!", colour=get_colour()
                )
                await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, ctx: Context):
        with open("./dicts/Bal.json", "r+") as k:

            data = json.load(k)
            if FALSCH:
                return await send_embed(ctx, "", "You cannot work! You have got covid")
            mon = data[str(ctx.author.id)]["Bal"]
            x = randint(250, 750)
            mon += x
            l = [
                "maid",
                "prostitute",
                "taxi driver",
                "cleaner",
                "trash cleaner",
                "coder",
                "programmer",
                "truck driver",
                "shop keeper",
                "alchoholic (the government was handing out free money)",
                "farmer",
                "blacksmith",
                "artist",
                "product tester",
                "designer",
                "architect",
                "teacher",
                "lawyer",
                "soldier",
                "police officer",
                "plumber",
                "handyman",
                "psychiatrist",
                "therapist",
                "athlete",
                "wrestler",
                "sales managment",
                "fisherman",
                "lumberjack",
                "insurance provider",
                "doctor",
                "nurse",
                "actuary",
                "barrister",
                "scientist",
                "curator",
                "herbalist",
                "broker",
                "banker",
                "journalist",
                "analyst",
                "it consultant",
                "museum guide tour",
                "miner",
                "pharmacist",
                "musician",
                "librarian",
                "site manager",
                "trader",
                "translator",
            ]
            v = ""
            e = choice(l)
            if e[:1] in ["a", "e", "i", "u", "o"]:
                v = f"an {e}"
            else:
                v = f"a {e}"

            update_json(k, data)
            await send_embed(
                ctx,
                "Work",
                """


            You just made `{x}` JesterCoins from working as {v}

            """,
            )


def setup(bot):
    bot.add_cog(Economy(bot))

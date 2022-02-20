import disnake
import json
import asyncio

from disnake.ext import commands
from core.utils import get_colour, update_json, send_embed
from core import Context


class GetUser:
    def __init__(self, file, user="", family=""):

        thefile = open(f"./dicts/{file}", "r+")
        thedata = json.load(thefile)
        if user in thedata:
            theuser = user
            thefamily = thedata[str(user)][family]
        else:
            theuser = False
            thefamily = False

        self.file = thefile
        self.data = thedata
        self.theuser = theuser
        self.family = thefamily
        self.append = update_json(thefile, thedata)

    def user(self, user=""):

        if user in self.data:
            theuser = self.data[str(user)]

        else:
            theuser = user

        self.user = theuser


class Love(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command(help="Pokes the `<member>` specified")
    async def poke(self, ctx: Context, member: disnake.Member = ""):

        if member == "":
            embed = disnake.Embed(
                description=f"**{ctx.author.name}** has poked you 😗",
                colour=get_colour(),
            )
            await ctx.author.send(embed=embed)
            embed = disnake.Embed(
                description=f"The **poke** will be sent to the specified member in aprox **{round(self.bot.latency * 1000)}**ms",
                colour=get_colour(),
            )
            await ctx.reply(embed=embed)
        else:
            embed = disnake.Embed(
                description=f"**{ctx.author.name}** has poked you 😗",
                colour=get_colour(),
            )
            await member.send(embed=embed)
            embed = disnake.Embed(
                description=f"The **poke** will be sent to the specified member in aprox **{round(self.bot.latency * 1000)}** ms",
                colour=get_colour(),
            )
            await ctx.reply(embed=embed)

    @commands.command(help="Sends a hug to the `<member>` specified")
    async def hug(self, ctx: Context, member: disnake.Member = ""):
        if member == "":

            embed = disnake.Embed(
                description=f"**{ctx.author.name}** has given you the gift of a hug 🌷",
                colour=get_colour(),
            )
            await ctx.author.send(embed=embed)
            embed = disnake.Embed(
                description=f"The **hug** will be sent to the specified member in aprox **{round(self.bot.latency * 1000)}**ms",
                colour=get_colour(),
            )
            await ctx.reply(embed=embed)
        else:

            embed = disnake.Embed(
                description=f"**{ctx.author.name}** has given you the gift of a hug 🌷",
                colour=get_colour(),
            )
            await member.send(embed=embed)
            embed = disnake.Embed(
                description=f"The **hug** will be sent to the specified member in aprox **{round(self.bot.latency * 1000)}**ms",
                colour=get_colour(),
            )
            await ctx.reply(embed=embed)

    @commands.command()
    async def love(self, ctx: Context):
        await send_embed(ctx, "Name 1")
        received_msg = str(
            (
                await self.bot.wait_for(
                    "message",
                    timeout=60.0,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                )
            ).content
        ).lower()
        await send_embed(ctx, "Name 2?")
        received_msg1 = str(
            (
                await self.bot.wait_for(
                    "message",
                    timeout=60.0,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                )
            ).content
        ).lower()
        try:
            x = int(received_msg)
            z = int(received_msg1)
            await send_embed(ctx, "That isnt a name...")
        except:
            first_letter1 = received_msg[:1]
            last_letter1 = received_msg[-1:]
            first_letter2 = received_msg1[:1]
            last_letter2 = received_msg1[-1:]
            result1 = (ord(first_letter1)) - 85
            result2 = (ord(last_letter1)) - 85
            result3 = (ord(first_letter2)) - 85
            result4 = (ord(last_letter2)) - 85

            over = result1 + result2
            over1 = result3 + result4

            over2 = over + over1

            for k in ("e", "l", "i", "s", "a"):
                if k in received_msg:
                    over2 += 3
                if k in received_msg1:
                    over2 += 3

            if over2 > 100:
                over2 -= 71

            await send_embed(
                ctx,
                f"Compatabiliy between {received_msg} and {received_msg1}",
                f"**Percentage:** {over2}%",
            )

    @commands.command(aliases=["marrage"])
    async def family(self, ctx: Context):
        File = GetUser("Love.json", f"{str(ctx.author.id)}", "marriage")
        if File.family:

            embed = disnake.Embed(
                title="👨 Family 👩",
                description=f"**{ctx.author.name}** x **{File.family}** \n They have been married since {File.data[str(ctx.author.id)]['since']}",
                colour=get_colour(),
            )
            embed.set_footer(text="\nMay ever hapiness bless them")
            await ctx.reply(embed=embed)
        else:
            await send_embed(ctx, "Marriage", "You are single bro...")

    @commands.command()
    async def marry(self, ctx: Context, member: disnake.Member):
        if member == ctx.author:
            return await send_embed(ctx, "You cannot marry yourself...")
        embed = disnake.Embed(
            title="🎉 Marriage 🎉",
            description=f"**{member.name}** do you accept **{ctx.author.name}** to be your partner? React with this message if you want to get married",
            colour=get_colour(),
        )
        msg = await ctx.reply(embed=embed)
        await msg.add_reaction("💖")
        partner = member
        try:
            emoji, user = await self.bot.wait_for(
                "reaction_add",
                timeout=300.0,
                check=lambda e, u: u == member and e.message.id == msg.id,
            )
            File = GetUser("Love.json")

            if str(ctx.author.id) in File.data:
                arr = File.data[str(ctx.author.id)]["id"]
                del File.data[str(arr)]
                us = self.bot.get_user(int(arr))
                await us.send(f"You got divorced from {ctx.author.name} and they married {member.name}!")
                File.data[str(ctx.author.id)]["marriage"] = partner.name
                File.data[str(member.id)]["id"] = str(partner.id)
                File.data[str(ctx.author.id)]["since"] = str(ctx.message.created_at)

            else:
                File.data[str(ctx.author.id)] = {
                    "marriage": partner.name,
                    "since": str(ctx.message.created_at),
                    "id": str(partner.id),
                }

            if str(member.id) in File.data:
                File.data[str(member.id)]["marriage"] = ctx.author.name
                File.data[str(member.id)]["id"] = str(ctx.author.id)
                File.data[str(member.id)]["since"] = str(ctx.message.created_at)

            else:

                File.data[str(member.id)] = {
                    "marriage": ctx.author.name,
                    "since": str(ctx.message.created_at),
                    "id": str(ctx.author.id),
                }

            update_json(File.file, File.data)
            em = disnake.Embed(
                title="Success!",
                description="Ah, the wonders of life, congratulations on getting married!",
                colour=get_colour(),
            )
            em.set_image(url="https://giphy.com/clips/livingsingle-7GN899Bf6g98SdFpra")
            await ctx.reply(embed=em)
        except asyncio.TimeoutError:
            await send_embed(
                ctx,
                "Marriage",
                f"Oh no! {member} did not respond in time! Try again at a time that {member.name} is available...",
            )

    @commands.command()
    async def divorce(self, ctx: Context):
        File = GetUser("Love.json")
        if str(ctx.author.id) in File.data:
            marr = File.data[str(ctx.author.id)]["id"]

            del File.data[str(marr)]
            del File.data[str(ctx.author.id)]

            update_json(File.file, File.data)
            await send_embed(ctx, "Divorce...", "They were such a good couple :(")
        else:
            await send_embed(ctx, "Marriage", "You are single bro...")


def setup(bot):
    bot.add_cog(Love(bot))

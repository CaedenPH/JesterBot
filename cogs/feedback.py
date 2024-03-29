import json
from typing import Union

from disnake.ext import commands

from core import Context
from core.utils import send_embed, update_json

with open("./dicts/Feedback.json", "r") as k:
    data = json.load(k)


class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def feedback(self, ctx: Context, *, feedback):
        with open("./dicts/Feedback.json", "r+") as k:
            data = json.load(k)
            data["feedback"]["message"].append(feedback)
            data["feedback"]["author"].append(ctx.author.name)
            data["feedback"]["id"].append(ctx.author.id)
            update_json(k, data)

        await send_embed(ctx, "", "Sent!")

    @commands.command()
    async def viewfeedback(
        self,
        ctx: Context,
        distance: Union[
            int,
            str,
        ] = 0,
        author_from: Union[
            int,
            str,
        ] = None,
    ):
        await send_embed(
            ctx,
            "",
            "**Error: **distance must be an integer (an index placevalue) if no `author_from` is given!",
        ) if hasattr(distance, "upper") and author_from is None else await send_embed(
            ctx,
            "",
            f'*`{distance}`*: "{data["feedback"]["message"][distance]}", submitted by **{data["feedback"]["author"][distance]}**'
            if distance != 0
            else f"**You can index off of the index on the left side. Type `{ctx.prefix}viewfeedback <index>`\n**\n"
            + "\n".join(
                [
                    f"`{num}:` {data['feedback']['message'][k]}**, said by {data['feedback']['author'][k]}**"
                    for num, k in enumerate(range(len(data["feedback"]["message"])))
                    if num <= 9
                ]
            ),
            a="Feedback",
            i_u=ctx.author.display_avatar.url,
        ) if author_from is None else await send_embed(
            ctx,
            "",
            "\n".join(
                [
                    f"`{num}`: {data['feedback']['message'][num]}"
                    for num, k in enumerate(data["feedback"]["author"])
                    if k == author_from
                ]
            ),
            a=f"Feedback from {author_from}",
            i_u=ctx.author.display_avatar.url,
            f=f"All these messges are from {author_from}",
        ) if hasattr(
            author_from, "upper"
        ) else await send_embed(
            ctx,
            "",
            "\n".join(
                [
                    f"`{num}`: {data['feedback']['message'][num]}"
                    for num, k in enumerate(data["feedback"]["id"])
                    if k == author_from
                ]
            ),
            a=f"Feedback from {await self.bot.fetch_user(author_from)}",
            i_u=ctx.author.display_avatar.url,
            f=f"All these messages are from {await self.bot.fetch_user(author_from)}",
        )

    @commands.command(aliases=["dial", "call", "assistance"])
    async def support(self, ctx: Context):
        f = open("./dicts/Dial.json", "r+")
        data = json.load(f)
        if str(ctx.channel.id) in data:
            return await send_embed(
                ctx, "", "This is already engaged in a support dial!"
            )
        data[str(ctx.channel.id)] = True
        update_json(f, data)
        chan = self.bot.get_channel(866598271991545886)
        await send_embed(
            ctx,
            "",
            "You are now connected to **JesterBot offical Support Dial**. Type `j.closesupport` to end your ticket",
        )
        await send_embed(
            chan,
            "",
            f"You are now connected to **{ctx.author}** in **{ctx.guild}** with channel id of **{ctx.channel.id}**",
        )
        await chan.send("<@521226389559443461> - <@298043305927639041>")

    @commands.command(
        aliases=["closedial", "endsupport", "enddial", "dialend", "hangup"]
    )
    async def closesupport(self, ctx: Context, chan=""):
        c = self.bot.get_channel(866598271991545886)
        f = open("./dicts/Dial.json", "r+")
        data = json.load(f)
        if chan:
            if ctx.author.id in [521226389559443461, 298043305927639041]:
                if chan in data:
                    del data[chan]
                    update_json(f, data)
                    return await ctx.reply("**Ended**")
        if str(ctx.channel.id) not in data:
            return await send_embed(ctx, "", "You are not engaged in a support dial!")
        del data[str(ctx.channel.id)]
        update_json(f, data)
        await send_embed(
            ctx, "", "The ticket has been closed! We hope your problem got solved!"
        )
        await send_embed(c, "", f"{ctx.author} ended a call at {ctx.channel.id}")

    @commands.Cog.listener("on_message")
    async def dial(self, message):
        if message.author == self.bot.user:
            return
        f = open("./dicts/Dial.json", "r+")
        data = json.load(f)
        chan = self.bot.get_channel(866598271991545886)
        if message.channel == chan:
            for k in data:
                newchan = self.bot.get_channel(int(k))
                return await newchan.send(f"**{message.author}:** {message.content}")
        if str(message.channel.id) in data:
            return await chan.send(f"**{message.author}:** {message.content}")


def setup(bot):
    bot.add_cog(Feedback(bot))

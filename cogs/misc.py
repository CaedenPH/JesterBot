import os
import disnake
import json
import asyncio
import datetime
import zipfile
import inspect

from disnake.ext import commands
from random import choice
from io import BytesIO
from core.constants import THUMBS_DOWN, THUMBS_UP

from core.utils import get_colour, send_embed
from core import JesterBot, Context
from core.paginator import Paginator


class Misc(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

    @commands.command(
        aliases=["channel_stats", "channel_health", "channel_info", "channel_information"]
    )
    async def channel_status(self, ctx: Context, channel: disnake.TextChannel = None):
        if not channel:
            channel = ctx.channel

        guild = ctx.guild

        embed = disnake.Embed(description="")
        embed.set_author(name="Channel Health:", icon_url=ctx.author.display_avatar.url)

        msg = await ctx.em("Processing... this may take a while.")
        async with ctx.channel.typing():
            count = 0
            async for message in channel.history(
                limit=500000,
                after=datetime.datetime.today() - datetime.timedelta(days=100),
            ):
                count += 1

            if count >= 5000:
                average = "OVER 5000!"
                healthiness = "VERY HEALTHY"

            else:
                try:
                    average = round(count / 100, 2)

                    if 0 > guild.member_count / average:
                        healthiness = "VERY HEALTHY"
                    elif guild.member_count / average <= 5:
                        healthiness = "HEALTHY"
                    elif guild.member_count / average <= 10:
                        healthiness = "NORMAL"
                    elif guild.member_count / average <= 20:
                        healthiness = "UNHEALTHY"
                    else:
                        healthiness = "VERY UNHEALTHY"

                except ZeroDivisionError:
                    average = 0
                    healthiness = "VERY UNHEALTHY"

            embed.description += f"**# of members in guild**: `{guild.member_count}`\n"
            embed.description += (
                f"**# of messages per day on average in {channel}**: `{average}`\n"
            )
            embed.description += f"**Channel health**: `{healthiness}`\n"
            await msg.delete()
            await ctx.reply(embed=embed)

    @commands.command(aliases=["src"])
    async def source(self, ctx: Context, command=None):
        if not command:
            return await ctx.reply("https://github.com/caedenph/jesterbot")
        cmd = self.bot.get_command(command)
        if cmd:
            source = inspect.unwrap(cmd.callback).__code__
            return await ctx.reply(
                f"https://github.com/caedenph/jesterbot/tree/main/{''.join(inspect.getfile(source).split('jesterbot/')[1])}#L{inspect.getsourcelines(source)[1]}"
            )
        await ctx.em("No such command!")

    @commands.command()
    async def invited(self, ctx: Context, user: disnake.Member = None):
        if not user:
            user = ctx.author
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == user:
                totalInvites += i.uses
        await send_embed(
            ctx,
            "",
            f"{user.name} has invited **{totalInvites}** member{'' if totalInvites == 1 else 's'} to the server!",
        )

    @commands.command(description="Sends information about my account")
    async def info(self, ctx: Context, member: disnake.Member = None):
        if not member:
            member = ctx.author

        embed = (
            disnake.Embed(
                title="Information", timestamp=ctx.message.created_at, colour=get_colour()
            )
            .set_thumbnail(url=member.display_avatar.url)
            .add_field(name="Name", value=f"{member.name}")
            .add_field(name="Id", value=f"{member.id}")
            .add_field(name="Joined server at", value=f"{member.joined_at}")
            .add_field(name="Joined disnake at", value=f"{member.created_at}")
            .add_field(name="Nitro", value=f"{member.premium_since}")
            .add_field(name="Mobile", value=f"{member.is_on_mobile()}")
            .add_field(
                name="Flags",
                value=f"{', '.join(f'`{k.name}`' for k in member.public_flags.all())}",
            )
        )

        await ctx.reply(embed=embed)

    @commands.command()
    async def channel(self, ctx: Context):
        embed = disnake.Embed(title="Channel info", colour=get_colour())
        embed.add_field(name="Name", value=f"{ctx.channel.name}", inline=False)
        embed.add_field(name="Id", value=f"{ctx.channel.id}", inline=False)

        await ctx.reply(embed=embed)

    @commands.command(
        description="Make a secure password with a length that you can choose"
    )
    async def password(self, ctx: Context, lengthofpassword: int = 12):
        my_list = ["!", "?", "#"]
        for c in range(97, 123):
            my_list.append(chr(c))
        for e in range(1, 9):
            my_list.append(e)
        for t in range(65, 91):
            my_list.append(chr(t))

        password = ""
        while len(password) != lengthofpassword:
            password += str(choice(my_list))
        x = await ctx.author.send(password)
        await send_embed(ctx, "Password", f"||{x.jump_url}||")

    @commands.command(aliases=["stat"], description="Sends statistics about the server")
    async def stats(self, ctx: Context):

        (members, bots) = [m for m in ctx.guild.members if not m.bot], [
            m for m in ctx.guild.members if m.bot
        ]
        embed = disnake.Embed(title="Stats", colour=get_colour())
        embed.add_field(
            name="Server statistics",
            value=f"""
    Text Channels: {len(ctx.guild.text_channels)}
    Voice Channels: {len(ctx.guild.voice_channels)}
    Total Channels: {len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)}
    Members (bots excluded): {len(members)}
    Bots: {len(bots)}
    Roles in the server: {len(ctx.guild.roles)}
        """,
        )
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def check(
        self,
        ctx: Context,
        days: float = None,
        member: disnake.Member = None,
        channel: disnake.TextChannel = None,
    ):
        if not member:
            member = ctx.author
        if not channel:
            channel = ctx.channel
        if not days:
            days = 1
        if days >= 8:

            days = 7
        embed = disnake.Embed(
            description=f"**Thinking**... **processing...**\n**Calculated time it wil take:** {days * 14.6}\n**From:** {member.name}\n**In channel:** {channel}\nIt roughly takes 12 seconds per extra day, hence why you can only loop through 7 days",
            colour=get_colour(),
        ).set_footer(
            text="This process may take a while because it is gathering all data from the past week while getting ratelimited"
        )
        m = await ctx.reply(embed=embed)
        async with ctx.typing():
            x = datetime.datetime.utcnow() - datetime.timedelta(days=days)
            k = await channel.history(after=x, limit=None).flatten()
            messages = [
                f"{e.content.replace('`', '')}"
                for e in k
                if e.author == member and e.channel == channel
            ]
        await m.delete()
        pag = Paginator(ctx)
        await pag.paginate(
            content=", ".join(messages),
            name=f"{member} has said {len(messages)} messages in the past {days} days",
        )

    @commands.command(
        aliases=[
            "Server_icon",
            "Icon_server",
            "Guild_icon",
            "Server_Avatar",
            "avg",
            "guildav",
            "gc",
        ],
        description="Sends the avatar of the server (profile pic)",
    )
    async def avatarguild(self, ctx: Context):
        embed = disnake.Embed(title="Guild icon", colour=get_colour())
        embed.set_image(url=ctx.guild.icon_url)

        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["messages"],
        description="Says how many messages have been sent since the bot joined",
    )
    async def servermessages(self, ctx: Context, server=""):
        join = ctx.guild.get_member(828363172717133874)
        when = "24th of June 2021"
        joinedat = ""
        for k in str(join.joined_at):
            joinedat += k
        if int(joinedat[5:7]) > 6:
            if int(joinedat[7:9]) > 12:
                when = str(join.joined_at)

        with open("./dicts/Server.json") as k:
            data = json.load(k)

            if not server:
                embed = disnake.Embed(
                    description=f"**{data[str(ctx.guild.id)]['Score']}** messages since the {when}",
                    colour=get_colour(),
                )
            else:
                embed = disnake.Embed(
                    description=f"**{data[server]['Score']}** messages since {when}",
                    colour=get_colour(),
                )
            await ctx.reply(embed=embed)

    @commands.command(
        aliases=["s", "Sugg", "Sug", "Suggester"],
        description="Follow the instructions and a suggestion will appear",
    )
    async def suggest(self, ctx: Context):

        user = ctx.author.id
        username = self.bot.get_user(user)

        try:

            embed = disnake.Embed(title="Suggestion", colour=get_colour())
            embed1 = disnake.Embed(
                title=f"What is the title of your suggestion? Type end at any point to stop and type title to remove the description",
                colour=get_colour(),
            )
            x = await ctx.reply(embed=embed1)
            received_msg = str(
                (
                    await self.bot.wait_for(
                        "message",
                        timeout=60.0,
                        check=lambda m: m.author == ctx.author
                        and m.channel == ctx.channel,
                    )
                ).content
            ).lower()
            if received_msg not in ["end", "title"]:
                msg1 = received_msg
                embed2 = disnake.Embed(
                    title=f"What is the description of your suggestion? Type end at any point to stop",
                    colour=get_colour(),
                )
                y = await ctx.reply(embed=embed2)
                received_msg1 = str(
                    (
                        await self.bot.wait_for(
                            "message",
                            timeout=90.0,
                            check=lambda m: m.author == ctx.author
                            and m.channel == ctx.channel,
                        )
                    ).content
                ).lower()
                if received_msg1 != "end":
                    msg2 = received_msg1
                    embed.add_field(name="Title", value=msg1, inline=False)
                    embed.add_field(name="Description", value=msg2, inline=False)
                    embed.set_footer(
                        text=ctx.author.name, icon_url=username.display_avatar.url
                    )

                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(
                        limit=2,
                        check=lambda m: m.author == ctx.author
                        and m.channel == ctx.channel,
                    )
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction(THUMBS_UP)
                    await msg.add_reaction(THUMBS_DOWN)

                else:
                    embed3 = disnake.Embed(title="Goodbye", colour=get_colour())
                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(
                        limit=2,
                        check=lambda m: m.author == ctx.author
                        and m.channel == ctx.channel,
                    )
                    msg = await ctx.reply(embed=embed3)

            elif received_msg == "end":
                await x.delete()
                await ctx.channel.purge(
                    limit=2,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                )
                embed3 = disnake.Embed(title="Goodbye", colour=get_colour())
                await ctx.reply(embed=embed3)
            else:
                embed2 = disnake.Embed(
                    title=f"What is the Title of your suggestion? Type end at any point to stop",
                    colour=get_colour(),
                )
                y = await ctx.reply(embed=embed2)
                received_msg1 = str(
                    (
                        await self.bot.wait_for(
                            "message",
                            timeout=90.0,
                            check=lambda m: m.author == ctx.author
                            and m.channel == ctx.channel,
                        )
                    ).content
                ).lower()
                if received_msg1 != "end":

                    embed.add_field(name="Title", value=received_msg1, inline=False)

                    embed.set_footer(
                        text=ctx.author.name, icon_url=username.display_avatar.url
                    )

                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(
                        limit=2,
                        check=lambda m: m.author == ctx.author
                        and m.channel == ctx.channel,
                    )
                    msg = await ctx.reply(embed=embed)
                    await msg.add_reaction(THUMBS_UP)
                    await msg.add_reaction(THUMBS_DOWN)
        except asyncio.TimeoutError:
            embed = disnake.Embed(
                title="Time ran out, restart the ticket", colour=get_colour()
            )
            await ctx.reply(embed=embed)

    @commands.command()
    async def rules(self, ctx: Context):
        embed = disnake.Embed(title="Standard Rules", description="", colour=get_colour)
        embed.add_field(
            name="`1` NSFW ",
            value="All NSFW outside of an nsfw channel is banned and you will be muted and even banned up to the severity of the content.",
            inline=False,
        )

        embed.add_field(
            name="`2` Hate ",
            value="All forms of racism and homophobia will result in a ban with potential ban appeal in the near future after the ban.",
            inline=False,
        )

        embed.add_field(
            name="`3` Toxicm ",
            value="Unless you're being toxic as a joke it's prohibited, please report anyone is is harassing//bullying you please report to any of the staff members!",
            inline=False,
        )

        embed.add_field(
            name="`4` Advertising",
            value="Any form of advertising will be a kick & mute for every person, doesn't matter if it's in dms, chat, etc.",
            inline=False,
        )

        embed.set_image(
            url="https://i.pinimg.com/originals/09/9a/57/099a57d2fe430ea56cdc5ed4979ff909.gif"
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def booster(self, ctx: Context):
        embed = disnake.Embed(
            title="Booster perks",
            description="Boosting this server can help give us many other perks! Although it's not required we would love for you to boost us!",
            colour=get_colour(),
        )
        embed.add_field(
            name="`1` Free role ",
            value="When you boost you'll be able to choose a role for you and a friend!",
            inline=False,
        )

        embed.add_field(
            name="`2` Giveaway restrictions ",
            value="You will be able to bypass all giveaway restrictions!",
            inline=False,
        )

        embed.add_field(
            name="`3` Role ",
            value="Custom booster role that is above members!",
            inline=False,
        )

        embed.add_field(name="`4` Hugs", value="You'll get free hugs <3", inline=False)

        embed.set_image(
            url="https://support.discord.com/hc/article_attachments/360029033111/nitro_tank_gif.gif"
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def nitro(self, ctx: Context):
        embed = disnake.Embed(
            title="Nitro perks",
            description="Nitro can improve disnake experience and give many fun perks!",
            colour=get_colour(),
        )
        embed.add_field(
            name="`1` Live streams",
            value="Screen share on PC in `720p 60fps` or `1080p 30fps` - Stream at source",
            inline=False,
        )
        embed.add_field(
            name="`2` Gif",
            value="Upload and use animated avatars and emojis",
            inline=False,
        )
        embed.add_field(
            name="`3` Custom emojis",
            value="Share custom emojis across all servers",
            inline=False,
        )
        embed.add_field(
            name="`4` Large file uploads",
            value="Larger file upload size from 8mb to 100mb with nitro or 50mb with nitro classic",
            inline=False,
        )
        embed.set_thumbnail(
            url="https://cdn.disnakeapp.com/attachments/803430815714902060/852926789981437982/image0.png"
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=["zip"])
    async def zipemojis(self, ctx: Context):
        if len(ctx.guild.emojis) == 0:
            return await ctx.em(f"Your server doesn't have any custom emojis.")

        m = await ctx.em(
            f"Alright! Zipping all emojis owned by this server for you, This can take some time"
        )
        buf = BytesIO()

        async with ctx.typing():
            with zipfile.ZipFile(buf, "w") as f:
                for emoji in ctx.guild.emojis:
                    _bytes = await emoji.read()
                    f.writestr(
                        f'{emoji.name}.{"gif" if emoji.animated else "png"}', _bytes
                    )

            buf.seek(0)

        try:
            await m.delete()
        except:
            pass
        finally:
            await ctx.reply(
                f"{ctx.author.mention} Sorry to keep you waiting, here you go:",
                file=disnake.File(fp=buf, filename="emojis.zip"),
            )


def setup(bot: JesterBot):
    bot.add_cog(Misc(bot))

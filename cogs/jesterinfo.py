from webbrowser import get
import disnake
import json
import time

from disnake.ext import commands
from datetime import datetime

from core.utils import create_embed
from core.utils import get_colour, update_json, send_embed
from core.constants import LOADING
from core import Context, JesterBot


class JesterInfo(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

    @commands.command()
    async def links(self, ctx: Context):
        links = "[Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?self.bot_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot) │ [Vote for me!](https://top.gg/bot/828363172717133874/vote)"
        await send_embed(ctx, "", links)

    @commands.command()
    async def uptime(self, ctx: Context):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        (hours, remainder) = divmod(int(delta_uptime.total_seconds()), 3600)
        (minutes, seconds) = divmod(remainder, 60)
        (days, hours) = divmod(hours, 24)
        return await send_embed(
            ctx,
            "",
            f"I've been up for **{days}** Days, **{hours}** Hours, **{minutes}** Minutes, and **{seconds}** Seconds!",
        )

    @commands.command(
        aliases=["Ver", "versions"],
        description="Sends the version that the disnake bot is currently on - Changes frequently as updates occur",
    )
    async def version(self, ctx: Context):
        with open("./dicts/Updates.json", "r") as x:
            data = json.load(x)
            for m in data:

                embed = disnake.Embed(title=f"{data[m]['Version']}", colour=get_colour())
                await ctx.reply(embed=embed)

    @commands.command(
        aliases=["scoreover", "Overallscore", "Overall_score"],
        description="Sends the total number of commands used",
    )
    async def score(self, ctx: Context):
        score = await self.bot.db.fetchone("SELECT score FROM overall_score")
        await send_embed(
            ctx,
            "Score",
            f"`{score[0]}` commands have been ran through my entire lifetime!",
        )

    @commands.command(
        aliases=["notes", "patchnotes", "Updates", "Patch_Notes", "PT", "up"],
        description="Sends the most recent update to the bot",
    )
    async def update(self, ctx: Context):
        with open("./dicts/Updates.json", "r") as x:
            data = json.load(x)

            for m in data:

                if data[m]["Version"] is None:
                    embed = disnake.Embed(
                        description="Updates is currently being updated, no data to send",
                        colour=get_colour(),
                    )
                    return await ctx.reply(embed=embed)
                if data[m]["Bug fixes"] is None:
                    embed = disnake.Embed(
                        description="Updates is currently being updated, no data to send",
                        colour=get_colour(),
                    )
                    await ctx.reply(embed=embed)
                if data[m]["New commands"] is None:
                    embed = disnake.Embed(
                        description="Updates is currently being updated, no data to send",
                        colour=get_colour(),
                    )
                    await ctx.reply(embed=embed)
                if data[m]["Other"] is None:
                    embed = disnake.Embed(
                        description="Updates is currently being updated, no data to send",
                        colour=get_colour(),
                    )
                    await ctx.reply(embed=embed)
                else:
                    username = self.bot.get_user(828363172717133874)
                    embed = disnake.Embed(
                        title=f"**Updates**  \u200b <:Jesterinfo:863075610048987166>",
                        description="*Everytime there is a new update it will be \nposted here along with a version update!*",
                        colour=get_colour(),
                    )
                    embed.add_field(
                        value=f"{data[m]['Version']}", name="**Version**", inline=True
                    )

                    embed.add_field(
                        value=f"{data[str(m)]['Bug fixes']}",
                        name="**Bug fixes**",
                        inline=False,
                    )
                    embed.add_field(
                        value=f"{data[str(m)]['New commands']}",
                        name="**New commands**",
                        inline=True,
                    )
                    embed.add_field(
                        value=f"{data[str(m)]['Other']}", name="**Other**", inline=False
                    )

                    embed.set_footer(
                        text=ctx.author.name, icon_url=username.display_avatar.url
                    )
                    embed.set_thumbnail(
                        url="https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif"
                    )

                    await ctx.reply(embed=embed)

    @commands.command(
        aliases=["selfruns", "commands_used", "Selfrun", "Self_Score"],
        description="Sends the ammount of commands that you personally have ran",
    )
    async def selfscore(self, ctx: Context):
        with open("./dicts/score.json") as f:
            data = json.load(f)
            if str(ctx.author.id) in data:
                embed = disnake.Embed(
                    title=f"The ammount of commands you have ran are {data[str(ctx.author.id)]['score']}",
                    colour=get_colour(),
                )
                await ctx.reply(embed=embed)

    @commands.command(aliases=["binv", "botinv"])
    async def invite(self, ctx: Context):
        embed = disnake.Embed(
            title=f"I am currently in {len(self.bot.guilds)} servers!",
            description="[Official server](https://discord.gg/2654CuU3ZU) │ [Invite me!](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591)",
            colour=get_colour(),
        )
        embed.set_author(icon_url=ctx.author.display_avatar.url, name="Invite")

        await ctx.reply(embed=embed)

    @commands.command(aliases=["commandtop", "cmdtop", "topcmd"])
    async def topcommands(self, ctx: Context):
        x = []
        y = "\n"
        with open("./dicts/commands_used.json") as k:
            embed = disnake.Embed(colour=get_colour())
            embed.set_author(name="Top commands", icon_url=ctx.author.display_avatar.url)

            data = json.load(k)

            def get_key(item):
                return item[1]["score"]

            sorted_scores = sorted(data.items(), key=get_key, reverse=True)[:11]

            for item in sorted_scores:

                x.append(f"{item[0]}: {item[1]['score']}")

            embed.add_field(name=f"\u200b", value=f"**{y.join(x)}**", inline=False)

            await ctx.reply(embed=embed)

    @commands.command(
        aliases=["membtop", "topmemb", "memtop"],
        description="Sends the top members that have used the bot",
    )
    async def topmembers(self, ctx: Context):
        x = []
        y = "\n"
        with open("./dicts/score.json") as k:
            embed = disnake.Embed(colour=get_colour())
            embed.set_author(name="Top members", icon_url=ctx.author.display_avatar.url)
            data = json.load(k)

            def get_key(item):
                return item[1]["score"]

            sorted_scores = sorted(data.items(), key=get_key, reverse=True)[:11]

            for item in sorted_scores:
                for datas in data:
                    if item[0] in datas:

                        name = data[datas]["name"]
                x.append(f"{name}: {item[1]['score']}")

            embed.add_field(name=f"\u200b", value=f"**{y.join(x)}**", inline=False)

            await ctx.reply(embed=embed)

    @commands.command(aliases=["ammount_of_commands", "hmc"])
    async def how_many_commands(self, ctx: Context):
        await ctx.em(
            f"The bot has **{len([k for k in self.bot.commands if not k.hidden])}** available commands and **{len([k for k in self.bot.commands if k.hidden])}** hidden commands"
        )

    @commands.command(
        aliases=["pin", "pingy", "ms", "Latency"], description="Sends the ping of the bot"
    )
    async def ping(self, ctx: Context):
        time1 = time.perf_counter()
        msg = await ctx.reply(
            embed=disnake.Embed(title=f"Pinging... {LOADING}", color=get_colour())
        )
        time2 = time.perf_counter()

        db_time1 = time.perf_counter()
        await self.bot.db.execute(
            "SELECT prefixes FROM prefix WHERE user_id = ?", (ctx.author.id,)
        )
        db_time2 = time.perf_counter()

        embed = (
            disnake.Embed(
                title="🏓  Pong!",
                description=f"""\
```yaml
API      : {round(self.bot.latency*1000)}ms
Bot      : {round((time2-time1)*1000)}ms
Database : {round((db_time2-db_time1)*1000)}ms
```
            """,
            )
            .set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            .set_footer(
                text=f"Servers in: {len(self.bot.guilds)} │ Overall users: {len(self.bot.users)}"
            )
        )
        await msg.edit(embed=embed)

    @commands.command(
        aliases=["pref", "prefixs", "pre", "prefixes"],
        description="Change the prefix of the bot for you personally",
    )
    async def prefix(self, ctx: Context, *, prefix=None):
        if not prefix:
            async with ctx.typing():
                embed = await create_embed(ctx.message, self.bot)
            return await ctx.reply(embed=embed)

        prefixes = prefix.split(" ")
        await self.bot.insert_prefix(ctx.author.id, prefixes)

        embed = disnake.Embed(
            description=f"New prefixes are: {', '.join([f'`{prefix}`' for prefix in prefixes])}\nPing me for my prefixes if you forget!",
            colour=get_colour(),
        )
        embed.set_author(icon_url=ctx.author.display_avatar.url, name="Prefix")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["devs", "helpers", "coder", "coders"])
    async def credits(self, ctx: Context):
        coder = self.bot.get_user(298043305927639041)
        ideas_designer = self.bot.get_user(780555299106586634)
        helper = self.bot.get_user(483631842554019841)
        helper2 = self.bot.get_user(652407551849267200)
        sales = self.bot.get_user(521226389559443461)
        designer = self.bot.get_user(427120167361708032)
        embed = disnake.Embed(
            title="Credits",
            description=f"""
        **Coder:** *{coder.name}*
        **Designer:** *{designer.name}*
        **Helpers:** *{helper.name}*, *{helper2.name}*
        **Sales/Promoter:** *{sales.name}*
        **Ideas/layout designer:** *{ideas_designer.name}*
        
        """,
            colour=get_colour(),
        )
        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["ccolour"], description="change the color of the embeds!", hidden=True
    )
    async def ccolor(self, ctx: Context, *, colour: int):
        if colour.startswith("0x") and len(colour) != 8:
            embed = disnake.Embed(
                title="Colour",
                description="Put `0x` infront of the six letter/number [color](https://www.color-hex.com/)",
                colour=get_colour(),
            )
            return await ctx.reply(embed=embed)

        with open("./dicts/Color.json", "r+") as k:
            data = json.load(k)
            data["colour"] = colour
            update_json(k, data)

            embed = disnake.Embed(title="changed", colour=int(colour, 16))
            await ctx.reply(embed=embed)

    @commands.command()
    async def showcmds(self, ctx: Context):
        x = []
        embed = disnake.Embed(colour=get_colour())
        for command in self.bot.commands:

            x.append(f"`{command.name}`")
        xnum = 0
        for i in range(0, len(x)):
            xnum += 1
            if xnum == 25:
                if i <= 25:
                    embed.add_field(name=i, value=", ".join(x[0:i]), inline=False)
                else:

                    r = i - 25
                    embed.add_field(name=i, value=", ".join(x[r:i]), inline=False)

                xnum = 0

        await ctx.reply(embed=embed)

    @commands.command()
    async def serversin(self, ctx: Context):

        x = []
        num = 0
        for g in self.bot.guilds:
            x.append(g.name)
            num += 1

        await ctx.reply(", ".join(x[1:25]))
        await ctx.reply(", ".join(x[26 : len(x)]))


def setup(bot):
    bot.add_cog(JesterInfo(bot))

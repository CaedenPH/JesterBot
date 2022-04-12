import simpleeval
import re
import disnake
import async_cse

import pytz
import unicodedata
import wikipedia

from urllib.request import urlopen
from typing import Tuple
from pyMorseTranslator import translator
from datetime import datetime

from disnake.ext import commands

from core.utils import get_colour, send_embed
from core.utils.commands.eval import run_eval
from core.paginator import Paginator
from core.constants import (
    CLOSE,
    MORSE_TO_TEXT,
    TEXT_TO_MORSE,
    ASCII_DESCRIPTION,
    GOOGLE_KEY,
)
from core import Context
from .calculator import CalculatorView

encoder = translator.Encoder()
decoder = translator.Decoder()


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.google = async_cse.Search(GOOGLE_KEY)

    @commands.command(aliases=["calc"])
    async def calculator(self, ctx: Context):
        embed = (
            disnake.Embed(description="```yaml\n0```")
            .set_author(name="Calculator", icon_url=ctx.author.display_avatar.url)
            .set_footer(
                text="To interact with your virtual calculator, click the shown buttons."
            )
        )

        await ctx.reply(embed=embed, view=CalculatorView(embed, ctx))

    @commands.command()
    async def google(self, ctx: Context, *, query: str):
        try:
            results = await self.google.search(query, safesearch=True, image_search=False)
        except async_cse.NoResults:
            return await ctx.reply(f"No **Results** found for search **{query}**")
        if not results:
            return await ctx.reply(f"No **Results** found for search **{query}**")

        await ctx.reply(
            embed=disnake.Embed(
                title=f"Query: {query}",
                description="\n".join(
                    [
                        f"[{res.title}]({res.url})\n{res.description}\n\n"
                        for res in results[:5]
                    ]
                ),
                color=0x489CC4,
            )
            .set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
            )
            .set_author(
                name=ctx.author,
                icon_url="https://staffordonline.org/wp-content/uploads/2019/01/Google.jpg",
            )
        )

    @commands.command()
    async def qr(self, ctx: Context, *, text):
        m = await ctx.reply("**Creating...**")
        async with ctx.typing():
            async with self.bot.client.get(
                f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text}"
            ) as response:

                await send_embed(ctx, f"Qr code for {text}", i=response.url)
                await m.delete()

    @commands.command(hidden=True)
    async def hibernate(self, ctx: Context):
        await ctx.reply(":thumbsup:")
        self.bot.hiber = True

    @commands.command(hidden=True)
    async def hiber(self, ctx: Context):
        await ctx.reply(":thumbsup:")
        self.bot.hiber = False

    @commands.command()
    async def math(self, ctx: Context, *, math=None):
        if not math:
            return await send_embed(
                ctx,
                "",
                "**The current list of available eval operations**",
                i="https://cdn.disnakeapp.com/attachments/836812307971571762/846334605669826600/unknown.png",
            )

        result = simpleeval.simple_eval(math)
        embed = disnake.Embed(colour=get_colour())
        embed.set_footer(
            text=str(ctx.author) + " | Evaluation", icon_url=ctx.author.display_avatar.url
        )
        embed.add_field(
            name="Your expression: ", value=f'```yaml\n"{math}"\n```', inline=False
        )
        embed.add_field(name="Result: ", value=f"```\n{result}\n```")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["wiki"])
    async def wikipedia(self, ctx: Context, *, query):
        await ctx.em(wikipedia.summary(query))

    @commands.command()
    async def charinfo(self, ctx: Context, *, characters: str):
        """Shows you information on up to 50 unicode characters."""
        match = re.match(r"<(a?):(\w+):(\d+)>", characters)
        if match:
            return await send_embed(ctx, "", "Custom emojis are not allowed")

        if len(characters) > 50:
            return await send_embed(
                ctx, "", f"Too many characters ({len(characters)}/50)"
            )

        def get_info(char: str) -> Tuple[str, str,]:
            digit = f"{ord(char):x}"
            if len(digit) <= 4:
                u_code = f"\\u{digit:>04}"
            else:
                u_code = f"\\U{digit:>08}"
            url = f"https://www.compart.com/en/unicode/U+{digit:>04}"
            name = f"[{unicodedata.name(char, '')}]({url})"
            info = f"`{u_code.ljust(10)}`: {name} - {disnake.utils.escape_markdown(char)}"
            return (info, u_code)

        (char_list, raw_list) = zip(*(get_info(c) for c in characters))
        embed = disnake.Embed(colour=get_colour())
        embed.add_field(name="Character info", value="\n".join(char_list))
        if len(characters) > 1:
            embed.add_field(
                name="Full Raw Text", value=f"`{''.join(raw_list)}`", inline=False
            )

        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["fib"],
        description="Sends the numbers of the fibinaci upto the number provided",
    )
    async def fibonacci(self, ctx: Context, sequences=10000000000000):
        x = []

        if sequences > 1000000000000000:
            sequences = 100000000000000

        (a, b) = (0, 1)
        while a < sequences:
            x.append(str(a))

            (a, b) = (b, a + b)

        embed = disnake.Embed(
            title="Fibinaci", description=f"{', '.join(x)}", colour=get_colour()
        )
        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["av", "avatars"],
        description="Sends the mentioned users avatar or if none is specified, the usrs avatar",
    )
    async def avatar(self, ctx: Context, user: disnake.Member = None):
        if user is None:
            user = ctx.author.id
            username = self.bot.get_user(user)
            embed = disnake.Embed(title="Avatar", colour=get_colour())
            embed.set_author(name=username.name, icon_url=username.display_avatar.url)
            embed.set_image(url=username.display_avatar.url)
            await ctx.reply(embed=embed)

        else:

            username = self.bot.get_user(user.id)
            embed = disnake.Embed(title=f"Avatar", colour=get_colour())
            embed.set_author(name=username.name, icon_url=username.display_avatar.url)
            embed.set_image(url=username.display_avatar.url)
            await ctx.reply(embed=embed)

    @commands.command(
        aliases=["tz", "time", "zone"],
        description="Sends the current time of the [origin]. To get all of the places recognisable, leave `origin` blank",
    )
    async def timezone(self, ctx: Context, origin=None):
        try:
            if not origin:
                result = pytz.all_timezones
                y = Paginator(ctx)
                return await y.paginate(content=", ".join(result), name="Timezones")

            tz_NY = pytz.timezone(origin)
            now = datetime.now(tz_NY)
            x = str(now)
            _date = x[:10]
            _time = x[11:19]
            embed = disnake.Embed(
                title=f"**Time:** {_time} │ **Date:** {_date}", colour=get_colour()
            )
            embed.set_author(name="Datetime", icon_url=ctx.author.display_avatar.url)

            await ctx.reply(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Error", description=f"**TimeZoneError: {e}**", colour=get_colour()
            )
            await ctx.reply(embed=embed)

    @commands.command(aliases=["bin"])
    async def binary(self, ctx: Context, *, text):
        async with self.bot.client.get(
            url=f"https://some-random-api.ml/binary?text={text}"
        ) as response:
            fox = await response.json()

            embed = disnake.Embed(colour=get_colour())
            embed.add_field(name="Binary", value=f"{fox['binary']}")
            await ctx.reply(embed=embed)

    @commands.command(aliases=["unbin"])
    async def unbinary(self, ctx: Context, *, nums: str):
        async with self.bot.client.get(
            url=f"https://some-random-api.ml/binary?decode={nums}"
        ) as response:
            fox = await response.json()

            embed = disnake.Embed(colour=get_colour())
            embed.add_field(name="Decoded from binary", value=f"{fox['text']}")
            await ctx.reply(embed=embed)

    @commands.command(description=ASCII_DESCRIPTION)
    async def ascii(self, ctx: Context, *, text=None):
        x = []
        p = []
        num = 0
        if not text:

            for i in range(1, 256):
                num += 1
                if num <= 32:
                    pass
                else:

                    x.append(f"{chr(i)}")
            embed = disnake.Embed(
                title="Ascii:",
                description="\n*starting from 32 because characters prior to that number are not used, therefore sending blanks* \n"
                + f'```py\n{", ".join(x)}```',
                colour=get_colour(),
            )
            embed.set_footer(
                text="Type j.help ascii to get information about what the ascii table is. | `,` signifies a new character."
            )
            return await ctx.reply(embed=embed)

        z = text.split(" ")
        for c in z:

            for t in c:
                p.append(str(ord(t)))

            x.append(f"\n`{c}: {'-'.join(p)}`")
            p = []
        embed = disnake.Embed(
            title="Ascii:", description=", ".join(x), colour=get_colour()
        )
        embed.set_footer(
            text="Type j.help ascii to get information about what the ascii table is. | '-' signifies a new character."
        )
        await ctx.reply(embed=embed)

    @commands.command(
        aliases=["morse_code", "mcode"],
        description="""Encode or decode text/morse code into morse code/plain text, type .morse for help""",
    )
    async def morse(self, ctx: Context, *, string):
        _tempset = set(string)
        check = True
        for char in _tempset:
            if char not in [".", "-", " "]:
                check = False

        if check is True:
            _templist = str(string).split(" ")
            converted = "".join(MORSE_TO_TEXT[str(i)] for i in _templist)

            await send_embed(ctx, "Morse ---> Text", f"```yaml\n{converted}```")
        else:
            _templist = []
            for char in str(string):
                _templist.append(char)
            try:
                converted = " ".join(TEXT_TO_MORSE[str(i).upper()] for i in _templist)
                if len(converted) <= 1998:
                    await send_embed(ctx, "Text ---> Morse", f"```yaml\n{converted}```")
                else:

                    y = await Paginator(ctx)
                    await y.paginate(content=converted, name="Morse/Text")
            except KeyError:
                return await ctx.reply(
                    f"{CLOSE} The String contains some characters which cannot be converted into Morse!\n> If you think that's a Mistake, please report it to my Developers, they'll Review and fix it :)"
                )

    @commands.command(aliases=["eval2", "e2"], description="run code", hidden=True)
    async def evaldir(self, ctx: Context, *, code):
        x = await run_eval(ctx, code, _eval="dir")

        try:
            await ctx.reply(x)
        except:
            pass

    @commands.command(aliases=["eval1", "e1"], description="run code", hidden=True)
    async def evalreturn(self, ctx: Context, *, code):
        x = await run_eval(ctx, code, _eval="return")

        try:
            await ctx.reply(x)
        except:
            pass

    @commands.command(description="run code", hidden=True, aliases=["e"])
    async def eval(self, ctx: Context, *, code):
        x = await run_eval(ctx, code)
        try:
            await ctx.reply(x)
        except:
            pass

    @commands.command(aliases=["tinyurl", "shorten"])
    async def shorten_url(self, ctx: Context, *, url: str):
        tinyurl = await self.bot.loop.run_in_executor(
            None,
            lambda: urlopen("http://tinyurl.com/api-create.php?url=" + url)
            .read()
            .decode("utf-8"),
        )

        await ctx.message.delete()
        return await ctx.em(f"**Your tinyurl:** {tinyurl}")


def setup(bot):
    bot.add_cog(Utils(bot))

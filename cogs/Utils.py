from urllib.request import urlopen
from disnake.utils import _get_description
from core.constants import CLOSE
import disnake, requests
from disnake.ext import commands

from pyMorseTranslator import translator
import pytz, typing
from datetime import datetime

from core.utils.utils import thecolor, Json, thebed
from core.utils.commands.eval import run_eval
from core.paginator import Paginator
from core import Context

import simpleeval
import re
from typing import Tuple
import unicodedata

import wikipedia


sup = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "-": "⁻",
}
norm = {
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
}
operations = ["/", "*", "+", "-"]

encoder = translator.Encoder()
decoder = translator.Decoder()


class buttons(disnake.ui.View):
    def __init__(self, embed: disnake.Embed, ctx: commands.Context):
        super().__init__()

        self.embed = embed
        self.ctx = ctx

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        if interaction.author == self.ctx.author:
            return True

        await interaction.response.send_message(
            "This is not your calculator!", ephemeral=True
        )
        return False

    def get_description(self) -> str:
        return self.embed.description[8:-3]

    def edit_embed(self, label) -> str:
        content = self.get_description()
        if content == "0":
            return f"```yaml\n{label}```"

        if "Out" in content:
            return f"```yaml\n{label}```"
        if content[-1] == "ˣ":
            return f"```yaml\n{content[:-1]}{sup[label]}```"
        if content[-1] in norm:
            return f"```yaml\n{content}{sup[label]}```"
        return f"```yaml\n{content}{label}```"

    @disnake.ui.button(label="1", style=disnake.ButtonStyle.grey, row=0)
    async def first_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="2", style=disnake.ButtonStyle.grey, row=0)
    async def second_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="3", style=disnake.ButtonStyle.grey, row=0)
    async def third_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="*", style=disnake.ButtonStyle.green, row=0)
    async def fourth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):

        self.embed.description = self.edit_embed(" * ")
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="√", style=disnake.ButtonStyle.green, row=0)
    async def fifth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="4", style=disnake.ButtonStyle.grey, row=1)
    async def row_two_first_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="5", style=disnake.ButtonStyle.grey, row=1)
    async def row_two_second_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="6", style=disnake.ButtonStyle.grey, row=1)
    async def row_two_third_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="-", style=disnake.ButtonStyle.green, row=1)
    async def row_two_fourth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(" - ")
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="ˣ", style=disnake.ButtonStyle.green, row=1)
    async def row_two_fifth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="7", style=disnake.ButtonStyle.grey, row=2)
    async def row_three_first_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="8", style=disnake.ButtonStyle.grey, row=2)
    async def row_three_second_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="9", style=disnake.ButtonStyle.grey, row=2)
    async def row_three_third_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="+", style=disnake.ButtonStyle.green, row=2)
    async def row_three_fourth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(" + ")
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="⌫", style=disnake.ButtonStyle.red, row=2)
    async def row_three_fifth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        content = self.get_description()
        display = f"```yaml\n{self.get_description()[:-1] if self.get_description() != '0' else '0'}```"

        if content[-1] == " " and content[-2] in operations:
            display = f"```yaml\n{content[:-3]}```"

        self.embed.description = display
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label=".", style=disnake.ButtonStyle.grey, row=3)
    async def row_four_first_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="0", style=disnake.ButtonStyle.grey, row=3)
    async def row_four_second_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="=", style=disnake.ButtonStyle.grey, row=3)
    async def row_four_third_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        display = self.get_description()
        equation = "".join([k if k not in norm else f"**{norm[k]}" for k in display])
        pattern = re.compile("^√(\d+)")
        equation = pattern.sub("\\1 ** 0.5 ", equation)

        try:
            result = simpleeval.simple_eval(equation)
        except Exception as e:
            result = "Error! Something went wrong"

        self.embed.description = f"```yaml\nIn ❯❯ {display} \nOut ❯❯ {result}```"
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="/", style=disnake.ButtonStyle.green, row=3)
    async def row_four_fourth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(" / ")
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="Clear", style=disnake.ButtonStyle.red, row=3)
    async def row_four_fifth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = "```yaml\n0```"
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="(", style=disnake.ButtonStyle.blurple, row=4)
    async def row_five_first_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label=")", style=disnake.ButtonStyle.blurple, row=4)
    async def row_five_second_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(button.label)
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="Space", style=disnake.ButtonStyle.red, row=4)
    async def row_five_third_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        self.embed.description = self.edit_embed(" ")
        await interaction.response.edit_message(embed=self.embed)

    @disnake.ui.button(label="Sci", style=disnake.ButtonStyle.red, row=4)
    async def row_five_fourth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await interaction.response.send_message("Soon to come...", ephemeral=True)

    @disnake.ui.button(label="Exit", style=disnake.ButtonStyle.red, row=4)
    async def row_five_fifth_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await interaction.response.edit_message()
        self.stop()


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["calc"])
    async def calculator(self, ctx: Context):
        embed = (
            disnake.Embed(description="```yaml\n0```")
            .set_author(
                name="Calculator",
                icon_url=ctx.author.avatar.url,
            )
            .set_footer(
                text="To interact with your virtual calculator, click the shown buttons."
            )
        )

        await ctx.send(embed=embed, view=buttons(embed, ctx))

    @commands.command()
    async def qr(self, ctx: Context, *, text):
        m = await ctx.send("**Creating...**")
        async with ctx.typing():
            response = requests.get(
                f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text}"
            )

        await thebed(ctx, f"Qr code for {text}", i=response.url)
        await m.delete()

    @commands.command(hidden=True)
    async def hibernate(self, ctx: Context):
        await ctx.send(":thumbsup:")
        self.bot.hiber = True

    @commands.command(hidden=True)
    async def hiber(self, ctx: Context):
        await ctx.send(":thumbsup:")
        self.bot.hiber = False

    @commands.command()
    async def math(self, ctx: Context, *, math=None):
        if not math:
            return await thebed(
                ctx,
                "",
                "**The current list of available eval operations**",
                i="https://cdn.disnakeapp.com/attachments/836812307971571762/846334605669826600/unknown.png",
            )

        result = simpleeval.simple_eval(math)
        embed = disnake.Embed(color=thecolor())
        embed.set_footer(
            text=str(ctx.author) + " | Evaluation", icon_url=ctx.author.avatar.url
        )
        embed.add_field(
            name="Your expression: ", value=f'```yaml\n"{math}"\n```', inline=False
        )
        embed.add_field(name="Result: ", value=f"```\n{result}\n```")
        await ctx.send(embed=embed)

    @commands.command(aliases=["wiki"])
    async def wikipedia(self, ctx, *, query):
        await ctx.em(wikipedia.summary(query))

    @commands.command()
    async def charinfo(self, ctx: Context, *, characters: str):
        """Shows you information on up to 50 unicode characters."""
        match = re.match(r"<(a?):(\w+):(\d+)>", characters)
        if match:
            return await thebed(ctx, "", "Custom emojis are not allowed")

        if len(characters) > 50:
            return await thebed(ctx, "", f"Too many characters ({len(characters)}/50)")

        def get_info(char: str) -> Tuple[str, str]:
            digit = f"{ord(char):x}"
            if len(digit) <= 4:
                u_code = f"\\u{digit:>04}"
            else:
                u_code = f"\\U{digit:>08}"
            url = f"https://www.compart.com/en/unicode/U+{digit:>04}"
            name = f"[{unicodedata.name(char, '')}]({url})"
            info = (
                f"`{u_code.ljust(10)}`: {name} - {disnake.utils.escape_markdown(char)}"
            )
            return info, u_code

        char_list, raw_list = zip(*(get_info(c) for c in characters))
        embed = disnake.Embed(color=thecolor())
        embed.add_field(name="Character info", value="\n".join(char_list))
        if len(characters) > 1:
            embed.add_field(
                name="Full Raw Text", value=f"`{''.join(raw_list)}`", inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(
        aliases=["fib"],
        description="Sends the numbers of the fibinaci upto the number provided",
    )
    async def fibonacci(self, ctx: Context, sequences=10000000000000):
        x = []

        if sequences > 1000000000000000:
            sequences = 100000000000000

        a, b = 0, 1
        while a < sequences:
            x.append(str(a))

            a, b = b, a + b

        embed = disnake.Embed(
            title="Fibinaci", description=f"{', '.join(x)}", colour=thecolor()
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["av", "avatars"],
        description="Sends the mentioned users avatar or if none is specified, the usrs avatar",
    )
    async def avatar(self, ctx: Context, user: disnake.Member = ""):
        if user == "":
            user = ctx.author.id
            username = self.bot.get_user(user)
            embed = disnake.Embed(title=f"Avatar", colour=thecolor())
            embed.set_author(name=username.name, icon_url=username.avatar.url)
            embed.set_image(url=username.avatar.url)
            await ctx.send(embed=embed)

        else:

            username = self.bot.get_user(user.id)
            embed = disnake.Embed(title=f"Avatar", colour=thecolor())
            embed.set_author(name=username.name, icon_url=username.avatar.url)
            embed.set_image(url=username.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(
        aliases=["tz", "time", "zone"],
        description="Sends the current time of the [origin]. To get all of the places recognisable, leave `origin` blank",
    )
    async def timezone(self, ctx: Context, origin=None):
        try:
            if not origin:
                var = ""
                num = 0
                result = pytz.all_timezones
                y = Paginator(ctx)
                return await y.paginate(content=", ".join(result), name="Timezones")

            tz_NY = pytz.timezone(origin)
            now = datetime.now(tz_NY)
            x = str(now)
            _date = x[:10]
            _time = x[11:19]
            embed = disnake.Embed(
                title=f"**Time:** {_time} │ **Date:** {_date}", colour=thecolor()
            )
            embed.set_author(name="Datetime", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Error", description=f"**TimeZoneError: {e}**", colour=thecolor()
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["bin"])
    async def binary(self, ctx: Context, *, text):

        response = requests.get(f"https://some-random-api.ml/binary?text={text}")
        fox = response.json()
        embed = disnake.Embed(color=thecolor())
        embed.add_field(name="Binary", value=f"{fox['binary']}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["unbin"])
    async def unbinary(self, ctx: Context, *, nums: str):

        response = requests.get(f"https://some-random-api.ml/binary?decode={nums}")
        fox = response.json()
        embed = disnake.Embed(color=thecolor())
        embed.add_field(name="Decoded from binary", value=f"{fox['text']}")
        await ctx.send(embed=embed)

    @commands.command(
        description="""ASCII was developed from telegraph code. Work on the ASCII standard began in May 1961. The first edition of the standard was published in 1963. Compared to earlier telegraph codes, the proposed Bell code and ASCII were both ordered for more convenient sorting (i.e., alphabetization) of lists.

The use of ASCII format for Network Interchange was described in 1969. That document was formally elevated to an Internet Standard in 2015.

Originally based on the English alphabet, ASCII encodes 128 specified characters into seven-bit integers as shown by the ASCII chart above. Ninety-five of the encoded characters are printable: these include the digits 0 to 9, lowercase letters a to z, uppercase letters A to Z, and punctuation symbols. 

For example, lowercase i would be represented in the ASCII encoding by binary 1101001 = hexadecimal 69 (i is the ninth letter) = decimal 105.
To get the ascii table type j.ascii

Source: [Website](https://en.wikipedia.org/wiki/ASCII)
    """
    )
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
                colour=thecolor(),
            )
            embed.set_footer(
                text="Type j.help ascii to get information about what the ascii table is. | `,` signifies a new character."
            )
            return await ctx.send(embed=embed)

        z = text.split(" ")
        for c in z:

            for t in c:
                p.append(str(ord(t)))

            x.append(f"\n`{c}: {'-'.join(p)}`")
            p = []
        embed = disnake.Embed(
            title="Ascii:", description=", ".join(x), colour=thecolor()
        )
        embed.set_footer(
            text="Type j.help ascii to get information about what the ascii table is. | '-' signifies a new character."
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["morse_code", "mcode"],
        description="""Encode or decode text/morse code into morse code/plain text, type .morse for help""",
    )
    async def morse(self, ctx: Context, *, string):

        TEXT_TO_MORSE = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            "0": "-----",
            ",": "--..--",
            ".": ".-.-.-",
            "?": "..--..",
            "/": "-..-.",
            "-": "-....-",
            "(": "-.--.",
            ")": "-.--.-",
            ":": "---...",
            "'": ".----.",
            "’": ".----.",
            '"': ".-..-.",
            " ": ".......",
            "!": "-.-.--",
            "@": ".--.-.",
            "$": "...-..-",
            "&": ".-...",
            ";": "-.-.-.",
            "=": "-...-",
            "+": ".-.-.",
            "_": "..--.-",
        }

        MORSE_TO_TEXT = {
            ".-": "A",
            "-...": "B",
            "-.-.": "C",
            "-..": "D",
            ".": "E",
            "..-.": "F",
            "--.": "G",
            "....": "H",
            "..": "I",
            ".---": "J",
            "-.-": "K",
            ".-..": "L",
            "--": "M",
            "-.": "N",
            "---": "O",
            ".--.": "P",
            "--.-": "Q",
            ".-.": "R",
            "...": "S",
            "-": "T",
            "..-": "U",
            "...-": "V",
            ".--": "W",
            "-..-": "X",
            "-.--": "Y",
            "--..": "Z",
            ".----": "1",
            "..---": "2",
            "...--": "3",
            "....-": "4",
            ".....": "5",
            "-....": "6",
            "--...": "7",
            "---..": "8",
            "----.": "9",
            "-----": "0",
            "--..--": ",",
            ".-.-.-": ".",
            "..--..": "?",
            "-..-.": "/",
            "-....-": "-",
            "-.--.": "(",
            "-.--.-": ")",
            "---...": ":",
            ".----.": "'",
            ".-..-.": '"',
            ".......": " ",
            "-.-.--": "!",
            ".--.-.": "@",
            "...-..-": "$",
            ".-...": "&",
            "-.-.-.": ";",
            "-...-": "=",
            ".-.-.": "+",
            "..--.-": "_",
        }

        _tempset = set(string)
        check = True
        for char in _tempset:
            if char not in [".", "-", " "]:
                check = False

        if check is True:
            _templist = str(string).split(" ")
            converted = "".join(MORSE_TO_TEXT[str(i)] for i in _templist)

            await thebed(ctx, "Morse ---> Text", f"```yaml\n{converted}```")
        else:
            _templist = []
            for char in str(string):
                _templist.append(char)
            try:
                converted = " ".join(TEXT_TO_MORSE[str(i).upper()] for i in _templist)
                if len(converted) <= 1998:
                    await thebed(ctx, "Text ---> Morse", f"```yaml\n{converted}```")
                else:

                    y = await Paginator(ctx)
                    await y.paginate(content=converted, name="Morse/Text")
            except KeyError as e:
                return await ctx.reply(
                    f"{CLOSE} The String contains some characters which cannot be converted into Morse!\n> If you think that's a Mistake, please report it to my Developers, they'll Review and fix it :)"
                )

    @commands.command(aliases=["eval2", "e2"], description="run code", hidden=True)
    async def evaldir(self, ctx: Context, *, code):
        x = await run_eval(ctx, code, _eval="dir")

        try:
            await ctx.send(x)
        except:
            pass

    @commands.command(aliases=["eval1", "e1"], description="run code", hidden=True)
    async def evalreturn(self, ctx: Context, *, code):
        x = await run_eval(ctx, code, _eval="return")

        try:
            await ctx.send(x)
        except:
            pass

    @commands.command(description="run code", hidden=True, aliases=["e"])
    async def eval(self, ctx: Context, *, code):
        x = await run_eval(ctx, code)
        try:
            await ctx.send(x)
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

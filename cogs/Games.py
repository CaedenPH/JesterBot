import datetime
import disnake, os, requests, json, asyncio
from disnake.ext.commands import has_permissions
from disnake.ext import commands
from disnake.utils import get
from asyncio import sleep
from random import choice, randint
from core.utils import get_colour, send_embed
from core import Context

import random

HANGMANPICS = [
    "",
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
    """
     
  +---+   _   _  _____   ____   ___  _____  ____  
  |   |  | | | || ____| |  _ \ |_ _|| ____||  _ \ 
  O   |  | |_| ||  _|   | | | | | | |  _|  | | | |
 /|\  |  |  _  || |___  | |_| | | | | |___ | |_| |
 / \  |  |_| |_||_____| |____/ |___||_____||____/ 
      |

=========""",
][::-1]


class Card:
    def __init__(self):
        self.suit = choice(["Hearts ðŸŽ”", "Diamonds â—†", "Clubs â™§", "Spades â™¤"])
        self.num = randint(1, 13)
        self.show = self.num
        if self.num in [1, 11, 12, 13]:
            if self.num == 1:
                self.show = "Ace"
                self.num = 0
            else:
                self.num = 10
                self.show = choice(["King", "Jack", "Queen"])
        self.card = f"{self.show} of {self.suit}"


async def buno(ctx, title, description="", **kwargs):
    theembed = disnake.Embed(title=title, description=description, colour=get_colour())
    theembed.set_author(icon_url=ctx.author.avatar.url, name="Uno")
    author = kwargs.get("a")
    icon_url = kwargs.get("i_u")
    footer = kwargs.get("f")
    thumbnail = kwargs.get("t")
    image = kwargs.get("i")
    if footer:
        theembed.set_footer(text=footer)
    if author:
        theembed.set_author(name=author)
        if icon_url:
            theembed.set_author(name=author, icon_url=icon_url)
    if thumbnail:
        theembed.set_thumbnail(url=thumbnail)
    if image:
        theembed.set_image(url=image)
    await ctx.send(embed=theembed)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def message_content(self, guesses_left, guesses, word):
        return f"```yaml\n{HANGMANPICS[guesses_left]}````{' '.join([k if k in guesses else '_' for k in word])}`\nYou have {guesses_left} guesses left"

    @commands.command(
        aliases=["rr"],
        description="You play russian roulette with yourself - 1 in 6 chance you will die...Be warned!",
    )
    async def russianroulette(self, ctx: Context):
        rand = randint(1, 5)
        if rand == 1:
            embed = disnake.Embed(title="🔫 / You died", colour=get_colour())
            await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(title="🌹 / You lived", colour=get_colour())
            await ctx.send(embed=embed)

    @commands.command(
        aliases=["bj"], description="Emits a game of blackjack with the user"
    )
    async def blackjack(self, ctx: Context):
        one_ace = False
        BotHit = False

        Player_Card_1 = Card()
        Player_Card_2 = Card()

        Oposition_Card_1 = Card()
        Oposition_Card_2 = Card()

        Player_Total = Player_Card_1.num + Player_Card_2.num
        Oposition_Total = Oposition_Card_1.num + Oposition_Card_2.num

        embed = disnake.Embed(
            description=f"**Your cards:** \n{Player_Card_1.card} \n {Player_Card_2.card}\n\n**Type h to hit or s to stand**",
            colour=get_colour(),
        )
        embed.set_author(
            name=f"Blackjack - Score: {Player_Total}", icon_url=ctx.author.avatar.url
        )
        embed.set_footer(text="K, Q, J = 10  |  A = 1 or 11")
        await ctx.send(embed=embed)
        # Opponent ace
        if Oposition_Card_1.num == 0:
            Oposition_Total += 1
        if Oposition_Card_2.num == 0:
            Oposition_Total += 1

        if Oposition_Total < 10:
            Oposition_Card_3 = Card()
            BotHit = True
            Oposition_Total += Oposition_Card_3.num
            if Oposition_Card_1.num == 0 and Oposition_Total != 10:
                Oposition_Total += 1
            else:
                Oposition_Total += 11
            if Oposition_Card_2.num == 0 and Oposition_Total != 10:
                Oposition_Total += 1
            else:
                Oposition_Total += 11

        # ACE

        try:
            received_msg2 = str(
                (
                    await self.bot.wait_for(
                        "message",
                        timeout=90.0,
                        check=lambda m: m.author == ctx.author
                        and m.channel == ctx.channel,
                    )
                ).content
            ).lower()
            while received_msg2 != "s":
                if received_msg2 == "h":
                    Player_Card_3 = Card()
                    if Player_Card_3.num != 0:
                        Player_Total += Player_Card_3.num
                        embed = disnake.Embed(
                            description=f"**Your card:** \n {Player_Card_3.card}",
                            colour=get_colour(),
                        )
                        embed.set_footer(text="Type s to stand or h to hit")
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        await ctx.send(embed=embed)
                        if Player_Total > 21:
                            embed = disnake.Embed(
                                title="You lose because you went over! Restart the game",
                                colour=get_colour(),
                            )
                            embed.set_author(
                                name=f"Blackjack - Score: {Player_Total}",
                                icon_url=ctx.author.avatar.url,
                            )
                            return await ctx.send(embed=embed)

                    else:
                        embed = disnake.Embed(
                            description="You drew an ace, choose 1 or 11 for its value",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        await ctx.send(embed=embed)
                        try:
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
                            if received_msg1 == "1":
                                Player_Total += 1
                                embed = disnake.Embed(
                                    description=f"Type h to hit or s to stand",
                                    colour=get_colour(),
                                )
                                embed.set_author(
                                    name=f"Blackjack - Score: {Player_Total}",
                                    icon_url=ctx.author.avatar.url,
                                )
                            elif received_msg1 == "11":
                                Player_Total += 11
                                embed = disnake.Embed(
                                    description=f"Type h to hit or s to stand",
                                    colour=get_colour(),
                                )
                                embed.set_author(
                                    name=f"Blackjack - Score: {Player_Total}",
                                    icon_url=ctx.author.avatar.url,
                                )
                            else:
                                embed = disnake.Embed(
                                    title="Choose 1 or 11, restart the game",
                                    colour=get_colour(),
                                )
                            embed = disnake.Embed(
                                description=f"Type h to hit or s to stand",
                                colour=get_colour(),
                            )
                            embed.set_author(
                                name=f"Blackjack - Score: {Player_Total}",
                                icon_url=ctx.author.avatar.url,
                            )
                        except asyncio.TimeoutError:
                            embed = disnake.Embed(
                                title="I gave up waiting", colour=get_colour()
                            )
                            return await ctx.send(embed=embed)

                else:
                    embed = disnake.Embed(
                        title="Incorrect answer, restart the game", colour=get_colour()
                    )
                    return await ctx.send(embed=embed)

                received_msg2 = str(
                    (
                        await self.bot.wait_for(
                            "message",
                            timeout=90.0,
                            check=lambda m: m.author == ctx.author
                            and m.channel == ctx.channel,
                        )
                    ).content
                ).lower()
            else:
                if Player_Card_1.num == 0:
                    embed = disnake.Embed(
                        description="You have an ace, choose 1 or 11 for its value",
                        colour=get_colour(),
                    )
                    embed.set_author(name="Blackjack", icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                    one_ace = True
                    try:
                        received_msg = str(
                            (
                                await self.bot.wait_for(
                                    "message",
                                    timeout=90.0,
                                    check=lambda m: m.author == ctx.author
                                    and m.channel == ctx.channel,
                                )
                            ).content
                        ).lower()
                        if Player_Card_2.num != 0:
                            if received_msg == "1":
                                Player_Total += 1

                            elif received_msg == "11":
                                Player_Total += 11

                            else:
                                embed = disnake.Embed(
                                    title="Choose 1 or 11, restart the game",
                                    colour=get_colour(),
                                )
                                return await ctx.send(embed=embed)
                        else:
                            if received_msg == "1":
                                Player_Total += 1
                            elif received_msg == "11":
                                Player_Total += 11
                            else:
                                embed = disnake.Embed(
                                    title="Choose 1 or 11, restart the game",
                                    colour=get_colour(),
                                )
                                return await ctx.send(embed=embed)

                        await ctx.send(embed=embed)
                    except asyncio.TimeoutError:
                        embed = disnake.Embed(
                            title="I gave up waiting", colour=get_colour()
                        )
                        await ctx.send(embed=embed)
                        return await ctx.send(embed=embed)

                if Player_Card_2.num == 0:
                    if one_ace:

                        embed = disnake.Embed(
                            description="You have an ace, choose 1 or 11 for its value",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        await ctx.send(embed=embed)
                        try:
                            received_msg = str(
                                (
                                    await self.bot.wait_for(
                                        "message",
                                        timeout=90.0,
                                        check=lambda m: m.author == ctx.author
                                        and m.channel == ctx.channel,
                                    )
                                ).content
                            ).lower()
                            if received_msg == "1":
                                Player_Total += 1

                            elif received_msg == "11":
                                Player_Total += 11

                            else:
                                embed = disnake.Embed(
                                    title="Choose 1 or 11, restart the game",
                                    colour=get_colour(),
                                )
                                return await ctx.send(embed=embed)
                            await ctx.send(embed=embed)
                        except asyncio.TimeoutError:
                            embed = disnake.Embed(
                                title="I gave up waiting", colour=get_colour()
                            )
                            return await ctx.send(embed=embed)

                    else:
                        embed = disnake.Embed(
                            description="You have an ace, choose 1 or 11 for its value",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        await ctx.send(embed=embed)
                        try:
                            received_msg = str(
                                (
                                    await self.bot.wait_for(
                                        "message",
                                        timeout=90.0,
                                        check=lambda m: m.author == ctx.author
                                        and m.channel == ctx.channel,
                                    )
                                ).content
                            ).lower()
                            if received_msg == "1":
                                Player_Total += 1

                            elif received_msg == "11":
                                Player_Total += 11

                            else:
                                embed = disnake.Embed(
                                    title="Choose 1 or 11, restart the game",
                                    colour=get_colour(),
                                )
                                return await ctx.send(embed=embed)
                            await ctx.send(embed=embed)

                        except asyncio.TimeoutError:
                            embed = disnake.Embed(
                                title="I gave up waiting", colour=get_colour()
                            )
                            return await ctx.send(embed=embed)

                if Player_Total > 21:
                    embed = disnake.Embed(
                        title="You went over 21!", colour=get_colour()
                    )
                    return await ctx.send(embed=embed)
                if BotHit:
                    if Player_Total > Oposition_Total:
                        embed = disnake.Embed(
                            title="You won against the opposition!",
                            description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        return await ctx.send(embed=embed)

                    elif Player_Total < Oposition_Total:
                        embed = disnake.Embed(
                            title="You lost to the opposition!",
                            description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        return await ctx.send(embed=embed)
                    else:
                        embed = disnake.Embed(
                            titlen="You drew with the opposition!",
                            description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        return await ctx.send(embed=embed)

                else:

                    if Player_Total > Oposition_Total:
                        embed = disnake.Embed(
                            title="You won against the opposition!",
                            description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        return await ctx.send(embed=embed)

                    elif Player_Total < Oposition_Total:
                        embed = disnake.Embed(
                            title="You lost to the opposition!",
                            description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        return await ctx.send(embed=embed)
                    else:
                        embed = disnake.Embed(
                            titlen="You drew with the opposition!",
                            description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**",
                            colour=get_colour(),
                        )
                        embed.set_author(
                            name=f"Blackjack - Score: {Player_Total}",
                            icon_url=ctx.author.avatar.url,
                        )
                        return await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            embed = disnake.Embed(title="I gave up waiting", colour=get_colour())
            return await ctx.send(embed=embed)

    @commands.command(
        aliases=["dices", "die"],
        description="Rolls a dice and compares the number to `<roll>`, difficulty can be; easiest (1 in 2 chance), easy (1 in 3 chance), normal (1 in 6 chance), hard (1 in 9 chance), impossible (1 in 15 chance)",
    )
    async def dice(self, ctx: Context, num, difficulty="normal"):
        try:

            num = int(num)
        except Exception as e:
            return await send_embed(ctx, "That is not an integer!")

        async def ea():

            rollrig = ["1", "2", "3", "4", "5", "6"]
            rand = randint(1, 2)
            rollrigy = choice(rollrig)

            async def displaycorrect():
                nonlocal rollrigy

                if num != int(rollrigy):
                    rollrig = [str(num)]
                embed = disnake.Embed(
                    title=f"Good guess! The roll was {rollrig[0]}", colour=get_colour()
                )
                await ctx.send(embed=embed)

            async def displaywrong():
                nonlocal rollrigy, rollrig

                if int(rollrigy) == num:
                    rollrig.remove(str(num))

                    rollrigy = choice(rollrig)
                    embed = disnake.Embed(
                        title=f"Your guess was incorrect, the roll was {rollrigy}",
                        colour=get_colour(),
                    )
                    await ctx.send(embed=embed)

            if num == 1:
                if rand == 1:
                    await displaycorrect()

                elif rand != 1:
                    await displaywrong()

            if num == 2:
                if rand == 1:
                    await displaycorrect()
                elif rand != 1:
                    await displaywrong()
            if num == 3:
                if rand == 1:
                    await displaycorrect()
                elif rand != 1:
                    await displaywrong()

            if num == 4:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()

            if num == 5:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()

            if num == 6:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()

        async def easy():
            rollrig = ["1", "2", "3", "4", "5", "6"]
            rand = randint(1, 3)
            rollrigy = choice(rollrig)

            async def displaycorrect():
                nonlocal rollrigy

                if num != int(rollrigy):
                    rollrig = [str(num)]
                embed = disnake.Embed(
                    title=f"Good guess! The roll was {rollrig[0]}", colour=get_colour()
                )
                await ctx.send(embed=embed)

            async def displaywrong():
                nonlocal rollrigy

                if int(rollrigy) == num:
                    rollrig.remove(str(num))

                    rollrigy = choice(rollrig)
                embed = disnake.Embed(
                    title=f"Your guess was incorrect, the roll was {rollrigy}",
                    colour=get_colour(),
                )
                await ctx.send(embed=embed)

            if num == 1:
                if rand == 1:
                    await displaycorrect()

                elif rand != 1:
                    await displaywrong()

            if num == 2:
                if rand == 1:
                    await displaycorrect()
                elif rand != 1:
                    await displaywrong()
            if num == 3:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()

            if num == 4:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()
            if num == 5:
                if rand == 3:
                    await displaycorrect()
                elif rand != 3:
                    await displaywrong()
            if num == 6:
                if rand == 3:
                    await displaycorrect()

                elif rand != 3:
                    await displaywrong()

        async def normal():
            rand = randint(1, 6)
            rollrig = ["1", "2", "3", "4", "5", "6"]
            rollrigy = choice(rollrig)

            if int(rollrigy) == num:
                rollrig.remove(str(num))
                rollrigy = choice(rollrig)
            if rand == num:
                embed = disnake.Embed(
                    title=f"Good guess! The roll was {rollrig[0]}", colour=get_colour()
                )
                await ctx.send(embed=embed)

            elif rand != num:
                embed = disnake.Embed(
                    title=f"Your guess was incorrect, the roll was {rollrigy}",
                    colour=get_colour(),
                )
                await ctx.send(embed=embed)

        async def hard():
            rand = randint(1, 9)
            rollrig = ["1", "2", "3", "4", "5", "6"]
            rollrigy = choice(rollrig)

            if int(rollrigy) == num:
                rollrig.remove(str(num))
                print(rollrig)
            if rand == num:
                embed = disnake.Embed(
                    title=f"Good guess! The roll was {rollrig[0]}", colour=get_colour()
                )
                await ctx.send(embed=embed)

            elif rand != num:
                embed = disnake.Embed(
                    title=f"Your guess was incorrect, the roll was {rollrigy}",
                    colour=get_colour(),
                )
                await ctx.send(embed=embed)

        async def impossible():
            rand = randint(1, 20)
            rollrig = ["1", "2", "3", "4", "5", "6"]
            rollrigy = choice(rollrig)

            if int(rollrigy) == num:
                rollrig.remove(str(num))
                print(rollrig)
            if rand == num:
                embed = disnake.Embed(
                    title=f"Good guess! The roll was {rollrig[0]}", colour=get_colour()
                )
                await ctx.send(embed=embed)

            elif rand != num:
                embed = disnake.Embed(
                    title=f"Your guess was incorrect, the roll was {rollrigy}",
                    colour=get_colour(),
                )
                await ctx.send(embed=embed)

        if difficulty == "normal":
            await normal()

        elif difficulty == "hard":
            await hard()

        elif difficulty == "easy":
            await easy()

        elif difficulty == "impossible":
            await impossible()

        elif difficulty == "easiest":
            await ea()

    @commands.command(
        aliases=["rock", "rockpaperscissors"],
        description="Plays rock paper scissors with the bot `<choice>` must be rock, paper, or scissors",
    )
    async def rps(self, ctx: Context, roll):

        random_num = randint(0, 2)

        if roll not in ["rock", "paper", "scissors"]:
            embed = disnake.Embed(
                title="Thats not an option. Choose rock, paper, or scissors...",
                colour=get_colour(),
            )
            await ctx.send(embed=embed)

        if random_num == 0:
            cpu_choice = "rock"

        elif random_num == 1:
            cpu_choice = "paper"
        elif random_num == 2:
            cpu_choice = "scissors"

        if roll == "rock":
            if cpu_choice == "rock":
                embed = disnake.Embed(
                    title="You drew",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you drew",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")

                await ctx.send(embed=embed)
            elif cpu_choice == "paper":
                embed = disnake.Embed(
                    title="You lost",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you lost",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)

            elif cpu_choice == "scissors":
                embed = disnake.Embed(
                    title="You won",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you won",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)

        if roll == "paper":
            if cpu_choice == "paper":
                embed = disnake.Embed(
                    title="Drew",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you drew",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")

                await ctx.send(embed=embed)

            elif cpu_choice == "scissors":
                embed = disnake.Embed(
                    title="You lost",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you lost",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")

                await ctx.send(embed=embed)

            elif cpu_choice == "rock":
                embed = disnake.Embed(
                    title="You won",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you won",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)

        if roll == "scissors":
            if cpu_choice == "scissors":
                embed = disnake.Embed(
                    title="You drew",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you drew",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)
            elif cpu_choice == "rock":
                embed = disnake.Embed(
                    title="You lost",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you lost",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")

                await ctx.send(embed=embed)

            elif cpu_choice == "paper":
                embed = disnake.Embed(
                    title="You won",
                    description=f"You picked {roll}, bot picked {cpu_choice}, therefore you won",
                    colour=get_colour(),
                )
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)

    @commands.command(
        aliases=["rpsbait", "rpsbaits", "RPSB", "RockPaperScissorsBait"],
        description="Emits a fake rock paper scissors game with a bot",
    )
    async def rpsfail(self, ctx: Context):
        embed = disnake.Embed(title=f"Rock paper scissors!", colour=get_colour())
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("\U0001f4bf")
        await msg.add_reaction("\U0001f4f0")
        await msg.add_reaction("\U00002702")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "\U0001f4bf"

        reaction, user = await self.bot.wait_for("reaction_add", check=check)
        await msg.delete()
        embed = disnake.Embed(title=f"Baited", colour=get_colour())
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["gussing", "Guessing", "Guessing_game", "gg"],
        description="Plays a guessinggame with the bot (bot thinks of a number)",
    )
    async def guessinggame(self, ctx: Context):
        rand = randint(1, 100)
        embed = disnake.Embed(
            title=f"Give me a number between 1-100, the game has started'",
            colour=get_colour(),
        )
        await ctx.send(embed=embed)

        try:
            received_msg = int(
                (
                    await self.bot.wait_for(
                        "message",
                        check=lambda m: m.author == ctx.author
                        and m.channel == ctx.channel,
                        timeout=10,
                    )
                ).content
            )
            while received_msg != rand:

                if received_msg > rand:
                    embed = disnake.Embed(title="Lower", colour=get_colour())
                    await ctx.send(embed=embed)

                elif received_msg < rand:
                    embed = disnake.Embed(title="Higher", colour=get_colour())
                    await ctx.send(embed=embed)
                elif str(received_msg) == "q":
                    embed = disnake.Embed(title="Goodbye", colour=get_colour())
                    return await ctx.send(embed=embed)
                received_msg = int(
                    (
                        await self.bot.wait_for(
                            "message",
                            check=lambda m: m.author == ctx.author
                            and m.channel == ctx.channel,
                            timeout=10,
                        )
                    ).content
                )
            else:
                embed = disnake.Embed(
                    title=f"Correct! The answer was {rand}", colour=get_colour()
                )
                return await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            embed = disnake.Embed(title="I gave up waiting", colour=get_colour())
            await ctx.send(embed=embed)

    @commands.command()
    async def anagram(self, ctx: Context) -> None:
        with open("./resources/anagram.json") as stream:
            data = json.load(stream)

        choice = random.choice(list(data.keys()))
        print(data[choice])
        embed = (
            disnake.Embed(
                title=f"Your anagram is {choice}",
                description=f"There are {len(data[choice])} answers. You have 60 seconds to respond with your answers. The answers are all the same length as the word",
            )
            .set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            .set_footer(
                text=f"Out of {len(list(data.keys()))} options! ps these are all completely real words that are allowed on scrabble"
            )
        )
        await ctx.send(embed=embed)

        responses = []
        time = datetime.datetime.utcnow()
        try:
            while msg := await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                timeout=60 - (datetime.datetime.utcnow() - time).total_seconds(),
            ):
                responses.append(msg.content)

                if len(responses) == len(data[choice]):
                    raise asyncio.TimeoutError()

        except asyncio.TimeoutError:
            embed = disnake.Embed(
                title=f"Anagram for {choice}",
                description=f"The answers were: `{', '.join(data[choice])}`",
            ).set_author(name="Nice try!", icon_url=ctx.author.avatar.url)

            if responses != data[choice]:
                return await ctx.send(embed=embed)
            await ctx.em("Wow you got all the anagrams!")

    @commands.command()
    async def hangman(self, ctx: Context) -> None:
        with open("./resources/hangman_words.txt") as txt:
            words = txt.readlines()

        word = random.choice(words).strip()
        WORD_WAS = f"The word was `{word}`"

        guesses = []
        guesses_left = 7

        msg = await ctx.send(self.message_content(guesses_left, guesses, word))
        try:
            while m := await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                timeout=60,
            ):
                """
                5 Conditions in order;
                    a) content == q; exit
                    b) content == word; win
                    c) all letters guessed are in word; win
                    d) guesses_left == 1; loss
                    e) content > 1 letter; punt
                then;
                    if content not in guesses;
                        if content not in word;
                            guesses_left -= 1
                        then;
                        -> edit(...)
                """

                content = m.content.lower()
                guesses.append(content)

                if content == "q":
                    return await ctx.em(f"Game ended. {WORD_WAS}")
                if content == word:
                    return await ctx.em(f"That is the word! {WORD_WAS}")
                if all([w in guesses for w in list(word)]):
                    return await ctx.em(f"Well done! You got the word. {WORD_WAS}")
                if guesses_left == 1:
                    return await ctx.em(f"Unlucky, you ran out of guesses! {WORD_WAS}")
                if len(content) >= 2:
                    await ctx.em(
                        f"`{content}` is not the word! Try sending letters one at a time"
                    )

                if content not in guesses[:-1]:
                    if content not in word:
                        guesses_left -= 1

                await msg.edit(
                    content=self.message_content(guesses_left, guesses, word)
                )

        except asyncio.TimeoutError:
            await ctx.em("You ran out of time!")


def setup(bot):
    bot.add_cog(Games(bot))

import datetime
import disnake
import os
import requests
import json
import asyncio
import random

from disnake.ext.commands import has_permissions, command
from core.utils import get_colour, send_embed
from core import Context
from core.constants import HANGMAN

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


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def message_content(self, guesses_left, guesses, word):
        return f"```yaml\n{HANGMAN[guesses_left]}````{' '.join([k if k in guesses else '_' for k in word])}`\nYou have {guesses_left} guesses left"

    @commands.command(
        aliases=["rr"],
        description="You play russian roulette with yourself - 1 in 6 chance you will die...Be warned!",
    )
    async def russianroulette(self, ctx: Context):
        rand = randint(1, 6)
        if rand == 1:
            return await send_embed("🔫 / You died")
        await send_embed("🌹 / You lived")

    @command(
        aliases=["bj"], description="Emits a game of blackjack with the user"
    )
    async def blackjack(self, ctx: Context):
        await send_embed("Working...")

    @command(
        aliases=["dices", "die"],
        description="Rolls a dice and compares the number to `<roll>`, difficulty can be; easiest (1 in 2 chance), easy (1 in 3 chance), normal (1 in 6 chance), hard (1 in 9 chance), impossible (1 in 15 chance)",
    )
    async def dice(self, ctx: Context, num, difficulty="normal"):
        await send_embed("Working...")

    @command(
        aliases=["rock", "rockpaperscissors"],
        description="Plays rock paper scissors with the bot `<choice>` must be rock, paper, or scissors",
    )
    async def rps(self, ctx: Context, roll):
        await send_embed("Working...")

    @command(
        aliases=["rpsbait", "rpsbaits", "RPSB", "RockPaperScissorsBait"],
        description="Emits a fake rock paper scissors game with a bot",
    )
    async def rpsfail(self, ctx: Context):
        msg = await send_embed("Rock, paper, scissors!")
        await msg.add_reaction("\U0001f4bf")
        await msg.add_reaction("\U0001f4f0")
        await msg.add_reaction("\U00002702")

        def check(reaction, user):
            return user == ctx.author
        reaction, user = await self.bot.wait_for("reaction_add", check=check)

        embed = disnake.Embed(title=f"Baited", colour=get_colour())
        await msg.edit(embed=embed)

    @command(
        aliases=["gussing", "Guessing", "Guessing_game", "gg"],
        description="Plays a guessinggame with the bot (bot thinks of a number)",
    )
    async def guessinggame(self, ctx: Context):
        number = randint(1, 100)
        await send_embed("Guess a number between 1-100")

        try:
            while (message:=await self.bot.wait_for("message")):
                if message.content == "q":
                    return await send_embed("Game ended")
                if message.content.isalpha():
                    await send_embed("Send an integer between 1-100")

                guess = int(message.content)
                if guess > rand:
                    await send_embed("Lower")
                elif guess < rand:
                    await send_embed("Higher")
                elif guess == number:
                    return await send_embed(f"Well done! The number was {number}")

        except asyncio.TimeoutError:
            await send_embed("Game timed out")

    @command()
    async def anagram(self, ctx: Context) -> None:
        with open("./resources/anagram.json") as stream:
            data = json.load(stream)

        choice = random.choice(list(data.keys()))
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

    @command()
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

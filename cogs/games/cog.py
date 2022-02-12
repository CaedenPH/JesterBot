import datetime
import disnake
import json
import asyncio

from disnake.ext.commands import command, Cog
from random import randint, choice

from core.utils import get_colour, send_embed
from core import Context
from core.constants import HANGMAN, BLACKJACK_WELCOME
from .blackjack import BlackJack



class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    def message_content(self, guesses_left, guesses, word):
        return f"```yaml\n{HANGMAN[guesses_left]}````{' '.join([k if k in guesses else '_' for k in word])}`\nYou have {guesses_left} guesses left"
    
    @command(
        aliases=["rr"],
        description="You play russian roulette with yourself - 1 in 6 chance you will die...Be warned!",
    )
    async def russianroulette(self, ctx: Context):
        rand = randint(1, 6)
        if rand == 1:
            return await send_embed(ctx, "🔫 / You died")
        await send_embed(ctx, "🌹 / You lived")

    @command(aliases=["bj"], description="Emits a game of blackjack with the user")
    async def blackjack(self, ctx: Context):
        embed = disnake.Embed(
            title="Blackjack",
            description=BLACKJACK_WELCOME, 
            timestamp=ctx.message.created_at
        ).set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar.url
        )
        view = BlackJack(ctx)
        view.bot_message = await ctx.send(
            embed=embed,
            view=view
        )

    @command(
        aliases=["dices", "die"],
        description="Rolls a dice and compares the number to `<roll>`, difficulty can be; easiest (1 in 2 chance), easy (1 in 3 chance), normal (1 in 6 chance), hard (1 in 9 chance), impossible (1 in 15 chance)",
    )
    async def dice(self, ctx: Context, num: str, difficulty: str = "normal"):
        await send_embed(ctx, "Working...")

    @command(
        aliases=["rock", "rockpaperscissors"],
        description="Plays rock paper scissors with the bot `<choice>` must be rock, paper, or scissors",
    )
    async def rps(self, ctx: Context, roll: str):
        moves = {
            'rock': {
                'scissors': 'won', 'paper': 'lost'
                },
            'scissors': {
                'paper': 'won', 'rock': 'lost'
                }
            ,
            'paper': {
                'rock': 'won', 'scissors': 'lost'
                }
        }

        if roll not in moves:
            return await send_embed(
                ctx, "", "Choose a move out of `rock`, `paper`, `scissors`"
            )

        computer_choice = choice(list(moves.keys()))
        await send_embed(
            ctx, "Rock paper scissors", f"You **{moves[roll][computer_choice] if roll != computer_choice else 'drew'}** against the bot! You chose {roll} and the bot chose {computer_choice}"
        )
        
    @command(
        aliases=["rpsbait", "rpsbaits", "RPSB", "RockPaperScissorsBait"],
        description="Emits a fake rock paper scissors game with a bot",
    )
    async def rpsfail(self, ctx: Context):
        msg = await send_embed(ctx, "Rock, paper, scissors!")
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
        await send_embed(ctx, "Guess a number between 1-100")

        try:
            while message := await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            ):
                if message.content == "q":
                    return await send_embed(ctx, "Game ended")
                if message.content.isalpha():
                    await send_embed(ctx, "Send an integer between 1-100")
                    continue

                guess = int(message.content)
                if guess > number:
                    await send_embed(ctx, "Lower")
                elif guess < number:
                    await send_embed(ctx, "Higher")
                elif guess == number:
                    return await send_embed(ctx, f"Well done! The number was {number}")
        except asyncio.TimeoutError:
            await send_embed(ctx, "Game timed out")

    @command()
    async def anagram(self, ctx: Context) -> None:
        with open("./resources/anagram.json") as stream:
            data = json.load(stream)

        anagram = choice(list(data.keys()))
        embed = (
            disnake.Embed(
                title=f"Your anagram is {anagram}",
                description=f"There are {len(data[anagram])} answers. You have 60 seconds to respond with your answers. The answers are all the same length as the word",
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

                if len(responses) == len(data[anagram]):
                    raise asyncio.TimeoutError()

        except asyncio.TimeoutError:
            embed = disnake.Embed(
                title=f"Anagram for {anagram}",
                description=f"The answers were: `{', '.join(data[anagram])}`",
            ).set_author(name="Nice try!", icon_url=ctx.author.avatar.url)

            if responses != data[anagram]:
                return await ctx.send(embed=embed)
            await ctx.em("Wow you got all the anagrams!")

    @command()
    async def hangman(self, ctx: Context) -> None:
        with open("./resources/hangman_words.txt") as txt:
            words = txt.readlines()

        word = choice(words).strip()
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

                if content == "quit":
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

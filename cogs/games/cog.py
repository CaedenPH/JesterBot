import datetime
import json
import asyncio

from disnake import Embed
from disnake.ext.commands import command, Cog
from random import randint, choice

from core.utils import get_colour, send_embed
from core import Context
from core.constants import (
    HANGMAN,
    BLACKJACK_WELCOME,
    MINESWEEPER_MESSAGE,
    SNAKE_MESSAGE,
    SUDOKU_MESSAGE,
    WORDLE_MESSAGE,
)
from . import BlackJack, Casino, RussianRoulette, Dice, MineSweeper, Snake, Sudoku, Wordle


class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    def message_content(self, guesses_left, guesses, word):
        return f"```yaml\n{HANGMAN[guesses_left]}````{' '.join([k if k in guesses else '_' for k in word])}`\nYou have {guesses_left} guesses left"

    @command()
    async def wordle(self, ctx: Context) -> None:
        embed = Embed(
            title="Wordle",
            description="```yaml\n" + WORDLE_MESSAGE.format(word_length=5, light_mode=False) + "```",
            colour=get_colour(),
            timestamp=ctx.message.created_at,
        ).set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)

        view = Wordle(ctx)
        view.bot_message = await ctx.reply(embed=embed, view=view)

    @command(aliases=["so", "su"])
    async def sudoku(self, ctx: Context) -> None:
        embed = Embed(
            title="sudoku",
            description="```yaml\n" + SUDOKU_MESSAGE.format(light_mode=False, difficulty="medium") + "```",
            colour=get_colour(),
            timestamp=ctx.message.created_at,
        ).set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)

        view = Sudoku(ctx)
        view.bot_message = await ctx.reply(embed=embed, view=view)

    @command(aliases=["snek"])
    async def snake(self, ctx: Context) -> None:
        embed = Embed(
            title="Snake",
            description="```yaml\n" + SNAKE_MESSAGE.format(board_size=5, game_mode="normal") + "```",
            colour=get_colour(),
            timestamp=ctx.message.created_at,
        ).set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)

        view = Snake(ctx)
        view.bot_message = await ctx.reply(embed=embed, view=view)

    @command(aliases=["mine"])
    async def minesweeper(self, ctx: Context) -> None:
        embed = Embed(
            title="Mine Sweeper",
            description=MINESWEEPER_MESSAGE.format(board_size=5, bomb_count=5),
            colour=get_colour(),
            timestamp=ctx.message.created_at,
        ).set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)

        view = MineSweeper(ctx)
        view.bot_message = await ctx.reply(embed=embed, view=view)

    @command()
    async def casino(self, ctx: Context) -> None:
        embed = Embed(title="Casino Machine $", description="```000```", colour=get_colour()).set_footer(
            text="Get Three numbers in a row for a PRIZE"
        )

        await ctx.reply(embed=embed, view=Casino(ctx.author))

    @command(aliases=["rr", "gun_game", "russianroulette", "gungame"])
    async def russian_roulette(self, ctx: Context):
        embed = Embed(title="Russian Roulette", colour=get_colour()).set_footer(text="Dont die!")

        await ctx.reply(embed=embed, view=RussianRoulette(ctx))

    @command(aliases=["die"])
    async def dice(self, ctx: Context):
        embed = Embed(
            title="<:dicetitle:932727881069641858> Play now <:dicetitle:932727881069641858>",
            description="Your random roll awaits",
            colour=get_colour(),
        )

        await ctx.reply(embed=embed, view=Dice(ctx))

    @command(aliases=["bj"])
    async def blackjack(self, ctx: Context):
        embed = Embed(
            title="Blackjack", description=BLACKJACK_WELCOME, timestamp=ctx.message.created_at, colour=get_colour()
        ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        view = BlackJack(ctx)
        view.bot_message = await ctx.reply(embed=embed, view=view)

    @command(
        aliases=["rock", "rockpaperscissors"],
        description="Plays rock paper scissors with the bot `<choice>` must be rock, paper, or scissors",
    )
    async def rps(self, ctx: Context, roll: str):
        moves = {
            "rock": {"scissors": "won", "paper": "lost"},
            "scissors": {"paper": "won", "rock": "lost"},
            "paper": {"rock": "won", "scissors": "lost"},
        }

        if roll not in moves:
            return await send_embed(ctx, "", "Choose a move out of `rock`, `paper`, `scissors`")

        computer_choice = choice(list(moves.keys()))
        await send_embed(
            ctx,
            "Rock paper scissors",
            f"You **{moves[roll][computer_choice] if roll != computer_choice else 'drew'}** against the bot! You chose {roll} and the bot chose {computer_choice}",
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

        (reaction, user) = await self.bot.wait_for("reaction_add", check=check)

        embed = Embed(title=f"Baited", colour=get_colour())
        await msg.edit(embed=embed)

    @command(
        aliases=["gussing", "Guessing", "Guessing_game", "gg"],
        description="Plays a guessinggame with the bot (bot thinks of a number)",
    )
    async def guessinggame(self, ctx: Context):
        number = randint(1, 100)
        await send_embed(ctx, "Guess a number between 1-100")

        try:
            while message := await self.bot.wait_for("message", check=lambda m: m.author == ctx.author):
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
            Embed(
                title=f"Your anagram is {anagram}",
                description=f"There are {len(data[anagram])} answers. You have 60 seconds to respond with your answers. The answers are all the same length as the word",
            )
            .set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            .set_footer(
                text=f"Out of {len(list(data.keys()))} options! ps these are all completely real words that are allowed on scrabble"
            )
        )
        await ctx.reply(embed=embed)

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
            embed = Embed(
                title=f"Anagram for {anagram}", description=f"The answers were: `{', '.join(data[anagram])}`"
            ).set_author(name="Nice try!", icon_url=ctx.author.avatar.url)

            if responses != data[anagram]:
                return await ctx.reply(embed=embed)
            await ctx.em("Wow you got all the anagrams!")

    @command()
    async def hangman(self, ctx: Context) -> None:
        with open("./resources/hangman_words.txt") as txt:
            words = txt.readlines()

        word = choice(words).strip()
        WORD_WAS = f"The word was `{word}`"
        guesses = []
        guesses_left = 7

        msg = await ctx.reply(self.message_content(guesses_left, guesses, word))
        try:
            while m := await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60
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
                    await ctx.em(f"`{content}` is not the word! Try sending letters one at a time")

                if content not in guesses[:-1]:
                    if content not in word:
                        guesses_left -= 1

                await msg.edit(content=self.message_content(guesses_left, guesses, word))

        except asyncio.TimeoutError:
            await ctx.em("You ran out of time!")


def setup(bot):
    bot.add_cog(Games(bot))

from __future__ import annotations

import asyncio
import random
import typing as t

from disnake import HTTPException, MessageInteraction, Message, ButtonStyle, SelectOption
from disnake.ui import View, Button, Select, Item, select, button

from core import Context
from core.constants import (
    BLACK_SQUARE,
    RED_LETTERS,
    GREEN_LETTERS,
    PLAY_BUTTON,
    STOP_SIGN,
    VIDEO_GAME,
    WHITE_SQUARE,
    WORDLE_MESSAGE,
)


class square:
    revealed: bool
    light_mode: bool
    final_word: str
    letter: t.Optional[str]
    word: t.Optional[str]

    @classmethod
    def empty(cls, light_mode: bool, final_word: str) -> square:
        self = cls()
        self.light_mode = light_mode
        self.final_word = final_word
        self.revealed = False
        self.letter = None
        self.word = None
        return self

    def set_letter(self, letter: str, word: str) -> None:
        self.letter = letter.lower()
        self.word = word.lower()

    def __str__(self) -> str:
        if not self.letter:
            return WHITE_SQUARE if self.light_mode else BLACK_SQUARE

        if self.letter not in self.final_word:
            return f":regional_indicator_{self.letter}:"

        final_word, word = list(self.final_word), list(self.word)
        if final_word.index(self.letter) == word.index(self.letter):
            return GREEN_LETTERS[self.letter]
        return RED_LETTERS[self.letter]


class _WordleView(View):
    bot_message: Message

    def message_check(self, m: Message) -> bool:
        return m.author == self.ctx.author and m.channel == self.ctx.channel

    async def on_timeout(self) -> None:
        await self.stop()

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        return interaction.author == self.ctx.author and interaction.channel == self.ctx.channel

    async def stop(self) -> None:
        self.children = []
        await self.edit_embed()

    async def delete_message(self, message: Message) -> None:
        await asyncio.sleep(10)
        try:
            await message.delete()
        except HTTPException:
            pass

    async def edit_embed(self, desc: t.Optional[str] = None) -> None:
        """
        edit the bot message by
        changing description and
        view.

        params
        ------
        `desc: t.Optional[str]`
            the description to set to
            the embed, if None just change
            the message view.
        """

        embed = self.bot_message.embeds[0]
        if desc:
            embed.description = desc
        await self.bot_message.edit(embed=embed, view=self)

    @select(
        placeholder=f"Colour settings {BLACK_SQUARE}",
        options=[SelectOption(label="Light mode"), SelectOption(label="Dark mode")],
    )
    async def change_colour_settings(self, select: Select, interaction: MessageInteraction) -> None:
        """
        user selects whether or not
        they want dark mode or light
        mode (aka white squares or
        black squares.)

        params
        ------
        select: Select
            the select option that was
            chosen by the user.
        interaction: MessageInteraction
            the interaction instance that
            was returned by the discord api.
        """

        self.light_mode = select.values[0].startswith("Light")
        await interaction.response.defer()
        await self.edit_embed(
            "```yaml\n" + WORDLE_MESSAGE.format(word_length=self.word_length, light_mode=self.light_mode) + "```"
        )

    @select(
        placeholder=f"Change word length {VIDEO_GAME}",
        options=[SelectOption(label="4"), SelectOption(label="5"), SelectOption(label="6"), SelectOption(label="7")],
    )
    async def change_word_length(self, select: Select, interaction: MessageInteraction) -> None:
        """
        user changes the word length
        to either 4, 5, 6 or 7.

        params
        ------
        select: Select
            the select option that was
            chosen by the user.
        interaction: MessageInteraction
            the interaction instance that
            was returned by the discord api.
        """

        self.word_length = int(select.values[0])
        await interaction.response.defer()
        await self.edit_embed(
            "```yaml\n" + WORDLE_MESSAGE.format(word_length=self.word_length, light_mode=self.light_mode) + "```"
        )


class Wordle(_WordleView):
    """
    represents the main wordle
    game including board and
    board-related functions.

    attributes
    ----------
    `bot_message: Message`
        the original message that
        the bot sent. Used to edit.
    """

    def __init__(self, ctx: Context) -> None:
        super().__init__(timeout=720)

        self.ctx = ctx
        self.word_length = 5
        self.light_mode = False
        self.guesses = 0

    def format_board(self) -> str:
        board_string = ""
        for row in range(6):
            for square in range(self.word_length):
                board_string += str(self.board[row][square])
            board_string += "\n"
        return board_string

    @button(label="Guess", style=ButtonStyle.green, emoji=STOP_SIGN, disabled=True)
    async def guess(self, button: Button, interaction: MessageInteraction) -> None:
        """
        user guesses a word which is
        appended to the board and is
        show visually as to which
        letters are or are not in the
        correct spot.

        params
        ------
        button: Button
            the button that was pressed
            by the user.
        interaction: MessageInteraction
            the interaction instance that
            was returned by the discord api.
        """

        await interaction.response.send_message(f"Send a valid `{self.word_length}` letter long word", delete_after=10)

        while True:
            message = await self.ctx.bot.wait_for("message", timeout=720, check=self.message_check)
            await self.delete_message(message)

            if len(message.content) != self.word_length:
                return await message.reply(f"You must send a `{self.word_length}` letter long word", delete_after=10)

            async with self.ctx.bot.client.get(
                url=f"https://wordsapiv1.p.rapidapi.com/words/{message.content}/syllables",
                headers={"x-rapidapi-host": "wordsapiv1.p.rapidapi.com", "x-rapidapi-key": self.ctx.bot.RAPID_API_KEY},
            ) as response:
                json = await response.json()

            if "message" in json:
                return await message.reply("You must send a valid english word!", delete_after=10)

            word = list(message.content)
            for i in range(self.word_length):
                self.board[self.guesses][i].set_letter(word[i], message.content)
            self.guesses += 1

            await self.edit_embed(self.format_board())
            if message.content == self.word:
                return await message.reply("You won!")
            if self.guesses == 6:
                return await message.reply("You lose!")

    @button(label="Play", style=ButtonStyle.green, emoji=PLAY_BUTTON)
    async def play(self, button: Button, interaction: MessageInteraction) -> None:
        """
        user presses the play button
        to initiate the game stage and
        remove configuration buttons
        from the board.

        params
        ------
        button: Button
            the button that was pressed
            by the user.
        interaction: MessageInteraction
            the interaction instance that
            was returned by the discord api.
        """

        with open("./resources/hangman_words.txt") as f:
            self.word = random.choice([w.strip() for w in f.readlines() if len(w.strip()) == self.word_length])

        def undisable(c: t.Union[Button, Select]) -> Item:
            c.disabled = False
            return c

        self.board = [[square.empty(self.light_mode, self.word) for _ in range(self.word_length)] for __ in range(6)]
        self.children = [undisable(c) for c in self.children if c.disabled]

        await interaction.response.defer()
        await self.edit_embed(self.format_board())

    @button(label="Exit", style=ButtonStyle.danger, emoji=STOP_SIGN, disabled=True)
    async def exit(self, button: Button, interaction: MessageInteraction) -> None:
        """
        exit the game so to stop
        using resources to wait
        for a message or interaction.

        params
        ------
        button: Button
            the button that was pressed
            by the user.
        interaction: MessageInteraction
            the interaction instance that
            was returned by the discord api.
        """
        await self.stop()

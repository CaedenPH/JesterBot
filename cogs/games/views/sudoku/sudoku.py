from __future__ import annotations

import typing as t
import asyncio

from disnake import (
    SelectOption,
    HTTPException,
    MessageInteraction,
    Message,
    Embed,
    ButtonStyle,
)
from disnake.ui import View, Button, Select, Item, select, button

from .generator import SudokuGenerator
from core import Context
from core.constants import (
    BLACK_BORDER,
    BLACK_CROSS,
    CLOSE,
    BLACK_BARRIER,
    NUMBERS,
    PLAY_BUTTON,
    RED_NUMBERS,
    SUDOKU_MESSAGE,
    BLACK_SQUARE,
    VIDEO_GAME,
    WHITE_BORDER,
    WHITE_CROSS,
    WHITE_HORIZONTAL,
    WHITE_SQUARE,
    PLACE_NUMBER,
)


class Square:
    bot: bool
    light_mode: bool
    discovered: t.Optional[bool]
    number: int
    user_number: t.Optional[int]

    @classmethod
    def from_bot(cls, number: int, light_mode: bool) -> Square:
        self = cls()
        self.bot = True
        self.number = number
        self.light_mode = light_mode

        return self

    @classmethod
    def from_user(cls, number: int, light_mode: bool) -> Square:
        self = cls()
        self.bot = False
        self.number = number
        self.discovered = False
        self.user_number = None
        self.light_mode = light_mode

        return self

    def __str__(self) -> str:
        if self.bot:
            return NUMBERS[self.number] if self.light_mode else RED_NUMBERS[self.number]
        if self.discovered:
            return RED_NUMBERS[self.number] if self.light_mode else NUMBERS[self.number]
        if self.user_number:
            return (
                RED_NUMBERS[self.user_number]
                if self.light_mode
                else NUMBERS[self.user_number]
            )
        return WHITE_SQUARE if self.light_mode else BLACK_SQUARE


class SudokuBoard:
    """
    Represents a sudoku board.

    attributes
    ----------
    `solved_board: t.List[t.List[int]]`
        the solved_board to view later.
    `board: t.List[t.List[Square]]`
        the unsolved board for the
        user to view.
    """

    def __init__(self, board: t.List[t.List[int]], light_mode: bool):
        self.solved_board = board[0]
        self.board = board[1]
        self.light_mode = light_mode

        self.format_board()

    def format_board(self) -> None:
        """
        Insert square classes into all of
        the squares of the soduku board in order
        to effectively hide and unhide the
        squares from the player.
        """

        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    self.board[row][column] = Square.from_user(
                        self.solved_board[row][column], self.light_mode
                    )
                else:
                    self.board[row][column] = Square.from_bot(
                        self.board[row][column], self.light_mode
                    )

    def game_won(self) -> bool:
        """
        checks if the game is won
        using recursive list checking

        returns
        -------
        bool
            whether or not the game
            has won.
        """

        for row in range(9):
            for column in range(9):
                if self.board[row][column].bot:
                    continue
                if self.board[row][column].user_number != self.board[row][column].number:
                    return False
        return True

    def add_number(self, box: int, square: int, value: int) -> int:
        """
        add a user inputted number
        number to the board.

        error_codes = {
            1: game won
            2: game continuing
            3: invalid arg
        }

        returns
        -------
        int:
            the error code to
            return.
        """

        box -= 1
        square -= 1

        if self.board[box][square].bot:
            return 3

        self.board[box][square].user_number = value
        if self.game_won():
            return 1
        return 2

    def __str__(self) -> str:
        """
        format the board so the user
        can make use of it.

        returns
        -------
        visual_board: str
            the visual board for the user
            to view.
        """

        visual_board = ""
        visual_mode = {
            "border": BLACK_BORDER if self.light_mode else WHITE_BORDER,
            "barrier": BLACK_BARRIER if self.light_mode else WHITE_HORIZONTAL,
            "cross": BLACK_CROSS if self.light_mode else WHITE_CROSS,
        }

        for j in range(3):  # square rows
            for i in range(3):  # square columns
                for k in range(3):  # square height
                    for element in self.board[j * 3 + k][
                        i * 3 : i * 3 + 3
                    ]:  # looping over the three values in a row (1,2,3) -> (4,5,6) -> (7,8,9) -> (1,2,3) -> ...
                        visual_board += str(element)

                    if 2 > k:
                        visual_board += visual_mode["border"]
                visual_board += "\n"
            if 2 > j:
                visual_board += (
                    "".join(
                        [
                            visual_mode["barrier"]
                            + (visual_mode["cross"] if i % 3 == 0 and 8 > i else "")
                            for i in range(1, 10)
                        ]
                    )
                    + "\n"
                )
        return visual_board


class Sudoku(View):
    """
    Represents the sudoku view.

    attributes
    ----------
    `bot_message: Message`
        the message the bot sent at
        the start.
    `ctx: Context`
        the context passed into the view.
    """

    bot_message: Message

    def __init__(self, ctx: Context):
        super().__init__(timeout=7200)

        self.ctx = ctx
        self.light_mode = False
        self.clicked = False
        self.difficulty = "medium"

    def wait_for_check(self, m: Message) -> bool:
        """
        wait_for_check used in a wait_for.

        params
        -----
        m: Message
            the message recieved from
            the wait_for event.

        returns
        -------
        bool
            whether or not to activate
            the button (aka the right
            person clicked the button.)
        """

        return m.author == self.ctx.author and m.channel == self.ctx.channel

    async def on_error(
        self, error: Exception, item: Item, interaction: MessageInteraction
    ) -> None:
        print(error)

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        """
        the check called when a button
        is pressed. also initiated embed

        params
        ------
        interaction: disnake.MessageInteraction
            the interaction passed
            through from the click.

        returns
        -------
        bool
            whether or not the click should
            activate (aka the right person
            clicked it)
        """

        self.embed: Embed = self.bot_message.embeds[0]
        return (
            interaction.author == self.ctx.author
            and interaction.channel == self.ctx.channel
        )

    async def on_timeout(self) -> None:
        """
        the on_timeout method called
        when the timeout is over.
        """

        await self.stop()

    async def stop(self) -> None:
        """
        stop the view and remove all
        buttons (without explicitly
        stopping the view.)
        """

        self.children = []
        await self.edit_embed()

    async def edit_embed(self, desc: t.Optional[str] = None) -> None:
        """
        edits the bot embed without
        having to waste space in code

        params
        ------
        desc: typing.Optional[str] = None
            the description to put in the embed
            if no description is specified it will
            just edit the view of the message.
        """

        if desc:
            self.embed.description = str(desc)
        try:
            await self.bot_message.edit(embed=self.embed, view=self)
        except HTTPException:
            return

    async def delete_message(self, message: Message) -> None:
        """
        delete message without blocking
        the code.

        params
        ------
        message: disnake.Message
            the message to delete.
        """

        await asyncio.sleep(5)
        try:
            await message.delete()
        except HTTPException:
            pass

    @button(label="Place", style=ButtonStyle.green, emoji=NUMBERS[0], disabled=True)
    async def place(self, button: Button, interaction: MessageInteraction) -> None:
        """
        user places a number.

        params
        ------
        button: disnake.ui.Button
            the button instance that
            was clicked.
        interaction: disnake.MessageInteraction
            the interaction passed
            through.
        """

        await interaction.response.send_message(PLACE_NUMBER, delete_after=7.5)
        while True:
            message = await self.ctx.bot.wait_for(
                "message", timeout=3600, check=self.wait_for_check
            )
            asyncio.create_task(self.delete_message(message))

            try:
                user_input = message.content.split()
                box, square, value = (
                    int(user_input[0]),
                    int(user_input[1]),
                    int(user_input[2]),
                )
            except (IndexError, ValueError):
                return await message.add_reaction(CLOSE)

            if (
                box not in range(1, 10)
                or square not in range(1, 10)
                or value not in range(1, 10)
            ):
                return await message.add_reaction(CLOSE)

            result = self.board.add_number(box, square, value)
            if result == 3:
                await message.reply(
                    "You cant place a number on a bot square!", delete_after=7.5
                )
            if result == 2:
                await self.edit_embed(self.board)
            if result == 1:
                await self.edit_embed(self.board)
                await message.reply("You won!", delete_after=7.5)

    @button(label="Play", style=ButtonStyle.green, emoji=PLAY_BUTTON)
    async def play(self, button: Button, interaction: MessageInteraction) -> None:
        """
        initiate the sudoku game.

        checks
        ------
        self.clicked
            if the button has been
            pressed already

        params
        ------
        button: disnake.ui.Button
            the button instance that
            was clicked.
        interaction: disnake.MessageInteraction
            the interaction passed
            through.
        """

        if self.clicked:
            return
        self.clicked = True

        for child in self.children.copy():
            if child.disabled:
                child.disabled = False
            else:
                self.remove_item(child)

        self.board = SudokuBoard(
            board=SudokuGenerator().generate_puzzle(self.difficulty),
            light_mode=self.light_mode,
        )

        await interaction.response.defer()
        await self.edit_embed(self.board)

    @select(
        placeholder=f"Colour settings {BLACK_SQUARE}",
        options=[SelectOption(label="Light mode"), SelectOption(label="Dark mode")],
    )
    async def change_colour_settings(
        self, select: Select, interaction: MessageInteraction
    ) -> None:
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
            "```yaml\n"
            + SUDOKU_MESSAGE.format(
                difficulty=self.difficulty, light_mode=self.light_mode
            )
            + "```"
        )

    @select(
        placeholder=f"Change difficulty {VIDEO_GAME}",
        options=[
            SelectOption(label="easy"),
            SelectOption(label="medium"),
            SelectOption(label="hard"),
            SelectOption(label="insane"),
        ],
    )
    async def change_difficulty(
        self, select: Select, interaction: MessageInteraction
    ) -> None:
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

        self.difficulty = select.values[0]
        await interaction.response.defer()
        await self.edit_embed(
            "```yaml\n"
            + SUDOKU_MESSAGE.format(
                difficulty=self.difficulty, light_mode=self.light_mode
            )
            + "```"
        )

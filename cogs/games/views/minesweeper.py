from __future__ import annotations

import random
import re
import typing as t

from disnake import MessageInteraction, Message, Embed, ButtonStyle
from disnake.ui import View, Button, button

from core.constants import (
    BOMB,
    BLUE_SQUARE,
    RED_FLAG,
    MINESWEEPER_MESSAGE,
    NUMBERS,
    SPOON,
)
from core.context import Context


class Square:
    """
    Represents a square which could
    or could not contain a bomb.
    """

    bomb: bool
    discovered: bool
    flagged: bool
    surrounding_bombs: t.Optional[int]
    emoji_surrounding_bombs: t.Optional[str]

    @classmethod
    def empty(cls) -> Square:
        """
        empty square.
        """

        self = cls()
        self.bomb = False
        self.flagged = False
        self.discovered = False
        self.surrounding_bombs = None
        self.emoji_surrounding_bombs = None

        return self

    @classmethod
    def alive(cls, surrounding_bombs: int) -> Square:
        """
        alive and active square.
        """

        self = cls.empty()
        self.surrounding_bombs = surrounding_bombs
        self.emoji_surrounding_bombs = NUMBERS[surrounding_bombs]

        return self

    @classmethod
    def bomb(cls) -> Square:
        """
        square with a bomb in it.
        """

        self = cls.empty()
        self.bomb = True

        return self

    def __str__(self) -> str:
        if self.flagged:
            return RED_FLAG
        if self.discovered:
            if self.bomb:
                return BOMB
            return self.emoji_surrounding_bombs
        return BLUE_SQUARE


class Board:
    def __init__(self, board_size: int, bomb_count: 10):
        self.board_size = board_size
        self.bomb_count = bomb_count
        self.guesses = 0

        self.create_board()

    def create_board(self, ignore: t.List[int, int] = None) -> None:
        """
        Creates the game board.

        Params
        ------
        ignore: typing.List[int, int]
            coordinates to not place a bomb on
        """

        self.board = [
            [Square.empty() for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

        """
        board representation:
            [_, _, _, _, _, _]
            [_, _, _, _, _, _]
            [_, _, _, _, _, _]
            [_, _, _, _, _, _]
            [_, _, _, _, _, _]
        """

        self.add_bombs(ignore)
        for row in range(self.board_size):
            for column in range(self.board_size):
                if not self.board[row][column].bomb:
                    self.board[row][column] = Square.alive(
                        self.get_surrounding_bombs(row, column)
                    )

    def add_bombs(self, ignore: t.List[int, int] = None) -> None:
        """
        Add the bombs to the board in a random fashion.

        Params
        ------
        ignore: typing.List[int, int]
            coordinates to not place a bomb on
        """

        bombs_added = 0
        while bombs_added != self.bomb_count:
            row = random.randint(0, self.board_size - 1)
            column = random.randint(0, self.board_size - 1)

            if ignore:
                if row == ignore[0] and column == ignore[1]:
                    continue
            if self.board[row][column].bomb:
                continue

            self.board[row][column] = Square.bomb()
            bombs_added += 1

    def get_surrounding_bombs(self, row: int, column: int) -> int:
        """
        we want to loop around the bomb and get the 8 squares around it.
        | 1 | 2 | 3 |
        | 4 | x | 5 |
        | 6 | 7 | 8 |
        so we split into 3 and go 3 across and then 3 down.


        Params
        ------
        row: int
            the row of the board to
            search for.
        column: int
            the column of the board
            to search for.
        """

        bombs_surrounding = 0
        for _row in range(row - 1, row + 2):
            if 0 > _row or _row > self.board_size - 1:
                continue

            for _column in range(column - 1, column + 2):
                if 0 > _column or _column > self.board_size - 1:
                    continue
                if self.board[_row][_column].bomb:
                    bombs_surrounding += 1
        return bombs_surrounding

    def reveal_all(self) -> None:
        """
        Game over so reveal all squares.

        Returns
        -------
        None
        """

        for row in range(self.board_size):
            for column in range(self.board_size):
                self.board[row][column].discovered = True

    def reveal_zeroes(self, hit: t.List[int, int]) -> None:
        """
        Shows the zeroes around the number
        on the first players move.

        Params
        ------
        hit: typing.List[int, int]
            coordinates to not place a bomb on.
        """

        row = hit[0]
        column = hit[1]

        for _row in range(row - 1, row + 2):
            if 0 > _row or _row > self.board_size - 1:
                continue

            for _column in range(column - 1, column + 2):
                if 0 > _column or _column > self.board_size - 1:
                    continue
                if self.board[_row][_column].surrounding_bombs == 0:
                    self.board[_row][_column].discovered = True

    def dig(self, row: int, column: int) -> bool:
        """
        Reveal a square, and if its a bomb; blow up
        checks if there has only been one guess.

        Params
        ------
        row: int
            the row of the board to
            search for.
        column: int
            the column of the board
            to search for.

        Returns
        -------
        bool
            whether or not a bomb
            was hit or not.
        """

        self.guesses += 1
        if self.guesses == 1:
            if self.board[row][column].bomb:
                self.create_board([row, column])
                self.reveal_zeroes([row, column])

        if self.board[row][column].bomb:
            return False

        self.board[row][column].discovered = True
        return True

    def flag(self, row: int, column: int) -> None:
        """
        Flags/Unflags a square as containing a bomb.

        Params
        ------
        row: int
            the row of the board to
            search for.
        column: int
            the column of the board
            to search for.

        Returns
        -------
        None
        """

        self.board[row][column].flagged = not self.board[row][column].flagged

    def format(self) -> str:
        """
        Make the board look visually
        appealing to the player.

        Returns
        -------
        visual_board: str
            the visually appealing board.
        """

        visual_board = f"🟦 | {' | '.join([NUMBERS[n] for n in range(self.board_size)])} |\n{'-----' * self.board_size + '------'}\n"

        for row in range(self.board_size):
            for column in range(self.board_size):
                if column == 0:
                    visual_board += f"{NUMBERS[row]} | {self.board[row][column]} | "
                else:
                    visual_board += f"{self.board[row][column]} | "
            visual_board += f"\n{'-----' * self.board_size + '------'}\n"
        return visual_board

    def __str__(self) -> str:
        return self.format()


class MineSweeper(View):
    bot_message: Message

    def __init__(self, ctx: Context):
        super().__init__(timeout=540)

        self.ctx = ctx
        self.board_size = 5
        self.bomb_count = 5

    def wait_for_check(self, m) -> bool:
        return m.author == self.ctx.author and m.channel == self.ctx.channel

    async def on_timeout(self) -> None:
        for child in self.children:
            self.remove_item(child)
            self.stop()

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        self.embed: Embed = self.bot_message.embeds[0]

        return (
            interaction.author == self.ctx.author
            and interaction.channel == self.ctx.channel
        )

    async def edit_embed(self, desc: t.Union[str, Board]) -> None:
        self.embed.description = "```yaml\n" + str(desc) + "```"
        await self.bot_message.edit(embed=self.embed, view=self)

    @button(label="Dig", style=ButtonStyle.green, emoji=SPOON, disabled=True)
    async def dig_button(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.send_message(
            "Where do you want to dig? | Input as `row,column`", delete_after=15
        )

        message = await self.ctx.bot.wait_for("message", check=self.wait_for_check)
        user_input = re.split(",(\\s)*", message.content)

        row, column = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= self.board_size or column < 0 or column >= self.board_size:
            return await message.reply("Invalid location", delete_after=30)

        survive = self.board.dig(row, column)
        if not survive:
            self.board.reveal_all()
            await message.reply("You got blown up! Game over.")
        await self.edit_embed(self.board)

    @button(label="Flag", style=ButtonStyle.green, emoji=RED_FLAG, disabled=True)
    async def flag_button(
        self, button: Button, interaction: MessageInteraction
    ) -> None:
        await interaction.response.send_message(
            "Where do you want to flag? | Input as `row,column`", delete_after=15
        )

        message = await self.ctx.bot.wait_for("message", check=self.wait_for_check)
        user_input = re.split(",(\\s)*", message.content)

        row, column = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= self.board_size or column < 0 or column >= self.board_size:
            return await message.reply("Invalid location", delete_after=30)

        self.board.flag(row, column)
        await self.edit_embed(self.board)

    @button(label="Play", style=ButtonStyle.green, emoji="▶️")
    async def play_button(
        self, button: Button, interaction: MessageInteraction
    ) -> None:
        self.board = Board(self.board_size, self.bomb_count)

        for child in self.children:
            if isinstance(child, Button):
                child.disabled = not child.disabled

        await interaction.response.defer()
        await self.edit_embed(self.board)

    @button(label="Change board size", style=ButtonStyle.blurple, emoji=BLUE_SQUARE)
    async def change_board_size(
        self, button: Button, interaction: MessageInteraction
    ) -> None:
        await interaction.response.send_message(
            "What dimension would you like to change to? | Eg `7` gives a board 7 high and 7 wide | Send integer only",
            delete_after=15,
        )

        message = await self.ctx.bot.wait_for("message", check=self.wait_for_check)
        if int(message.content) > 10:
            return await message.reply("The limit is a 10x10 grid", delete_after=30)
        elif int(message.content) < 2:
            return await message.reply("The minimum is a 3x3 grid", delete_after=30)

        self.board_size = int(message.content)
        self.bomb_count = self.board_size
        await self.edit_embed(
            MINESWEEPER_MESSAGE.format(
                board_size=self.board_size, bomb_count=self.bomb_count
            )
        )

    @button(label="Change bomb count", style=ButtonStyle.blurple, emoji=BOMB)
    async def change_bomb_count(
        self, button: Button, interaction: MessageInteraction
    ) -> None:
        await interaction.response.send_message(
            "What would you like the bomb count to be? | Send integer only",
            delete_after=15,
        )

        message = await self.ctx.bot.wait_for("message", check=self.wait_for_check)
        if int(message.content) > (self.board_size ** 2) * 0.5:
            return await message.reply(
                "You cant have more than half of the board covered in bombs!",
                delete_after=30,
            )

        self.bomb_count = int(message.content)
        await self.edit_embed(
            MINESWEEPER_MESSAGE.format(
                board_size=self.board_size, bomb_count=self.bomb_count
            )
        )

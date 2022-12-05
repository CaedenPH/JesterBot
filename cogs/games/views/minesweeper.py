from __future__ import annotations

import asyncio
import copy
import random
import typing as t

from disnake import (
    ButtonStyle, Embed, HTTPException, Message, MessageInteraction
)
from disnake.ui import Button, Item, View, button

from core.constants import (
    BLACK_BARRIER, BLACK_BORDER, BLACK_SQUARE, BLUE_SQUARE, BOMB, CLOSE,
    MINESWEEPER_MESSAGE, NUMBERS, PLAY_BUTTON, RED_FLAG, RED_NUMBERS, SPOON,
    STOP_SIGN
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

    def __str__(self) -> str:
        """
        represents the visual square

        Returns
        -------
        emoji: str
            the emoji being returned
            whether that be flag,
            bomb, number or empty.
        """

        if self.discovered:
            if self.bomb:
                return BOMB
            return self.emoji_surrounding_bombs
        if self.flagged:
            return RED_FLAG
        return BLUE_SQUARE

    def flag(self) -> None:
        """
        flag/unflag a square
        """

        self.flagged = not self.flagged

    @classmethod
    def empty(cls) -> Square:
        """
        empty square.

        Returns
        -------
        self: Square
            empty placeholder square
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

        Returns
        -------
        self: Square
            the alive square instance
        """

        self = cls.empty()
        self.surrounding_bombs = surrounding_bombs
        self.emoji_surrounding_bombs = NUMBERS[surrounding_bombs]

        return self

    @classmethod
    def bomb(cls) -> Square:
        """
        square with a bomb in it.

        Returns
        -------
        self: Square
            the bomb square instance
        """

        self = cls.empty()
        self.bomb = True

        return self


class DigStatus:
    game_lost: bool
    game_won: bool

    @classmethod
    def empty(cls) -> DigStatus:
        self = cls()
        self.game_lost = False
        self.game_won = False

        return self

    @classmethod
    def loss(cls) -> DigStatus:
        self = cls.empty()
        self.game_lost = True

        return self

    @classmethod
    def win(cls) -> DigStatus:
        self = cls().empty()
        self.game_won = True

        return self

    def game_over(self) -> bool:
        return self.game_lost or self.game_won


class Board:
    def __init__(self, board_size: int, bomb_count: int):
        self.board_size = board_size
        self.bomb_count = bomb_count
        self.guesses = 0

        self.create_board()

    def create_board(self, ignore: t.List[int, int,] = None) -> None:
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

    def add_bombs(self, ignore: t.List[int, int,] = None) -> None:
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

    def reveal_zeroes(self, hit: t.List[int, int,]) -> None:
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

    def all_discovered(self) -> bool:
        """
        Checks to see if all non-bomb
        squares have been discovered
        """

        for row in range(self.board_size):
            for column in range(self.board_size):
                if (
                    not self.board[row][column].discovered
                    and not self.board[row][column].bomb
                ):
                    return False
        return True

    def dig(self, row: int, column: int) -> DigStatus:
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

        self.board[row][column].discovered = True
        if self.board[row][column].bomb:
            return DigStatus.loss()
        if self.all_discovered():
            return DigStatus.win()
        return DigStatus.empty()

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

        self.board[row][column].flag()

    def format(self) -> str:
        """
        Make the board look visually
        appealing to the player.

        Returns
        -------
        visual_board: str
            the visually appealing board.
        """

        visual_board = f"{BLACK_SQUARE} {BLACK_BORDER} {f' {BLACK_BORDER} '.join([RED_NUMBERS[n] for n in range(self.board_size)])}\n{BLACK_BARRIER * ((self.board_size * 3) - 2)}\n"

        for row in range(self.board_size):
            for column in range(self.board_size):
                if column == 0:
                    visual_board += f"{RED_NUMBERS[row]} {BLACK_BORDER} {self.board[row][column]} {BLACK_BORDER}"
                else:
                    visual_board += f"{self.board[row][column]} {BLACK_BORDER}"
            visual_board += f"\n{BLACK_BARRIER * ((self.board_size * 3) - 2)}\n"
        return visual_board

    def __str__(self) -> str:
        return self.format()


class MineSweeper(View):
    bot_message: Message

    def __init__(self, ctx: Context, new: bool = False):
        super().__init__(timeout=720)

        self.ctx = ctx
        self.button_pressed = 0

        if new:
            return

        self.board_size = 5
        self.bomb_count = 5
        self.dig = DigStatus.empty()
        self.board: Board = None

    async def new_message(self) -> MineSweeper:
        def undisable(child: Button):
            child.disabled = False
            if child.label == "Exit":
                child.row = 0
            return child

        new = MineSweeper(self.ctx, new=True)
        new.board = self.board
        new.dig = self.dig
        new.board_size = self.board_size
        new.bomb_count = self.bomb_count
        new.children = [
            undisable(child)
            for child in new.children
            if isinstance(child, Button) and child.disabled
        ]

        await self.exit()
        return new

    def wait_for_check(self, m) -> bool:
        return m.author == self.ctx.author and m.channel == self.ctx.channel

    async def exit(self) -> None:
        self.button_pressed = 0

        for child in self.children:
            if not isinstance(child, Button):
                continue

            child.disabled = True
        await self.edit_embed()

    async def on_timeout(self) -> None:
        await self.exit()

    async def on_error(
        self, error: Exception, item: Item, interaction: MessageInteraction
    ) -> None:
        print(error)

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        self.embed: Embed = self.bot_message.embeds[0]

        return (
            interaction.author == self.ctx.author
            and interaction.channel == self.ctx.channel
        )

    async def edit_embed(self, desc: t.Union[str, Board,] = None) -> None:
        if desc:
            self.embed.description = str(desc)
        if self.board:
            self.embed.set_footer(text=f"Guesses: {self.board.guesses}")
        try:
            await self.bot_message.edit(embed=self.embed, view=self)
        except HTTPException:
            return

    async def delete_message(self, message: Message) -> None:
        await asyncio.sleep(5)
        try:
            await message.delete()
        except HTTPException:
            pass

    @button(label="Dig", style=ButtonStyle.green, emoji=SPOON, disabled=True, row=0)
    async def dig_button(self, button: Button, interaction: MessageInteraction) -> None:
        """
        dig button [1]

        checks
        ------
        `dig.game_over()`
            if the game is over,
            don't respond.
        `button_pressed == 1`
            the button has already
            been pressed, ignore it.
        `button_pressed == 2`
            flag button was pressed,
            change it to 1.
        """

        if self.dig.game_over():
            return
        if self.button_pressed == 1:
            return
        self.button_pressed = 1

        await interaction.response.send_message(
            "Where do you want to dig? | Input as `row` `column` |", delete_after=5
        )
        while True:
            message = await self.ctx.bot.wait_for(
                "message", timeout=720, check=self.wait_for_check
            )
            asyncio.create_task(self.delete_message(message))

            if self.button_pressed != 1:
                return

            try:
                user_input = message.content.split()
                (row, column) = int(user_input[0]), int(user_input[-1])
            except ValueError:
                self.button_pressed = 0
                return await message.add_reaction(CLOSE)

            if (
                row < 0
                or row >= self.board_size
                or column < 0
                or column >= self.board_size
            ):
                self.button_pressed = 0
                return await message.add_reaction(CLOSE)

            self.dig = self.board.dig(row, column)
            if self.dig.game_lost:
                self.board.reveal_all()
                await message.reply(
                    "**You got blown up** | Try not to step on so many bombs!"
                )
            elif self.dig.game_won:
                self.board.reveal_all()
                await message.reply("**You dug all non-bomb squares** | You win!")
            await self.edit_embed(self.board)

            if self.dig.game_over():
                return

    @button(label="Flag", style=ButtonStyle.green, emoji=RED_FLAG, disabled=True, row=0)
    async def flag_button(self, button: Button, interaction: MessageInteraction) -> None:
        """
        flag button [2]

        checks
        ------
        `self.dig.game_over`
            if the game is over,
            don't respond.
        `self.button_pressed == 2`
            the button has already
            been pressed, ignore it.
        `self.button_pressed == 1`
            dig button was previously
            pressed. change it to 2.
        """

        if self.dig.game_over():
            return
        if self.button_pressed == 2:
            return
        self.button_pressed = 2

        await interaction.response.send_message(
            "Where do you want to flag? | Input as `row` `column`", delete_after=5
        )
        while True:
            message = await self.ctx.bot.wait_for(
                "message", timeout=720, check=self.wait_for_check
            )
            asyncio.create_task(self.delete_message(message))

            if self.button_pressed != 2:
                return

            try:
                user_input = message.content.split()
                (row, column) = int(user_input[0]), int(user_input[-1])
            except ValueError:
                self.button_pressed = 0
                return await message.add_reaction(CLOSE)

            if (
                row < 0
                or row >= self.board_size
                or column < 0
                or column >= self.board_size
            ):
                self.button_pressed = 0
                return await message.add_reaction(CLOSE)

            self.board.flag(row, column)
            await self.edit_embed(self.board)

            if self.dig.game_over():
                return

    @button(
        label="Resend", style=ButtonStyle.blurple, emoji=BLUE_SQUARE, row=0, disabled=True
    )
    async def resend(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.defer()

        view = await self.new_message()
        view.bot_message = await self.ctx.send(embed=self.embed, view=view)

    @button(label="Play", style=ButtonStyle.green, emoji=PLAY_BUTTON, row=0)
    async def play_button(self, button: Button, interaction: MessageInteraction) -> None:
        """
        play the game, and removes
        all buttons that cannot be used
        mid game and replaces them
        with disabled buttons.
        """

        def undisable(child: Button):
            child.disabled = False
            if child.label == "Exit":
                child.row = 0
            return child

        self.board = Board(self.board_size, self.bomb_count)
        self.children = [
            undisable(child)
            for child in self.children
            if isinstance(child, Button) and child.disabled
        ]

        await interaction.response.defer()
        await self.edit_embed(self.board)

    @button(
        label="Change board size", style=ButtonStyle.blurple, emoji=BLUE_SQUARE, row=1
    )
    async def change_board_size(
        self, button: Button, interaction: MessageInteraction
    ) -> None:
        """
        resize the board.
        """

        await interaction.response.send_message(
            "What dimension would you like to change to? | Eg `7` gives a board 7 high and 7 wide | Send integer only",
            delete_after=5,
        )

        message = await self.ctx.bot.wait_for(
            "message", timeout=720, check=self.wait_for_check
        )
        asyncio.create_task(self.delete_message(message))

        if int(message.content) > 10:
            return await message.reply("The limit is a 10x10 grid", delete_after=30)
        elif int(message.content) < 2:
            return await message.reply("The minimum is a 3x3 grid", delete_after=30)
        if message.content.isalpha():
            return await message.add_reaction(CLOSE)

        self.board_size = int(message.content)
        self.bomb_count = self.board_size
        await self.edit_embed(
            MINESWEEPER_MESSAGE.format(
                board_size=self.board_size, bomb_count=self.bomb_count
            )
        )

    @button(label="Change bomb count", style=ButtonStyle.blurple, emoji=BOMB, row=1)
    async def change_bomb_count(
        self, button: Button, interaction: MessageInteraction
    ) -> None:
        """
        change the bomb count.
        """

        await interaction.response.send_message(
            "What would you like the bomb count to be? | Send integer only",
            delete_after=5,
        )

        message = await self.ctx.bot.wait_for(
            "message", timeout=720, check=self.wait_for_check
        )
        if int(message.content) > (self.board_size ** 2) * 0.5:
            return await message.reply(
                "You cant have more than half of the board covered in bombs!",
                delete_after=30,
            )
        if message.content.isalpha():
            return await message.add_reaction(CLOSE)

        self.bomb_count = int(message.content)
        await self.edit_embed(
            MINESWEEPER_MESSAGE.format(
                board_size=self.board_size, bomb_count=self.bomb_count
            )
        )
        asyncio.create_task(self.delete_message(message))

    @button(label="Exit", style=ButtonStyle.danger, emoji=STOP_SIGN, disabled=True, row=1)
    async def exit_button(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.defer()
        await self.exit()

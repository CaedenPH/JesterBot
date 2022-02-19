from __future__ import annotations

import random
import re
import typing as t

from disnake import MessageInteraction, Message, Embed, ButtonStyle
from disnake.ui import View, Button, button

from core.constants import BOMB, BLUE_SQUARE, RED_FLAG, MINESWEEPER_MESSAGE, NUMBERS, SPOON
from core.context import Context

class Square:
    bomb: bool
    discovered: bool
    flagged: bool
    surrounding_bombs: t.Optional[int]
    emoji_surrounding_bombs: t.Optional[str]

    @classmethod
    def empty(cls) -> Square:
        self = cls()
        self.bomb = False
        self.flagged = False
        self.discovered = False
        self.surrounding_bombs = None
        self.emoji_surrounding_bombs = None

        return self

    @classmethod
    def alive(cls, surrounding_bombs: int) -> Square:
        self = cls.empty()
        self.surrounding_bombs = surrounding_bombs
        self.emoji_surrounding_bombs = NUMBERS[surrounding_bombs]

        return self

    @classmethod
    def bomb(cls) -> Square:
        self = cls.empty()
        self.bomb = True
    
        return self

    def __str__(self) -> str:
        if self.flagged:
            return RED_FLAG
        if self.discovered:
            return self.emoji_surrounding_bombs
        return BLUE_SQUARE
        
class Board:
    def __init__(self, board_size: int, bomb_count: 10):
        self.board_size = board_size
        self.bomb_count = bomb_count
        self.create_board()

    def create_board(self) -> None:
        self.board = [[Square.empty() for _ in range(self.board_size)] for _ in range(self.board_size)]

        """
        board representation:
            [_, _, _, _, _, _]
            [_, _, _, _, _, _]
            [_, _, _, _, _, _]
            [_, _, _, _, _, _]
            [_, _, _, _, _, _]
        """

        bombs_added = 0
        while bombs_added != self.bomb_count:
            row = random.randint(0, self.board_size-1)
            column = random.randint(0, self.board_size-1)

            if self.board[row][column].bomb:
                continue

            self.board[row][column] = Square.bomb()
            bombs_added += 1

        for row in range(self.board_size):
            for column in range(self.board_size):
                if not self.board[row][column].bomb:
                    self.board[row][column] = Square.alive(self.get_surrounding_bombs(row, column))

    def get_surrounding_bombs(self, row: int, column: int) -> int:
        """
        we want to loop around the bomb and get the 8 squares around it
        | 1 | 2 | 3 |
        | 4 | x | 5 |
        | 6 | 7 | 8 |

        so we split into 3 and go 3 across and then 3 down
        """

        bombs_surrounding = 0
        for _row in range(row-1, row+2):
            if 0 > _row or _row > self.board_size -1:
                continue

            for _column in range(column-1, column+2):
                if 0 > _column or _column > self.board_size -1 :
                    continue    
                print(_row, _column)
                if self.board[_row][_column].bomb:
                    bombs_surrounding += 1
        return bombs_surrounding

    def format(self) -> str:
        "0️⃣ | 1️⃣ | 2️⃣ | 3️⃣ | 4️⃣ | 5️⃣ | 6️⃣ | 7️⃣ | 8️⃣ | 9️⃣"
        string = f"🟦 | {' | '.join([NUMBERS[n] for n in range(self.board_size)])} |\n{'-----' * self.board_size + '------'}\n"

        for row in range(self.board_size):
            for column in range(self.board_size):
                if column == 0:
                    string += f"{NUMBERS[row]} | {self.board[row][column]} | "
                else:
                    string += f"{self.board[row][column]} | "

            string += f"\n{'-----' * self.board_size + '------'}\n"
        return string

    def __str__(self) -> str:
        return self.format()

class MineSweeper(View):
    bot_message: Message

    def __init__(self, ctx: Context):
        super().__init__(timeout=540)

        self.ctx = ctx
        self.board_size = 10
        self.bomb_count = 10

    def wait_for_check(self, m) -> bool:
        return (
            m.author == self.ctx.author
            and m.channel == self.ctx.channel
        )

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
        await interaction.response.send_message("Where do you want to dig? | Input as `row,column`")

        message = await self.ctx.bot.wait_for("message", check=self.wait_for_check)
        user_input = re.split(',(\\s)*', message.content)

        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return await message.reply("Invalid location")
        
        await self.edit_embed(self.board)

    @button(label="Flag", style=ButtonStyle.green, emoji=RED_FLAG, disabled=True)
    async def flag_button(self, button: Button, interaction: MessageInteraction) -> None:
        ...

    @button(label="Play", style=ButtonStyle.green, emoji="▶️")
    async def play_button(self, button: Button, interaction: MessageInteraction) -> None:
        self.board = Board(self.board_size, self.bomb_count)
        print(self.board)

        for child in self.children:
            if isinstance(child, Button):
                child.disabled = not child.disabled

        await interaction.response.defer()
        await self.edit_embed(self.board)

    @button(label="Change board size", style=ButtonStyle.blurple, emoji=BLUE_SQUARE)
    async def change_board_size(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.send_message("What dimension would you like to change to? | Eg `7` gives a board 7 high and 7 wide | Send integer only ")

        message = await self.ctx.bot.wait_for("message", check=self.wait_for_check)
        self.board_size = int(message.content)

        await self.edit_embed(
            MINESWEEPER_MESSAGE.format(
                board_size=self.board_size,
                bomb_count=self.bomb_count
        ))

    @button(label="Change bomb count", style=ButtonStyle.blurple, emoji=BOMB)
    async def change_bomb_count(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.send_message("What would you like the bomb count to be? | Send integer only")

        message = await self.ctx.bot.wait_for("message", check=self.wait_for_check)
        if int(message.content) > self.board_size * self.board_size * 0.5:
            return await message.reply("You cant have more than half of the board covered in bombs!")

        self.bomb_count = int(message.content)
        await self.edit_embed(
            MINESWEEPER_MESSAGE.format(
                board_size=self.board_size,
                bomb_count=self.bomb_count
        ))

from __future__ import annotations

import random
import typing as t
import asyncio

from disnake import MessageInteraction, Message, HTTPException, Embed, ButtonStyle
from disnake.ui import View, Button, button
from disnake.ext.tasks import loop

from core.constants import (
    BLUE_SQUARE,
    CLOSE,
    GREEN_SQUARE,
    PLAY_BUTTON,
    SNAKE_MESSAGE,
    STOP_SIGN,
    SWEET,
    UP_ARROW,
    DOWN_ARROW,
    LEFT_ARROW,
    RIGHT_ARROW,
    VIDEO_GAME,
    WHITE_SQUARE,
)

_p1 = button(style=ButtonStyle.grey, emoji=BLUE_SQUARE, disabled=True, row=0)
_p2 = button(style=ButtonStyle.grey, emoji=BLUE_SQUARE, disabled=True, row=1)
_p3 = button(style=ButtonStyle.grey, emoji=BLUE_SQUARE, disabled=True, row=2)
_p4 = button(style=ButtonStyle.grey, emoji=BLUE_SQUARE, disabled=True, row=3)


class GameMode:
    active_sweets: int
    game_mode: str

    @classmethod
    def easy(cls) -> GameMode:
        self = cls()
        self.active_sweets = 6
        self.game_mode = "easy"

        return self

    @classmethod
    def normal(cls) -> GameMode:
        self = cls()
        self.active_sweets = 4
        self.game_mode = "normal"

        return self

    @classmethod
    def hard(cls) -> GameMode:
        self = cls()
        self.active_sweets = 2
        self.game_mode = "hard"

        return self

    def __str__(self) -> None:
        return self.game_mode


class SnakeGame:
    def __init__(self, board_size: int, game_mode: GameMode) -> None:
        self.board_size = board_size
        self.game_mode = game_mode

        self.snake_pos: t.List[t.List[int, int,]] = [[8, 5], [8, 6], [8, 7], [8, 8], [8, 9], [8, 10]]
        self.sweet_coords: t.List[t.List[int, int,]] = [
            [random.randint(0, self.board_size), random.randint(0, self.board_size)]
            for _ in range(self.game_mode.active_sweets)
        ]
        self.direction: t.List[int] = [0, 0]

    def move(self) -> None:
        self.snake_pos.pop(0)
        last_coord = self.snake_pos[-1]

        if self.direction[-1] == 0:  # direction: right
            if self.direction[-2]:
                self.snake_pos.reverse()
            new_coords = [last_coord[0], last_coord[-1] + 1]

        elif self.direction[-1] == 1:  # direction: left
            if self.direction[-2]:
                self.snake_pos.reverse()
            new_coords = [last_coord[0], last_coord[-1] - 1]

        elif self.direction[-1] == 2:  # direction: up
            if self.direction[-2]:
                self.snake_pos.reverse()
            new_coords = [last_coord[0] - 1, last_coord[-1]]

        else:  # direction: down
            if self.direction[-2]:
                self.snake_pos.reverse()
            new_coords = [last_coord[0] + 1, last_coord[-1]]
        self.snake_pos.append(new_coords)

    def format(self) -> str:
        board = [[WHITE_SQUARE for _ in range(self.board_size)] for __ in range(self.board_size)]
        visual_board = ""

        for row in range(self.board_size):
            for column in range(self.board_size):
                if [row, column] in self.snake_pos:
                    visual_board += GREEN_SQUARE
                elif [row, column] in self.sweet_coords:
                    visual_board += SWEET
                else:
                    visual_board += board[row][column]
            visual_board += "\n"
        return visual_board

    def __str__(self) -> str:
        return self.format()


class Snake(View):
    bot_message: Message

    def __init__(self, ctx):
        super().__init__(timeout=540)

        self.ctx = ctx
        self.embed: Embed
        self.board_size = 17
        self.game_mode: GameMode = GameMode.normal()

    async def on_timeout(self) -> None:
        await self.stop()

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        self.embed = self.bot_message.embeds[0]
        return interaction.author == self.ctx.author and interaction.channel == self.ctx.channel

    async def edit_embed(self, desc: t.Optional[str] = None) -> None:
        if desc:
            self.embed.description = "```yaml\n" + str(desc) + "```"
        self.embed.set_footer(text=f"Game mode: {str(self.game_mode)}")
        await self.bot_message.edit(embed=self.embed, view=self)

    async def stop(self) -> None:
        self.children = []
        await self.edit_embed()

    async def delete_message(self, message: Message) -> None:
        await asyncio.sleep(7.5)
        try:
            await message.delete()
        except HTTPException:
            pass

    @loop(seconds=1.0)
    async def move_snake(self) -> None:
        self.board.move()
        await self.edit_embed(self.board)

    @_p1
    async def _pl_1(self, _, __):
        ...

    @_p1
    async def _pl_2(self, _, __):
        ...

    @_p1
    async def _pl_3(self, _, __):
        ...

    @_p1
    async def _pl_4(self, _, __):
        ...

    @_p1
    async def _pl_5(self, _, __):
        ...

    @_p2
    async def _pl_6(self, _, __):
        ...

    @_p2
    async def _pl_7(self, _, __):
        ...

    @button(style=ButtonStyle.green, emoji=UP_ARROW, disabled=True)
    async def up(self, button: Button, interaction: MessageInteraction) -> None:
        """
        up button
        """

        self.board.direction.append(2)
        await interaction.response.defer()

    @_p2
    async def _pl_8(self, _, __):
        ...

    @_p2
    async def _pl_9(self, _, __):
        ...

    @_p3
    async def _pl_10(self, _, __):
        ...

    @button(style=ButtonStyle.green, emoji=LEFT_ARROW, disabled=True, row=2)
    async def left(self, button: Button, interaction: MessageInteraction) -> None:
        """
        left button
        """

        self.board.direction.append(1)
        await interaction.response.defer()

    @button(style=ButtonStyle.green, emoji=DOWN_ARROW, disabled=True, row=2)
    async def down(self, button: Button, interaction: MessageInteraction) -> None:
        """
        down button
        """

        self.board.direction.append(3)
        await interaction.response.defer()

    @button(style=ButtonStyle.green, emoji=RIGHT_ARROW, disabled=True, row=2)
    async def right(self, button: Button, interaction: MessageInteraction) -> None:
        """
        right button
        """

        self.board.direction.append(0)
        await interaction.response.defer()

    @_p3
    async def _pl_11(self, _, __):
        ...

    @_p4
    async def _pl_12(self, _, __):
        ...

    @_p4
    async def _pl_13(self, _, __):
        ...

    @_p4
    async def _pl_14(self, _, __):
        ...

    @_p4
    async def _pl_15(self, _, __):
        ...

    @_p4
    async def _pl_16(self, _, __):
        ...

    @button(label="Play", style=ButtonStyle.green, emoji=PLAY_BUTTON, row=4)
    async def play(self, button: Button, interaction: MessageInteraction) -> None:
        """
        play the snake game
        """

        if button.label == "Exit":
            return await self.stop()

        self.board = SnakeGame(self.board_size, self.game_mode)
        for child in self.children.copy():
            if not isinstance(child, Button):
                continue

            if child.label == "Play":
                child.label = "Exit"
                child.style = ButtonStyle.danger
                child.emoji = STOP_SIGN

            if child.style == ButtonStyle.green:
                child.disabled = False

            if child.style == ButtonStyle.blurple:
                self.remove_item(child)

        await interaction.response.defer()
        await self.edit_embed(self.board)
        self.move_snake.start()

    @button(label="Game mode", style=ButtonStyle.blurple, emoji=BLUE_SQUARE, disabled=True, row=4)
    async def change_game_mode(self, button: Button, interaction: MessageInteraction) -> None:
        """
        change game mode
        """

        await interaction.response.send_message(
            "What game mode would you like to change to? | Send an option out of easy, normal, hard", delete_after=15
        )

        message = (await self.ctx.bot.wait_for("message", timeout=540, check=self.wait_for_check)).lower()
        asyncio.create_task(self.delete_message(message))

        if message.content not in ["easy", "normal", "hard"]:
            return await message.reply("Send an option out of easy, normal, hard")

        if message.content == "easy":
            self.game_mode = GameMode.easy()
        elif message.content == "normal":
            self.game_mode = GameMode.normal()
        elif message.content == "hard":
            self.game_mode = GameMode.hard()

        await self.edit_embed(SNAKE_MESSAGE.format(board_size=self.board_size, game_mode=str(self.game_mode)))

    @button(label="Board size", style=ButtonStyle.blurple, emoji=VIDEO_GAME, disabled=True, row=4)
    async def change_board_size(self, button: Button, interaction: MessageInteraction) -> None:
        """
        change board size
        """

        await interaction.response.send_message(
            "What dimension would you like to change to? | Eg `7` gives a board 7 high and 7 wide | Send integer only",
            delete_after=15,
        )

        message = await self.ctx.bot.wait_for("message", timeout=540, check=self.wait_for_check)
        asyncio.create_task(self.delete_message(message))

        if int(message.content) > 10:
            return await message.reply("The limit is a 10x10 grid", delete_after=30)
        elif int(message.content) < 2:
            return await message.reply("The minimum is a 3x3 grid", delete_after=30)
        if message.content.isalpha():
            return await message.add_reaction(CLOSE)

        self.board_size = int(message.content)
        await self.edit_embed(SNAKE_MESSAGE.format(board_size=self.board_size, game_mode=str(self.game_mode)))

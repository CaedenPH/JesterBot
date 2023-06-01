import random

from disnake import ButtonStyle, Embed, MessageInteraction
from disnake.ui import Button, View, button

from core.utils import get_colour


class Dice(View):
    def __init__(self, ctx):
        super().__init__(timeout=180)

        self.ctx = ctx
        self.role_count: int = 0

    async def on_timeout(self) -> None:
        for child in self.children:
            self.remove_item(child)
            self.stop()

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        return (
            interaction.author == self.ctx.author
            and interaction.channel == self.ctx.channel
        )

    @button(label="Roll", style=ButtonStyle.green, emoji="▶️")
    async def roll(self, button: Button, interaction: MessageInteraction) -> None:
        self.role_count += 1
        random_number = random.randint(0, 5)
        emoji = {
            0: "<:dice1:932735376089559090>",
            1: "<:dice2:932735375649157122>",
            2: "<:dice3:932735376236363866>",
            3: "<:dice4:932735376160862278>",
            4: "<:dice5:932735376118923264>",
            5: "<:dice6:932735376274120765>",
        }
        embed = Embed(
            title="<:dicetitle:932727881069641858> Dice <:dicetitle:932727881069641858>",
            description=f"You rolled a: {emoji[random_number]} `{random_number}` {emoji[random_number]}",
            Colour=get_colour(),
        ).set_footer(
            text=f"{interaction.author.name} is playing with some dice | Role count: {self.role_count}",
            icon_url=(interaction.author.display_avatar.url),
        )
        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed, view=self)

    @button(label="Stop", style=ButtonStyle.red, emoji="⏹️")
    async def Stop(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.defer()
        await interaction.edit_original_message(view=None)
        self.stop()

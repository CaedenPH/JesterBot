import random

from disnake import MessageInteraction, Embed, ButtonStyle
from disnake.ui import View, Button, button


class RussianRoulette(View):
    def __init__(self, ctx):
        super().__init__(timeout=180)

        self.ctx = ctx

    async def on_timeout(self) -> None:
        for child in self.children:
            self.remove_item(child)
            self.stop()

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        return interaction.author == self.ctx.author and interaction.channel == self.ctx.channel

    @button(label="Play", style=ButtonStyle.green, emoji="▶️")
    async def play(self, button: Button, interaction: MessageInteraction) -> None:
        random_choice = random.choice(["🌹 / **You lived**", "<:gun:931861130488467456> / **You died**"])
        embed_colour = {"🌹 / **You lived**": 0x32CD32, "<:gun:931861130488467456> / **You died**": 0x8B0000}

        footer_text = random.choice(
            [
                "loves to play this game",
                "must like excitement",
                "is definitely a risk taker",
                "definitely hates life",
                "plays this game 24/7",
                "has issues",
                "probably needs some help",
            ]
        )

        embed = Embed(description=random_choice, colour=embed_colour[random_choice]).set_footer(
            text=f"{interaction.author.name} {footer_text}", icon_url=(interaction.author.display_avatar.url)
        )

        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed, view=self)

    @button(label="Exit", style=ButtonStyle.red, emoji="⏹️")
    async def exit(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.defer()
        await interaction.edit_original_message(view=None)
        self.stop()

import random

from disnake import ButtonStyle, Embed, MessageInteraction
from disnake.ui import Button, View, button

from core import Context
from core.utils.utils import get_colour


class Meme(View):
    def __init__(self, ctx: Context):
        super().__init__(timeout=180)

        self.ctx = ctx

    async def on_timeout(self) -> None:
        for child in self.children:
            self.remove_item(child)
            self.stop()

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        return (
            interaction.author == self.ctx.author
            and interaction.channel == self.ctx.channel
        )

    @button(label="Next", style=ButtonStyle.green, emoji="⏭️")
    async def meme(self, button: Button, interaction: MessageInteraction) -> None:
        post = random.choice(self.ctx.bot.meme_list)
        embed = (
            Embed(title=post.title, Colour=get_colour())
            .set_image(url=post.url)
            .set_footer(
                text=f"Requested by {interaction.author.name}",
                icon_url=interaction.author.display_avatar.url,
            )
        )
        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed, view=self)

    @button(label="Exit", style=ButtonStyle.red, emoji="⏹️")
    async def exit(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.defer()
        await interaction.edit_original_message(view=None)
        self.stop()

import asyncio
import random

from disnake import ButtonStyle, Embed, Member, MessageInteraction
from disnake.ui import Button, View, button


class Casino(View):
    def __init__(self, author: Member) -> None:
        self.author = author
        self.defualtstring = [
            "Casino Machine $",
            "Get Three numbers in a row for a PRIZE",
        ]
        super().__init__(timeout=60.0)
        self.retry.disabled = True

    async def on_timeout(self) -> None:
        for child in self.children:
            self.remove_item(child)
            self.stop()

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        if interaction.author != self.author:
            return False
        return True

    @button(label="Play", style=ButtonStyle.green, emoji="▶️")
    async def play(self, button: Button, interaction: MessageInteraction) -> None:
        self.exit.disabled = True
        self.play.disabled = True
        intsthink = Embed(
            title=self.defualtstring[0], description="```...```"
        ).set_footer(text=self.defualtstring[1])

        await interaction.response.edit_message(embed=intsthink, view=self)

        r_ints = (random.randint(1, 9), random.randint(1, 9), random.randint(1, 9))
        (result, ints) = ([], None)

        for i in r_ints:
            result.append(str(i))
            ints = Embed(
                title=self.defualtstring[0], description=f"```{''.join(result)}```"
            ).set_footer(text=self.defualtstring[1])
            await interaction.edit_original_message(embed=ints, view=self)
            await asyncio.sleep(0.2)

        self.retry.disabled = False
        self.exit.disabled = False
        await interaction.edit_original_message(embed=ints, view=self)

        if len(set(r_ints)) == 1:
            awinningembed = Embed(
                title="WINNER",
                description=f"{interaction.author.mention} has won {random.randint(1, 1000)}$",
            )
            self.stop()
            return await interaction.send(embed=awinningembed)

    @button(label="Retry", style=ButtonStyle.green, emoji="🔄")
    async def retry(self, button: Button, interaction: MessageInteraction) -> None:
        intsthink1 = Embed(
            title=self.defualtstring[0], description="```...```"
        ).set_footer(text=self.defualtstring[1])
        self.exit.disabled = True
        await interaction.response.edit_message(embed=intsthink1, view=self)

        r_ints = (random.randint(1, 9), random.randint(1, 9), random.randint(1, 9))

        (result, ints) = ([], None)
        for i in r_ints:
            result.append(str(i))
            ints = Embed(
                title=self.defualtstring[0], description=f"```{''.join(result)}```"
            ).set_footer(text=self.defualtstring[1])
            await interaction.edit_original_message(embed=ints, view=self)
            await asyncio.sleep(0.2)

        self.retry.disabled = False
        self.exit.disabled = False
        await interaction.edit_original_message(embed=ints, view=self)

        if len(set(r_ints)) == 1:
            bwinningembed = Embed(
                title="WINNER",
                description=f"{interaction.author.mention} has won {random.randint(1, 1000)}$",
            )
            self.stop()
            return await interaction.send(embed=bwinningembed)

    @button(label="Exit", style=ButtonStyle.red, emoji="⏹️")
    async def exit(self, button: Button, interaction: MessageInteraction) -> None:
        await interaction.response.defer()
        await interaction.edit_original_message(view=None)
        self.stop()

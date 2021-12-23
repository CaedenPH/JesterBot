import disnake
from disnake.ext import commands

from core.utils.emojis import COGemojis, HOME

class Dropdown(disnake.ui.Select):
    def __init__(self, data, ctx:commands.Context, utils):
        self.data = data
        self.ctx = ctx
        self.utils = utils


        options = [
            disnake.SelectOption(
                label="Home", 
                description="Return to the main help panel", 
                emoji=HOME
            ),
        ]
        for key in data:
            options.append(
                disnake.SelectOption(
                    label=key,
                    description=f"{len([k for k in ctx.bot.get_cog(key).walk_commands() if not k.hidden])} commands",
                    emoji=ctx.bot.get_emoji(COGemojis[key])
                )
            )
            
        super().__init__(
            placeholder="Choose a category.",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        label = interaction.values[0]

        if label not in self.data: 
            embed = await self.utils.main_help_embed(self.ctx)
            return await interaction.response.edit_message(embed=embed, view=self.view)
        
        cog = self.ctx.bot.get_cog(label)
        embed = await self.utils.specific_cog(cog, self.ctx)

        if interaction.author == self.ctx.author:
            return await interaction.response.edit_message(embed=embed, view=self.view)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class DropdownView(disnake.ui.View):    
    def __init__(self, data, ctx:commands.Context, utils):
        super().__init__(
            timeout=None
        )
        self.add_item(Dropdown(data, ctx, utils))

        
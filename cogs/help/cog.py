import json
import typing

import disnake
from disnake.ext import commands

from core import Context, JesterBot
from core.constants import (
    CATEGORIES, COG_DESCRIPTIONS, COG_EMOJIS, E_, J_, LINK, R_, S_, T_
)
from core.utils import get_colour

from . import DropdownView


def get_help(command: str) -> str:
    with open("./dicts/Cmds.json") as fp:
        data = json.load(fp)
    try:
        help = data[command]["help"].capitalize()
        return help
    except KeyError:
        return "No help"


class HelpUtils:
    links = "> [Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot) │ [Vote for me!](https://top.gg/bot/828363172717133874/vote)"

    def __init__(self, bot: JesterBot):
        self.bot = bot

    async def get_cog_from_str(self, cog_name: str) -> typing.Optional[commands.Cog]:
        cog_name = cog_name.lower()

        for k in self.bot.cogs:
            if k.lower() == cog_name:
                return self.bot.get_cog(k)
        return None

    async def main_help_embed(self, ctx: Context) -> disnake.Embed:
        description = f"\n```ml\n[] - Required Argument | <> - Optional Argument``````diff\n+ Use the dropbar to navigate through Categories``````diff\n+ Use {ctx.prefix}help prefix for info about the prefix```"
        cogs = [
            f">  {self.bot.get_emoji(COG_EMOJIS[k])} **{k}** `({len([e for e in self.bot.get_cog(k).walk_commands() if not e.hidden])})`"
            for k in self.bot.cogs
            if k in COG_DESCRIPTIONS
        ]

        return (
            disnake.Embed(
                title=f"{J_}{E_}{S_}{T_}{E_}{R_}",
                description=description,
                timestamp=ctx.message.created_at,
                colour=get_colour(),
            )
            .add_field(
                name=f"{CATEGORIES} **Categories:**\n\u200b",
                value="\n".join(cogs[i] for i in range(0, len(cogs), 2)) + "\n\u200b",
            )
            .add_field(
                name="\u200b\n\u200b",
                value="\n".join(cogs[i] for i in range(1, len(cogs), 2)),
            )
            .add_field(name=f"{LINK} **Links:**", value=f"**{self.links}**", inline=False)
        )

    async def main_help(self, ctx: Context) -> None:
        embed = await self.main_help_embed(ctx)
        await ctx.reply(
            embed=embed, view=DropdownView(COG_DESCRIPTIONS, ctx, HelpUtils(self.bot))
        )

    async def specific_command(
        self, command: commands.Command, ctx: Context
    ) -> disnake.Embed:
        return (
            disnake.Embed(colour=get_colour())
            .add_field(
                name=" ❯❯ Name", value=f"`{command.name.capitalize()}`", inline=False
            )
            .add_field(
                name=" ❯❯ Alias",
                value=f"{', '.join(f'`{k}`' for k in command.aliases if command.aliases)} "
                if command.aliases
                else "`none`",
                inline=False,
            )
            .add_field(
                name=" ❯❯ Usage",
                value=f"`j.{command.name} {command.signature}`"
                if command.signature
                else f"`j.{command.name}`",
                inline=False,
            )
            .add_field(
                name=" ❯❯ Description",
                value=f"{get_help(command.name)}"
                if get_help(command.name)
                else "Currently no help!",
                inline=False,
            )
            .set_author(name="Help", icon_url=ctx.author.display_avatar.url)
            .set_footer(text="<> = needed │ [] = not needed")
        )

    async def specific_cog(self, cog: commands.Cog, ctx: Context) -> disnake.Embed:
        if cog.qualified_name not in COG_DESCRIPTIONS:
            return await self.no_command(ctx)

        commands = [f"- `{k.name}`" for k in cog.walk_commands() if not k.hidden]
        return (
            disnake.Embed(
                description=COG_DESCRIPTIONS[cog.qualified_name], colour=get_colour()
            )
            .set_author(
                name=f"{cog.qualified_name}", icon_url=ctx.author.display_avatar.url
            )
            .add_field(
                name="\u200b",
                value="\n".join(commands[i] for i in range(0, len(commands), 2)),
            )
            .add_field(
                name="\u200b",
                value="\n".join(commands[i] for i in range(1, len(commands), 2)),
            )
        )

    async def no_command(self, ctx: Context) -> disnake.Embed:
        message = ctx.message.content.replace(
            f"{ctx.prefix}{ctx.invoked_with} ", ""
        ).strip()
        commands = [
            f"- `{k.name}`"
            for k in self.bot.commands
            if k.name.startswith(message[0].lower()) and not k.hidden
        ]

        return (
            disnake.Embed(colour=get_colour())
            .set_author(
                name=f"{message} is not a command!",
                icon_url=ctx.author.display_avatar.url,
            )
            .add_field(
                name="\u200b",
                value="\n".join(commands[i] for i in range(0, len(commands), 2)) if commands else "-"
            )
            .add_field(
                name="\u200b",
                value="\n".join(commands[i] for i in range(1, len(commands), 2)) if commands else "-",
            )
        )


class Help(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot
        self.utils = HelpUtils(bot)

    @commands.command(
        aliases=["h", "commands", "cmd", "command", "?", "helpme", "helpcommand", "cmds"]
    )
    async def help(self, ctx: Context, command=None) -> None:
        if not command:
            embed = await self.utils.main_help_embed(ctx)
            return await ctx.reply(
                embed=embed, view=DropdownView(COG_DESCRIPTIONS, ctx, self.utils)
            )

        cog = await self.utils.get_cog_from_str(command)
        if cog:
            embed = await self.utils.specific_cog(cog, ctx)
            return await ctx.reply(embed=embed)

        cmd = self.bot.get_command(command)
        if cmd:
            embed = await self.utils.specific_command(cmd, ctx)
            return await ctx.reply(embed=embed)

        embed = await self.utils.no_command(ctx)
        return await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))

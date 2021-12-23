import disnake, json
from disnake.ext import commands

from core.utils.utils import Cmds
from core.utils.emojis import j, s, t, e, r, COGemojis, CATEGORIES, LINK
from core.utils.view import DropdownView

from core.Context import Context

class HelpUtils:
    links = "> [Official server](https://disnake.gg/2654CuU3ZU) │ [Bot invite](https://disnake.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot) │ [Vote for me!](https://top.gg/bot/828363172717133874/vote)"

    def __init__(self, bot):
        self.bot = bot
        with open('./dicts/Emoji.json') as k:
            self.data = json.load(k)

    async def main_help_embed(self, ctx:commands.Context) -> disnake.Embed:
        description = f"\n```ml\n[] - Required Argument | <> - Optional Argument``````diff\n+ Use the dropbar to navigate through Categories``````diff\n+ Use {ctx.prefix}help prefix for info about the prefix```"
        cogs = [f">  {self.bot.get_emoji(COGemojis[k])} **{k}**" for k in self.bot.cogs if k in self.data]

        return disnake.Embed(
            title=f"{j}{e}{s}{t}{e}{r}", 
            description=description,
            timestamp=ctx.message.created_at
        ).add_field(
            name=f"{CATEGORIES} **Categories:**\n\u200b", 
            value='\n'.join([cogs[i] for i in range(0, len(cogs), 2)]) + "\n\u200b"
        ).add_field(
            name="\u200b\n\u200b", 
            value='\n'.join([cogs[i] for i in range(1, len(cogs), 2)]),
        ).add_field(
            name=f"{LINK} **Links:**", 
            value=f"**{self.links}**", 
            inline=False
        ).set_footer(
            text=f"Expires in 5 minutes")

    async def main_help(self, ctx:commands.Context) -> None:
        embed = await self.main_help_embed(ctx)
        await ctx.send(embed=embed, view=DropdownView(self.data, ctx, HelpUtils(self.bot)))

    async def specific_command(self, command:commands.Command, ctx:commands.Context) -> disnake.Embed:
        return disnake.Embed(
            ).add_field(
                name=" ❯❯ Name", 
                value=f"`{command.name.capitalize()}`", 
                inline=False,
            ).add_field(
                name=" ❯❯ Alias", 
                value=f"{', '.join([f'`{k}`' for k in command.aliases if command.aliases])} " if command.aliases else f"`none`", 
                inline=False,
            ).add_field(
                name=" ❯❯ Usage", 
                value=f"`j.{command.name} {command.signature}`" if command.signature else f'`j.{command.name}`', 
                inline=False,
            ).add_field(
                name=" ❯❯ Description", 
                value=Cmds(command.name).chelp if Cmds(command.name).chelp else "Currently no help!", 
                inline=False,
            ).set_author(
                name="Help", 
                icon_url = ctx.author.avatar.url,
            ).set_footer(
                text="<> = needed │ [] = not needed")

    async def specific_cog(self, cog:commands.Cog, ctx:commands.Context) -> disnake.Embed:
        if cog.qualified_name not in self.data:
            return self.no_command(ctx)

        commands = [f"- `{k.name}`" for k in cog.walk_commands() if not k.hidden]
        return disnake.Embed(
            description=self.data[cog.qualified_name],
            ).set_author(
                name=f"{cog.qualified_name}",
                icon_url=ctx.author.avatar.url,
            ).add_field(
                name="\u200b",
                value="\n".join([commands[i] for i in range(0, len(commands), 2)]),
            ).add_field(
                name="\u200b",
                value="\n".join([commands[i] for i in range(1, len(commands), 2)]),
            )

    async def no_command(self, ctx:commands.Context) -> disnake.Embed:
        message = ctx.message.content.replace(f"{ctx.prefix}{ctx.invoked_with} ", "").strip()
        commands = [f"- `{k.name}`" for k in self.bot.commands if k.name.startswith(message[0]) and not k.hidden]
        
        return disnake.Embed(
            description="**Did you mean:**\n" + '\n'.join(commands),
            ).set_author(
                name=f"{message} is not a command!",
                icon_url=ctx.author.avatar.url,
            )

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = HelpUtils(bot)
        with open('./dicts/Emoji.json') as k:
            self.data = json.load(k)

    @commands.command(
        aliases=['h', 'commands', 'cmd', 'command', '?', 'helpme', 'helpcommand', 'cmds']
        )
    async def help(self, ctx:Context, command=None) -> None:
        if not command:
            return await self.utils.main_help(ctx)
     
        cmd = self.bot.get_command(command)
        if cmd:
            embed = await self.utils.specific_command(cmd, ctx)
            return await ctx.send(embed=embed)

        cog = self.bot.get_cog(command.capitalize())
        if cog:
            embed = await self.utils.specific_cog(cog, ctx)
            return await ctx.send(embed=embed)

        embed = await self.utils.no_command(ctx)
        return await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Help(bot))

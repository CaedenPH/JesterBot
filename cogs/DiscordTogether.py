import discord

from discord import InvalidArgument
from discord.ext.commands import BotMissingPermissions
from discord.ext import commands
from discord.http import Route
from typing import Union
from core.utils.Error.exception import myException

defaultApplications = {
    'youtube': '755600276941176913',
    'poker': '755827207812677713',
    'betrayal': '773336526917861400',
    'fishing': '814288819477020702',
    'chess': '832012586023256104'
}

class DiscordTogetherUrlGen:
    def __init__(self, bot):
        self.bot = bot

    async def create_link(self, voiceChannelID: int, option: str) -> str:
        if not isinstance(voiceChannelID, (str,int)):
            raise TypeError(f"'voiceChannelID' parameter MUST be of type string or integer, not a \"{type(voiceChannelID).__name__}\" type.")
        if not isinstance(option, (str,int)):
            raise TypeError(f"'option' parameter MUST be of type string or integer, not a \"{type(option).__name__}\" type.")

        # Pre Defined Application ID
        if option and (str(option).lower().replace(" ", "") in defaultApplications.keys()):
            data = {
                'max_age': 86400,
                'max_uses': 0,
                'target_application_id': defaultApplications[str(option).lower().replace(" ","")],
                'target_type': 2,
                'temporary': False,
                'validate': None
            }

            try:
                result = await self.bot.http.request(Route("POST", f"/channels/{voiceChannelID}/invites"), json = data)
            except Exception as e:
                if "10003" in str(e):
                    raise myException.InvalidChannelID("Voice Channel ID is invalid.")
                elif "50013" in str(e):
                    raise BotMissingPermissions(["CREATE_LINK"])
                elif "130000" in str(e):
                    raise ConnectionError("API resource is currently overloaded. Try again a little later.")
                else:
                    raise ConnectionError("An error occurred while retrieving data from Discord API.")

            return f"https://discord.com/invite/{result['code']}"

        # User Defined Application ID
        elif option and (str(option).replace(" ", "") not in defaultApplications.keys()) and str(option).replace(" ","").isnumeric():
            data = {
                'max_age': 86400,
                'max_uses': 0,
                'target_application_id': str(option).replace(" ", ""),
                'target_type': 2,
                'temporary': False,
                'validate': None
            }

            try:
                result = await self.bot.http.request(Route("POST", f"/channels/{voiceChannelID}/invites"), json = data)
            except Exception as e:
                if "10003" in str(e):
                    raise myException.InvalidChannelID("Voice Channel ID is invalid.")
                elif "target_application_id" in str(e):
                    option = str(option).replace(" ", "")
                    raise InvalidArgument(f"\"{option}\" is an invalid custom application ID.")
                elif "50013" in str(e):
                    raise BotMissingPermissions(["CREATE_LINK"])
                elif "130000" in str(e):
                    raise ConnectionError("API resource is currently overloaded. Try again a little later.")
                else:
                    raise ConnectionError("An error occurred while retrieving data from Discord API.")

            return f"https://discord.com/invite/{result['code']}"
        else:
            raise myException.InvalidActivityChoice("Invalid activity option chosen. You may only choose between (\"youtube\",\"poker\",\"chess\",\"fishing\",\"betrayal\") or input a custom application ID as a string.")

class DiscordTogether(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.togetherControl = DiscordTogetherUrlGen(bot)

    @commands.command(name='yt_together')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def discord_together_youtube(self, ctx: commands.Context) -> discord.message.Message:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        return await ctx.send(f"Click the blue link!\n{link}", delete_after=60)

    @commands.command(name='poker_together')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def discord_together_poker(self, ctx: commands.Context) -> discord.message.Message:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'poker')
        return await ctx.send(f"Click the blue link!\n{link}", delete_after=60)

    @commands.command(name='chess_together')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def discord_together_chess(self, ctx: commands.Context) -> discord.message.Message:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'chess')
        return await ctx.send(f"Click the blue link!\n{link}", delete_after=60)

    @commands.command(name='betrayal_together')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def discord_together_betrayal(self, ctx: commands.Context) -> discord.message.Message:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal')
        return await ctx.send(f"Click the blue link!\n{link}", delete_after=60)

    @commands.command(name='fishing_together')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def discord_together_fishing(self, ctx: commands.Context) -> discord.message.Message:
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
        return await ctx.send(f"Click the blue link!\n{link}", delete_after=60)

def setup(bot):
    bot.add_cog(DiscordTogether(bot))
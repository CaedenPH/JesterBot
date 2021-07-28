import discord
from discord.ext import commands

from core.utils.utils import thecolor

class Context(commands.Context):
    

    async def em(self, message):
        return await self.send(
            embed = discord.Embed(
                description=message,
                color=thecolor() 
            )
        )

    async def send(self, content: any = None, **kwargs):
        perms = self.channel.permissions_for(self.me)
        if not perms.send_messages:
            try:
                await self.author.send(
                    "I can't send any messages in that channel. \nPlease give me sufficient permissions to do so."
                )
            except discord.Forbidden:
                pass
            return

        require_embed_perms = kwargs.pop("embed_perms", False)
        if require_embed_perms and not perms.embed_links:
            kwargs = {}
            content = (
                "Oops! I need **Embed Links** permission to work properly. \n"
                "Please tell a server admin to grant me that permission."
            )
        if isinstance(content, discord.Embed):
            kwargs["embed"] = content
            content = None
        if isinstance(content, discord.File):
            kwargs["file"] = content
            content = None

        return await super().send(content, **kwargs)
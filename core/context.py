import disnake
import asyncio

from disnake.ext import commands
from core.constants import TRASHCAN
from core.utils import get_colour


class Context(commands.Context):
    async def em(self, message, **kwargs):
        return await super().send(
            embed=disnake.Embed(description=message, colour=get_colour()), **kwargs
        )

    async def send(self, content: any = None, **kwargs):
        perms = self.channel.permissions_for(self.me)
        if not perms.send_messages:
            try:
                await self.author.send(
                    "I can't send any messages in that channel. \nPlease give me sufficient permissions to do so."
                )
            except disnake.Forbidden:
                pass
            return

        require_embed_perms = kwargs.pop("embed_perms", False)
        if require_embed_perms and not perms.embed_links:
            kwargs = {}
            content = (
                "Oops! I need **Embed Links** permission to work properly. \n"
                "Please tell a server admin to grant me that permission."
            )
        if isinstance(content, disnake.Embed):
            kwargs["embed"] = content
            content = None
        if isinstance(content, disnake.File):
            kwargs["file"] = content
            content = None

        msg = await super().send(content, **kwargs)
        self.bot.data[self.message] = {"bot": msg}
        try:

            async def reaction_task(msg, arg, kwargs):
                def check(r, u):
                    return r.message == msg and u == arg.author

                await asyncio.sleep(3)
                try:

                    await msg.add_reaction(TRASHCAN)
                except Exception as a:
                    return

                try:
                    r, u = await arg.bot.wait_for(
                        "reaction_add", check=check, timeout=250
                    )
                    if str(r.emoji.id) == TRASHCAN[11:-1]:
                        await msg.delete()
                except Exception as b:
                    try:
                        await msg.clear_reactions()
                    except Exception as c:
                        pass

            loop = asyncio.get_running_loop()
            loop.create_task(reaction_task(msg, self, kwargs))
        except:
            pass
        return msg

    async def reply(self, content: any = None, **kwargs):
        perms = self.channel.permissions_for(self.me)
        if not perms.send_messages:
            try:
                await self.author.send(
                    "I can't send any messages in that channel. \nPlease give me sufficient permissions to do so."
                )
            except disnake.Forbidden:
                pass
            return

        require_embed_perms = kwargs.pop("embed_perms", False)
        if require_embed_perms and not perms.embed_links:
            kwargs = {}
            content = (
                "Oops! I need **Embed Links** permission to work properly. \n"
                "Please tell a server admin to grant me that permission."
            )
        if isinstance(content, disnake.Embed):
            kwargs["embed"] = content
            content = None
        if isinstance(content, disnake.File):
            kwargs["file"] = content
            content = None

        msg = await super().reply(content, **kwargs)
        self.bot.data[self.message] = {"bot": msg}
        try:

            async def reaction_task(msg, arg, kwargs):
                def check(r, u):
                    return r.message == msg and u == arg.author

                await asyncio.sleep(3)
                try:
                    await msg.add_reaction(TRASHCAN)
                except Exception as a:
                    return

                try:
                    r, u = await arg.bot.wait_for(
                        "reaction_add", check=check, timeout=250
                    )
                    if str(r.emoji.id) == TRASHCAN[11:-1]:
                        await msg.delete()
                except Exception as b:
                    try:
                        await msg.clear_reactions()
                    except Exception as c:
                        pass

            loop = asyncio.get_running_loop()
            loop.create_task(reaction_task(msg, self, kwargs))
        except:
            pass
        return msg

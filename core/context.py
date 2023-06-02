from __future__ import annotations

import asyncio
import inspect
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import disnake
import disnake.abc
import disnake.utils
from disnake.ext.commands import Command, Context, view
from disnake.message import Message

from core.constants import TRASHCAN
from core.utils import get_colour

if TYPE_CHECKING:
    from disnake.state import ConnectionState

    from core.bot import JesterBot

MISSING: Any = disnake.utils.MISSING


class Context(Context):
    def __init__(
        self,
        *,
        message: Message,
        bot: JesterBot,
        view: view.StringView,
        args: List[Any] = MISSING,
        kwargs: Dict[
            str,
            Any,
        ] = MISSING,
        prefix: Optional[str] = None,
        command: Optional[Command] = None,
        invoked_with: Optional[str] = None,
        invoked_parents: List[str] = MISSING,
        invoked_subcommand: Optional[Command] = None,
        subcommand_passed: Optional[str] = None,
        command_failed: bool = False,
        current_parameter: Optional[inspect.Parameter] = None,
    ):
        self.message: Message = message
        self.bot: JesterBot = bot
        self.args: List[Any] = args or []
        self.kwargs: Dict[
            str,
            Any,
        ] = (
            kwargs or {}
        )
        self.prefix: Optional[str] = prefix
        self.command: Optional[Command] = command
        self.view: view.StringView = view
        self.invoked_with: Optional[str] = invoked_with
        self.invoked_parents: List[str] = invoked_parents or []
        self.invoked_subcommand: Optional[Command] = invoked_subcommand
        self.subcommand_passed: Optional[str] = subcommand_passed
        self.command_failed: bool = command_failed
        self.current_parameter: Optional[inspect.Parameter] = current_parameter
        self._state: ConnectionState = self.message._state

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
                except Exception:
                    return

                try:
                    (r, u) = await arg.bot.wait_for(
                        "reaction_add", check=check, timeout=250
                    )
                    if str(r.emoji.id) == TRASHCAN[11:-1]:
                        await msg.delete()
                except Exception:
                    try:
                        await msg.clear_reactions()
                    except Exception:
                        pass

            loop = asyncio.get_running_loop()
            loop.create_task(reaction_task(msg, self, kwargs))
        except Exception:
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
                except Exception:
                    return

                try:
                    (r, u) = await arg.bot.wait_for(
                        "reaction_add", check=check, timeout=250
                    )
                    if str(r.emoji.id) == TRASHCAN[11:-1]:
                        await msg.delete()
                except Exception:
                    try:
                        await msg.clear_reactions()
                    except Exception:
                        pass

            loop = asyncio.get_running_loop()
            loop.create_task(reaction_task(msg, self, kwargs))
        except Exception:
            pass
        return msg

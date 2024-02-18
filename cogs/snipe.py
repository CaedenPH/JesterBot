import random
import time
import typing as t
from datetime import datetime

import disnake
from disnake.ext import commands

from core import Context, JesterBot
from core.constants import CLOSE
from core.utils import get_colour, send_embed


class Snipe(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot

    async def getch_user(self, user_id: int) -> t.Optional[disnake.User]:
        user = self.bot.get_user(user_id)
        if user:
            return user

        try:
            user = await self.bot.fetch_user(user_id)
        except disnake.HTTPException:
            pass
        return user or None

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if message.author.bot:
            return

        await self.bot.db.update(
            "INSERT INTO snipe VALUES (?, ?, ?, ?, ?)",
            (
                message.id,
                message.channel.id,
                message.author.id,
                message.content or message.attachments[0].url,
                time.time(),
            ),
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if before.author.bot:
            return
        if before.content == after.content:
            return

        await self.bot.db.update(
            "INSERT INTO edit_snipe VALUES (?, ?, ?, ?, ?, ?)",
            (
                random.randint(100000000, 100000000000),
                before.channel.id,
                before.author.id,
                before.content or before.attachments[0].url,
                after.content or after.attachments[0].url,
                time.time(),
            ),
        )

    @commands.command()
    async def snipe(self, ctx: Context, amount: int = 0):
        results = (
            await self.bot.db.fetchall(
                "SELECT * FROM snipe WHERE channel_id = ?", (ctx.channel.id,)
            )
        )[::-1]
        if not results:
            m = await send_embed(
                ctx, "Snipe", f"> No deleted messages found in {ctx.channel.mention}."
            )
            return await m.add_reaction(CLOSE)
        if amount >= len(results):
            m = await send_embed(
                ctx, "Snipe", f"> I found no messages {amount} deletes ago."
            )
            return await m.add_reaction(CLOSE)

        result = results[amount]
        user = await self.getch_user(result[2])

        embed = disnake.Embed(
            description=f"""
Message in: {ctx.channel.mention}
Message from: {user.mention}
Message deleted at: {disnake.utils.format_dt(datetime.fromtimestamp(result[4]))}
```yaml
{result[3]}
```
""",
            colour=get_colour(),
        ).set_thumbnail(url=user.display_avatar.url or ctx.author.default_avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def aim(self, ctx: Context, user: disnake.Member = None):
        if user is None:
            user = ctx.author

        results = (
            await self.bot.db.fetchall(
                "SELECT * FROM snipe WHERE channel_id = ? and user_id = ?",
                (ctx.channel.id, user.id),
            )
        )[::-1]
        if not results:
            m = await send_embed(
                ctx,
                "Snipe",
                f"> No deleted messages from {user.mention} found in {ctx.channel.mention}.",
            )
            return await m.add_reaction(CLOSE)

        result = results[0]
        user = await self.getch_user(result[2])

        embed = disnake.Embed(
            description=f"""
Message in: {ctx.channel.mention}
Message from: {user.mention}
Message deleted at: {disnake.utils.format_dt(datetime.fromtimestamp(result[4]))}
```yaml
{result[3]}
```
""",
            colour=get_colour(),
        ).set_thumbnail(url=user.display_avatar.url or ctx.author.default_avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=["esnipe"])
    async def editsnipe(self, ctx: Context, amount: int = 0):
        results = (
            await self.bot.db.fetchall(
                "SELECT * FROM edit_snipe WHERE channel_id = ?", (ctx.channel.id,)
            )
        )[::-1]
        if not results:
            m = await send_embed(
                ctx,
                "Edit Snipe",
                f"> No edited messages found in {ctx.channel.mention}.",
            )
            return await m.add_reaction(CLOSE)
        if amount >= len(results):
            m = await send_embed(
                ctx, "Edit Snipe", f"> I found no messages {amount} edits ago."
            )
            return await m.add_reaction(CLOSE)

        result = results[amount]
        user = await self.getch_user(result[2])

        embed = disnake.Embed(
            description=f"""
Message in: {ctx.channel.mention}
Message from: {user.mention}
Message edited at: {disnake.utils.format_dt(datetime.fromtimestamp(result[5]))}
```yaml
{result[3]}
```
changed to:
```yaml
{result[4]}
```
""",
            colour=get_colour(),
        ).set_thumbnail(url=user.display_avatar.url or ctx.author.default_avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=["eaim"])
    async def editaim(self, ctx: Context, user: disnake.Member = None):
        if user is None:
            user = ctx.author

        results = (
            await self.bot.db.fetchall(
                "SELECT * FROM edit_snipe WHERE channel_id = ? and user_id = ?",
                (ctx.channel.id, user.id),
            )
        )[::-1]
        if not results:
            m = await send_embed(
                ctx,
                "Snipe",
                f"> No deleted messages from {user.mention} found in {ctx.channel.mention}.",
            )
            return await m.add_reaction(CLOSE)

        result = results[0]
        user = await self.getch_user(result[2])

        embed = disnake.Embed(
            description=f"""
Message in: {ctx.channel.mention}
Message from: {user.mention}
Message edited at: {disnake.utils.format_dt(datetime.fromtimestamp(result[5]))}
```yaml
{result[3]}
```
changed to:
```yaml
{result[4]}
```
""",
            colour=get_colour(),
        ).set_thumbnail(url=user.display_avatar.url or ctx.author.default_avatar)
        await ctx.send(embed=embed)


def setup(bot: JesterBot) -> None:
    bot.add_cog(Snipe(bot))

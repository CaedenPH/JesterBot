import discord_together
from disnake.ext import commands

from core import Context, JesterBot
from core.constants import BOT_TOKEN


class DiscordTogether(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot
        self.together_control = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.together_control = await discord_together.DiscordTogether(BOT_TOKEN)

    @commands.command(aliases=["yt_together"])
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def youtube_together(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "youtube"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def poker_together(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "poker"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def chess_together(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "chess"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def betrayal_together(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "betrayal"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def fishing_together(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "fishing"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def awkword(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "awkword"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def spellcast(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "spellcast"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def doodle_crew(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "doodle-crew"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def word_snack(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "word-snack"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def letter_tile(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "letter-tile"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def checkers(self, ctx: Context):
        if ctx.author.voice is None:
            return await ctx.em("You need to be in a voice channel!")
        link = await self.together_control.create_link(
            ctx.author.voice.channel.id, "checkers"
        )
        await ctx.reply(f"Click the blue link\n{link}", delete_after=60)


def setup(bot):
    bot.add_cog(DiscordTogether(bot))

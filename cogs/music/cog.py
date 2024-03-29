import disnake
from disnake.ext import commands

from core.context import Context
from core.utils import get_colour, send_embed

from . import dcutils


async def embed2(ctx, description) -> disnake.Message:
    embed = disnake.Embed(description=description, colour=get_colour())
    embed.set_footer(text="Type j.help Music to get all the music commands.")
    embed.set_author(name="Music", icon_url=ctx.author.display_avatar.url)

    return await ctx.reply(embed=embed)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music = dcutils.Music()

    @commands.command()
    async def lyrics(self, ctx: Context, *, song):
        async with self.bot.client.get(
            url=f"https://some-random-api.ml/lyrics?title={song}"
        ) as response:
            fox = await response.json()
            await send_embed(ctx, f'Lyrics of {fox["title"]}', fox["lyrics"])

    @commands.command()
    async def join(self, ctx: Context):
        if not ctx.author.voice:
            return await embed2(ctx, "You are not in a music channel.")

        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await voice_channel.connect()
            return await embed2(ctx, "Joined")
        else:
            if ctx.voice_client.channel == voice_channel:
                return await embed2(ctx, "I am already here.")
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def leave(self, ctx: Context):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            return await ctx.message.add_reaction("🎵")
        await embed2(ctx, "I am not in a music channel.")

    @commands.command()
    async def play(self, ctx: Context, *, url):
        if not ctx.author.voice:
            return await embed2(ctx, "You are not in a music channel.")

        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await voice_channel.connect()

        player = self.music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            await embed2(
                ctx,
                f"**Playing:** {song.name} \n**Duration**: {round(song.duration / 60)} minutes",
            )
        else:
            song = await player.queue(url, search=True)
            await embed2(ctx, f"**Queued:** {song.name}")

    @commands.command()
    async def pause(self, ctx: Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await embed2(ctx, "You are not playing any music.")

        song = await player.pause()
        await embed2(ctx, f"**Paused:** {song.name}")

    @commands.command()
    async def resume(self, ctx: Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await embed2(ctx, f"**Resumed:** {song.name}")

    @commands.command()
    async def stop(self, ctx: Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await embed2(ctx, "You are not playing any music.")

        await player.stop()
        await embed2(ctx, "Stopped")

    @commands.command()
    async def loop(self, ctx: Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        if not player:
            return await embed2(ctx, "You are not playing any music.")

        song = await player.toggle_song_loop()
        if song.is_looping:
            await embed2(ctx, f"**Enabled loop for:** {song.name}")
        else:
            await embed2(ctx, f"**Disabled loop for:** {song.name}")

    @commands.command()
    async def queue(self, ctx: Context):
        x = []
        z = 0
        player = self.music.get_player(guild_id=ctx.guild.id)

        for song in player.current_queue():
            if z == 0:
                x.append(f"**{z}**: {song.name} - {round(song.duration / 60)}m")
            else:
                x.append(f"\n**{z}**: {song.name}- {round(song.duration / 60)}m")
            z += 1

        await embed2(ctx, f"{', '.join(x)}")

    @commands.command()
    async def nowplaying(self, ctx: Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await embed2(ctx, song.name)

    @commands.command()
    async def skip(self, ctx: Context):
        z = 0

        player = self.music.get_player(guild_id=ctx.guild.id)
        for song in player.current_queue():
            if z == 0:
                song1 = song.name
            elif z == 1:
                song2 = song.name
            z += 1
        await embed2(ctx, f"**Skipped from:** *{song1}* **To:** \n*{song2}*")

    @commands.command()
    async def volume(self, ctx: Context, vol: str):
        player = self.music.get_player(guild_id=ctx.guild.id)
        (song, volume) = await player.change_volume(
            float(vol) / 100
        )  # volume should be a float between 0 to 1
        await embed2(ctx, f"**Changed volume for:** *{song.name}* **to {volume*100}**%")

    @commands.command()
    async def remove_song(self, ctx: Context, index):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await embed2(ctx, f"**Removed:** {song.name} from queue")


def setup(client):
    client.add_cog(Music(client))

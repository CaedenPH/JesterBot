import discord
from discord.ext import commands
import youtube_dl

from core.utils import dcutils
from core.utils.utils import thecolor, Json, thebed
from core.Context import Context

import re
import requests

async def embed2(ctx, description):

    embed = discord.Embed(description=description, color=thecolor())
    embed.set_footer(text='Type j.help Music to get all the music commands!')
    embed.set_author(name="Music", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music = dcutils.Music()

    @commands.command()
    async def lyrics(self, ctx:Context, *, song):

        response = requests.get(f"https://some-random-api.ml/lyrics?title={song}")
        fox = response.json()
        await thebed(ctx, f'Lyrics of {fox["title"]}', fox['lyrics'])

    @commands.command()
    async def join(self, ctx:Context):

        if not ctx.author.voice:
            return await embed2(ctx, 'You are not in a music channel!')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_bot is None:
            await voice_channel.connect()
            return await embed2(ctx, 'Joined')
        else:
            if ctx.voice_bot.channel == voice_channel:
                return await embed2(ctx, 'Already here!')
            await ctx.voice_bot.move_to(voice_channel)

    @commands.command()
    async def leave(self, ctx:Context):
        if ctx.voice_bot:

            await ctx.voice_bot.disconnect()
            return await ctx.message.add_reaction('🎵')
        await embed2(ctx, 'I am not in a music channel!')

    @commands.command()
    async def play(self, ctx:Context, *, url):
        if not ctx.author.voice:
            return await embed2(ctx, 'You are not in a music channel!')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_bot is None:
            await voice_channel.connect()
            
        player = self.music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_bot.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            await embed2(ctx, f"**Playing:** {song.name} \n**Duration**: {round(song.duration / 60)} minutes")
        else:
            song = await player.queue(url, search=True)
            await embed2(ctx, f"**Queued:** {song.name}")

    @commands.command()
    async def pause(self, ctx:Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        await embed2(ctx, f"**Paused:** {song.name}")

    @commands.command()
    async def resume(self, ctx:Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await embed2(ctx, f"**Resumed:** {song.name}")

    @commands.command()
    async def stop(self, ctx:Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await embed2(ctx, "Stopped")

    @commands.command()
    async def loop(self, ctx:Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await embed2(ctx, f"**Enabled loop for:** {song.name}")
        else:
            await embed2(ctx, f"**Disabled loop for:** {song.name}")

    @commands.command()
    async def queue(self, ctx:Context):
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
    async def nowplaying(self, ctx:Context):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await embed2(ctx, song.name)

    @commands.command()
    async def skip(self, ctx:Context):
        z = 0

        player = self.music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        for song in player.current_queue():
            if z == 0:
                song1 = song.name
            elif z == 1:
                song2 = song.name
            z += 1
        await embed2(ctx, f"**Skipped from:** *{song1}* **To:** \n*{song2}*")

    @commands.command()
    async def volume(self, ctx:Context, vol):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
        await embed2(ctx, f"**Changed volume for:** *{song.name}* **to {volume*100}**%")

    @commands.command()
    async def remove(self, ctx:Context, index):
        player = self.music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await embed2(ctx, f"**Removed:** {song.name} from queue")
             
def setup(bot):
    bot.add_cog(Music(bot))
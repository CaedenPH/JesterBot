import discord, os, requests, json, asyncio
from discord.ext.commands import has_permissions
from discord.ext import commands 
from discord.utils import get
from discord.ext import tasks
from discord import Intents
from asyncio import sleep
import yfinance as yf
from traceback import print_exc
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial

from random import choice, randint
import io
import textwrap
import contextlib
from discord.ext.buttons import Paginator
from traceback import format_exception
import youtube_dl
# class Queue:
#     def __init__(self, guild):
#         self.guild = guild
#         if self.guild 
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', '--default-search': 'ytsearch'}      
    
def Json(pref, data1):
    pref.seek(0)  # set point at the beginning of the file
    pref.truncate(0)  # clear previous content
    pref.write(json.dumps(data1, indent=4)) # write to file
async def embed1(ctx, title, description=""):
    embed = discord.Embed(title=title, color=xz)
    if description:

        embed = discord.Embed(title=title, description=description, color=xz)
    await ctx.send(embed=embed)
async def embed2(ctx, description):
   
    
    
    embed = discord.Embed(description=description, color=xz)
    embed.set_footer(text='Type help music to get all the music commands!')
    embed.set_author(name="Music", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
class TheColor:
    
    def __init__(self):
        
        with open('./dicts/Color.json', 'r') as k:
            data = json.load(k)
            self.color = data['Color']['color'] 
    
    
xz = int(TheColor().color, 16)

class Music(commands.Cog):
    def __init__(self, client):

        self.client = client
    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice:
            return await embed2(ctx, 'You are not in a music channel!')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            return await embed2(ctx, 'Joined')
        else:
            if ctx.voice_client.channel == voice_channel:
                return await embed2(ctx, 'Already here!')
            await ctx.voice_client.move_to(voice_channel)
        
    @commands.command(aliases=['leave'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction('🎵')

    @commands.command()
    async def play(self, ctx, url):
        with open('./dicts/Music.json', 'r+') as k:
            data = json.load(k)
            g = str(ctx.guild.id)
            #ctx.voice_client.stop()
            
            vc = ctx.voice_client
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                
                if not url.startswith('https:'):
                    
                    url = "ytsearch:" + url
                    info = ydl.extract_info(url, download=False)
                    url2 = info['entries'][0]['formats'][0]['url']
                    title = info['entries'][0]['title'] 
                else:
                    
                    info = ydl.extract_info(url, download=False)
                    url2 = info['formats'][0]['url']
                    title=info['title']
                
                source = await discord.FFmpegOpusAudio.from_probe(url2, 
                **FFMPEG_OPTIONS)
                if g in data:
                    data[g]['url'].append(url2)
                    data[g]['name'].append(title)
                else:
                    data[g] = {
                        'url': [url2],
                        'name': [title]
                    }
                Json(k, data)
                if vc.is_playing():
                    await embed2(ctx, 'Added to queue')
                    
                    while vc.is_playing:
                        pass
                    else:

                        vc.play(source)
                        await embed2(ctx, f'**Playing:** {title}')
                else:
                    vc.play(source)
                    await embed2(ctx, f'**Playing:** {title}')
    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await embed1(ctx, 'Music', 'Paused')    
    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await embed2(ctx, 'Resumed')
            
    @commands.command()
    async def queue(self, ctx):
        with open('./dicts/Music.json') as k:
            data = json.load(k)
            g = str(ctx.guild.id)
            if g in data:
                b = "\n".join(data[g]["name"])
                await embed2(ctx, f'**Your queue is currently:** *{b}*')
            else:
                await embed2(ctx, 'No queue!')
    @commands.command()
    async def loop(self, ctx):     
        ctx.voice_client.loop()
        await embed2(ctx, 'Looped')
    @commands.command(aliases=['delq', 'deleteq'])
    async def deletequeue(self, ctx):
        with open('./dicts/Music.json', 'r+') as k:
            data = json.load(k)
            g = str(ctx.guild.id)
            if g in data:
                del data[g]
                Json(k, data)
                await embed2(ctx, 'Deleted queue!')
    @commands.command()
    async def skip(self, ctx):
        with open('./dicts/Music.json', 'r+') as k:
            data = json.load(k)
            g = str(ctx.guild.id)
            if g in data:
                
                
                source = await discord.FFmpegOpusAudio.from_probe(data[g]['url'][1], 
                **FFMPEG_OPTIONS)
                ctx.voice_client.play(source)
                data[g]['url'].remove(0)
                Json(k, data)
                await embed2(ctx, 'Skipped')



    

def setup(client):
  client.add_cog(Music(client))

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
from youtube_dl import YoutubeDL
from random import choice, randint
import vacefron

vace_api = vacefron.Client()

class TheColor:
    def __init__(self):
        
        with open('./dicts/Color.json', 'r') as k:
            data = json.load(k)
            self.color = data['Color']['color'] 
    
xz = int(TheColor().color, 16)
class Images(commands.Cog):
    def __init__(self, client):
   

        self.client = client
    @commands.command(aliases=['change', 'changemind', 'change_my_mind'])
    async def mindchange(self, ctx, *, text:str=None):
        async with ctx.typing():
            embed = discord.Embed(title="Change my mind...", colour=xz)
            x = await vace_api.change_my_mind(text)
            embed.set_image(url=x.url)
            
            await ctx.send(embed=embed)
    @commands.command()
    async def nasapic(self, ctx):
        f = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=1")
        up = f.json()
        
        
         
        embed = discord.Embed(title='Nasapic', description=f'''
        **date:** {up[0]['date']} │
        **explanation:** {up[0]['explanation']}


        ''', color=xz
        )
        embed.set_image(url=up[0]['hdurl'])
        await ctx.send(embed=embed)

    @commands.command()
    async def rover(self, ctx):
        params = {"api_key":"zpru323jYkrSB0JNjZZMU6qv3bntIcZdVf5EpqK5"}
        f = r"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?"
        data = requests.get(f, params = params)
        fox = data.json()
        print(fox)
        for t in fox['photos']:
            print(t)
        embed = discord.Embed(title='Rover', color=xz)
        embed.set_image(url=fox['photos'])
        await ctx.send(embed=embed)
    @commands.command(invoke_without_command=True, help="Sends certain images of animals such as `dog`, `fox`, `cat`, to get the full list type `^image`", aliases=['imag', 'images', 'pic', 'pics'])
    async def image(self, ctx, imag=""):
        
        if imag not in ['cat', 'dog', 'panda', 'koala', 'fox', 'racoon', 'kangaroo']:
            embed = discord.Embed(title=f"{imag} is not a valid option" if imag else "Options", description="Valid Options are `cat`, `dog`, `panda`, `koala`, `fox`, `racoon`, `kangaroo`", colour=xz)
            await ctx.send(embed=embed)
        else:

            async with ctx.typing():

                
                animal = Animals(imag)
                
                embed = discord.Embed(title=f"Here is your {imag}", description=f"**Fact:**\n{animal.fact()}", colour=xz)
                embed.set_image(url=animal.image())
            await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Images(client))
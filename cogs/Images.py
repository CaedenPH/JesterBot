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
from animals import Animals
from dutils import thecolor, Json, thebed
import aiohttp
import dislash
vace_api = vacefron.Client()

class Images(commands.Cog):
    def __init__(self, client):
   

        self.client = client
    @commands.command()
    async def dir(self, ctx, *, c:object):
        await ctx.send(dir(c))
    @commands.command(hidden=True)
    async def ditest(self, ctx):
     

        msg = await ctx.send('hi', components=[dislash.Button(label='hello', custom_id='test', style=dislash.ButtonStyle.green)])
        def check(inter):
            return inter.message.id == msg.id and inter.author == ctx.author
        inter = await ctx.wait_for_button_click(check)
       
        await inter.reply(type=dislash.InteractionType.Acknowledge)
    @commands.command(aliases=['change', 'changemind', 'change_my_mind'])
    async def mindchange(self, ctx, *, text:str=None):
        async with ctx.typing():
            embed = discord.Embed(title="Change my mind...", colour=thecolor())
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


        ''', color=thecolor()
        )
        embed.set_image(url=up[0]['hdurl'])
        await ctx.send(embed=embed)

    @commands.command()
    async def rover(self, ctx):
        key2 = "dS9ecIIo07Q0gGLYXnCoJW6uCAKwDM9j0UnYbVre"
        async with aiohttp.ClientSession().get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key={}".format(key2)) as resp:
            response = await resp.json()
            await ctx.send(response)
    @commands.command(aliases=['rpic', 'randpic'])
    async def randompicture(self, ctx):
        async with ctx.typing():
            response = requests.get(f"https://source.unsplash.com/random")
            my_file = open('./images/random.png', 'wb')
            my_file.write(response.content)
            my_file.close()

        await ctx.send(file=discord.File('./images/random.png')) 
    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession().get("https://some-random-api.ml/meme") as resp:
            response = await resp.json()
            await ctx.send(response['image'])
    @commands.command(description="""Sends a wasted filtered avatar""")
    async def wasted(self, ctx, member: discord.Member=None):
       
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/wasted?avatar={avatar}")
            
            file = open('./images/wasted.png', 'wb')
            file.write(response.content)
            file.close()    
        await ctx.send(file=discord.File('./images/wasted.png'))
    @commands.command(description="""Sends a wasted filtered avatar""")
    async def threshold(self, ctx, member: discord.Member=None):
       
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/threshold/?avatar={avatar}")
            
            file = open('./images/threshold.png', 'wb')
            file.write(response.content)
            file.close()    
            await ctx.send(file=discord.File('./images/threshold.png'))        
    @commands.command()
    async def hornypass(self, ctx, member=None):
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/horny?avatar={avatar}")
            
            file = open('./images/hornypass.png', 'wb')
            file.write(response.content)
            file.close()    
        await ctx.send(file=discord.File('./images/hornypass.png'))   
        
    @commands.command(description="""Sends a fay filtered avatar""")
    async def gay(self, ctx, member:discord.Member=None):
        
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/gay?avatar={avatar}")
            file = open('./images/gay.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/gay.png')) 
            

    @commands.command(description="""Sends a glass filtered avatar""")
    async def glass(self, ctx, member:discord.Member=None):
        
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/glass?avatar={avatar}")
            file = open('./images/glass.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/glass.png')) 
            

    @commands.command(description="""Sends a triggered filtered avatar""")
    async def triggered(self, ctx, member:discord.Member=None):
       
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/triggered?avatar={avatar}")
            file = open('./images/triggered.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/triggered.png')) 
            

    @commands.command(description="""Sends a bloody filtered avatar""")
    async def bloody(self, ctx, member:discord.Member=None):
       
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/red?avatar={avatar}")
            file = open('./images/bloody.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/bloody.png')) 
        

    @commands.command(description="""Sends a YouTube comment with your custom comment""")
    async def ytcomment(self, ctx, *, comment):
       
        
        
       
        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar_url_as(format='png')}&comment={comment}&username={ctx.author.display_name}")
            file = open('./images/yt-comment.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/yt-comment.png'))
            

    @commands.command(description="""Makes a bright filtered avatar""")
    async def bright(self, ctx, member:discord.Member=None):
        
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/brightness?avatar={avatar}")
            file = open('./images/brightness.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/brightness.png')) 
            
    @commands.command(description="""Makes a bright filtered avatar""")
    async def invert(self, ctx, member:discord.Member=None):
        
        if member is None:
            avatar = ctx.author.avatar_url_as(format='png')
        else:
            avatar = member.avatar_url_as(format='png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/invert?avatar={avatar}")
            file = open('./images/invert.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/invert.png')) 
            
    @commands.command(description="""Makes a bright filtered avatar""")
    async def colorview(self, ctx, hexcolor):
        
       
        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/colorviewer?hex={hexcolor}")
            file = open('./images/color.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/color.png')) 
  


    @commands.command(aliases=['pic', 'imag', 'images', 'image'])
    async def picture(self, ctx, *, pic):
        
        async with ctx.typing():
            response = requests.get('https://source.unsplash.com/1600x900/?{}'.format(pic))
            my_file = open('./images/picture.png', 'wb')
            my_file.write(response.content)
            my_file.close()
                
        await ctx.send(file=discord.File('./images/picture.png')) 

    @commands.command(invoke_without_command=True, description="Sends certain images of animals such as `dog`, `fox`, `cat`, to get the full list type `^image`", aliases=['animalpic', 'animage'])
    async def animalimage(self, ctx, imag=""):
        
        if imag not in ['cat', 'dog', 'panda', 'koala', 'fox', 'racoon', 'kangaroo']:
            embed = discord.Embed(title=f"{imag} is not a valid option" if imag else "Options", description="Valid Options are `cat`, `dog`, `panda`, `koala`, `fox`, `racoon`, `kangaroo`", colour=thecolor())
            await ctx.send(embed=embed)
        else:

            async with ctx.typing():

                
                animal = Animals(imag)
                
                embed = discord.Embed(title=f"Here is your {imag}", description=f"**Fact:**\n{animal.fact()}", colour=thecolor())
                embed.set_image(url=animal.image())
        await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Images(client))
import discord, os, requests, json, asyncio
from discord.ext import commands 
from random import choice, randint
import vacefron
from animals import Animals
from core.utils.utils import thecolor, Json, thebed
from core.Context import Context

import aiohttp
vace_api = vacefron.Client()

class Images(commands.Cog):
    def __init__(self, bot):
   

        self.bot = bot
    
    
    @commands.command(aliases=['change', 'changemind', 'change_my_mind'])
    async def mindchange(self, ctx:Context, *, text:str=None):
        async with ctx.typing():
            embed = discord.Embed(title="Change my mind...", colour=thecolor())
            x = await vace_api.change_my_mind(text)
            embed.set_image(url=x.url)
            
            await ctx.send(embed=embed)

    @commands.command()
    async def nasapic(self, ctx:Context):
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
    async def rover(self, ctx:Context):
        key2 = "dS9ecIIo07Q0gGLYXnCoJW6uCAKwDM9j0UnYbVre"
        async with aiohttp.ClientSession().get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key={}".format(key2)) as resp:
            response = await resp.json()
            await ctx.send(response)

    @commands.command(aliases=['rpic', 'randpic'])
    async def randompicture(self, ctx:Context):
        async with ctx.typing():
            response = requests.get(f"https://source.unsplash.com/random")
            my_file = open('./images/random.png', 'wb')
            my_file.write(response.content)
            my_file.close()

        await ctx.send(file=discord.File('./images/random.png')) 

    @commands.command()
    async def meme(self, ctx:Context):
        async with aiohttp.ClientSession().get("https://some-random-api.ml/meme") as resp:
            response = await resp.json()
            await ctx.send(response['image'])

    @commands.command(description="""Sends a wasted filtered avatar""")
    async def wasted(self, ctx:Context, member: discord.Member=None):
       
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
    async def threshold(self, ctx:Context, member: discord.Member=None):
       
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
    async def hornypass(self, ctx:Context, member=None):
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
    async def gay(self, ctx:Context, member:discord.Member=None):
        
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
    async def glass(self, ctx:Context, member:discord.Member=None):
        
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
    async def triggered(self, ctx:Context, member:discord.Member=None):
       
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
    async def bloody(self, ctx:Context, member:discord.Member=None):
       
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
    async def ytcomment(self, ctx:Context, *, comment):
       
        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar_url_as(format='png')}&comment={comment}&username={ctx.author.display_name}")
            file = open('./images/yt-comment.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/yt-comment.png'))

    @commands.command(description="""Makes a bright filtered avatar""")
    async def bright(self, ctx:Context, member:discord.Member=None):
        
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
    async def invert(self, ctx:Context, member:discord.Member=None):
        
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
    async def colorview(self, ctx:Context, hexcolor):

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/colorviewer?hex={hexcolor}")
            file = open('./images/color.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/color.png')) 

    @commands.command(aliases=['pic', 'imag', 'images', 'image'])
    async def picture(self, ctx:Context, *, pic):
        
        async with ctx.typing():
            response = requests.get('https://source.unsplash.com/1600x900/?{}'.format(pic))
            my_file = open('./images/picture.png', 'wb')
            my_file.write(response.content)
            my_file.close()
                
        await ctx.send(file=discord.File('./images/picture.png')) 

    @commands.command(invoke_without_command=True, description="Sends certain images of animals such as `dog`, `fox`, `cat`, to get the full list type `j.image`", aliases=['animalpic', 'animage'])
    async def animalimage(self, ctx:Context, imag=""):
        
        if imag not in ['cat', 'dog', 'panda', 'koala', 'fox', 'racoon', 'kangaroo']:
            embed = discord.Embed(title=f"{imag} is not a valid option" if imag else "Options", description="Valid Options are `cat`, `dog`, `panda`, `koala`, `fox`, `racoon`, `kangaroo`", colour=thecolor())
            return await ctx.send(embed=embed)
       

        async with ctx.typing():
            
            animal = Animals(imag)
            
            embed = discord.Embed(title=f"Here is your {imag}", description=f"**Fact:**\n{animal.fact()}", colour=thecolor())
            embed.set_image(url=animal.image())
        await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Images(bot))
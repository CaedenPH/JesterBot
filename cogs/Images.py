import discord, os, requests, json, asyncio, aiohttp
from discord.ext import commands 
from random import choice, randint
import vacefron, PIL
from animals import Animals
import cv2 as cv
from PIL import ImageEnhance

from core.utils.utils import thecolor, Json, thebed
from core.Context import Context



vace_api = vacefron.Client()

async def img(ctx, member, name):
    await ctx.trigger_typing()

    if member is None:
        member = ctx.author

    url = member.avatar.url

    if member.avatar.is_animated():
        url = member.avatar.url.replace('.gif', '.png')
        

    async with aiohttp.ClientSession() as s:
        async with s.get(str(url)) as r:
            f = open(f'./images/{name}.png', 'wb')
            f.write(await r.read())
            f.close()

    return f"./images/{name}.png"

async def pilimg(ctx, member, name):
    await ctx.trigger_typing()

    if member is None:
        member = ctx.author

    url:str = member.avatar.url

    if member.avatar.is_animated():
        
        url:str = str(member.avatar.url).replace('.gif', '.webp')
        print(url)

    path = f'./images/{name}.png'
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            f = open(path, 'wb')
            f.write(await r.read())
            f.close()

    with PIL.Image.open(path) as im:
        return im, path
class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def sharp(self, ctx, sharpness:float=10, member:discord.Member=None):
        x = await pilimg(ctx, member, 'sharp')
        enhancer = ImageEnhance.Sharpness(x[0])
        enhancer.enhance(sharpness)
        enhancer.image.save(x[1])
        await ctx.send(file=discord.File(x[1]))
    
    @commands.command()
    async def enhance(self, ctx, factor:float, member:discord.Member=None):
        x = await pilimg(ctx, member, 'contrast')
        enhancer = ImageEnhance._Enhance()
        enhancer.enhance(factor)
        enhancer.image.save(x[1])
        await ctx.send(file=discord.File(x[1]))

    @commands.command()
    async def contrast(self, ctx, factor:float, member:discord.Member=None):
        x = await pilimg(ctx, member, 'contrast')
        enhancer = ImageEnhance.Contrast(x[0])
        enhancer.enhance(factor)    
        enhancer.image.save(x[1])
        await ctx.send(file=discord.File(x[1]))

    @commands.command()
    async def brightness(self, ctx, factor:float, member:discord.Member=None):
        x = await pilimg(ctx, member, 'brightness')
        enhancer = ImageEnhance.factor(x[0])
        enhancer.enhance(factor)
        enhancer.image.save(x[1])
        await ctx.send(file=discord.File(x[1]))
    
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
        async with aiohttp.ClientSession() as sess:
            async with sess.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key={}".format(key2)) as resp:
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
        async with aiohttp.ClientSession() as client:
            async with client.get("https://some-random-api.ml/meme") as resp:
                response = await resp.json()
                await ctx.send(response['image'])

    @commands.command(description="""Sends a wasted filtered avatar""")
    async def wasted(self, ctx:Context, member: discord.Member=None):
       
        if member is None:
            avatar = ctx.author.avatar.with_format('png')
        else:
            avatar = member.avatar.with_format('png')

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/wasted?avatar={avatar}")
            
            file = open('./images/wasted.png', 'wb')
            file.write(response.content)
            file.close()    
        await ctx.send(file=discord.File('./images/wasted.png'))

    @commands.command(description="""Sends a wasted filtered avatar""")
    async def threshold(self, ctx:Context, member: discord.Member=None):
       
        if member is None:
            avatar = ctx.author.avatar.with_format('png')
        else:
            avatar = member.avatar.with_format('png')

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/threshold/?avatar={avatar}")
            
            file = open('./images/threshold.png', 'wb')
            file.write(response.content)
            file.close()    
            await ctx.send(file=discord.File('./images/threshold.png'))    

   
        
    @commands.command(description="""Sends a fay filtered avatar""")
    async def gay(self, ctx:Context, member:discord.Member=None):
        
        if member is None:
            avatar = ctx.author.avatar.with_format('png')
        else:
            avatar = member.avatar.with_format('png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/gay?avatar={avatar}")
            file = open('./images/gay.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/gay.png')) 

    @commands.command(description="""Sends a glass filtered avatar""")
    async def glass(self, ctx:Context, member:discord.Member=None):
        
        if member is None:
            avatar = ctx.author.avatar.with_format('png')
        else:
            avatar = member.avatar.with_format('png')

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/glass?avatar={avatar}")
            file = open('./images/glass.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/glass.png')) 

    @commands.command(description="""Sends a triggered filtered avatar""")
    async def triggered(self, ctx:Context, member:discord.Member=None):
       
        if member is None:
            avatar = ctx.author.avatar.with_format('png')
        else:
            avatar = member.avatar.with_format('png')

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/triggered?avatar={avatar}")
            file = open('./images/triggered.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/triggered.png')) 

    @commands.command(description="""Sends a bloody filtered avatar""")
    async def bloody(self, ctx:Context, member:discord.Member=None):
       
        if member is None:
            avatar = ctx.author.avatar.with_format('png')
        else:
            avatar = member.avatar.with_format('png')

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/red?avatar={avatar}")
            file = open('./images/bloody.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/bloody.png')) 
        
    @commands.command(description="""Sends a YouTube comment with your custom comment""")
    async def ytcomment(self, ctx:Context, *, comment):
       
        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar.with_format('png')}&comment={comment}&username={ctx.author.display_name}")
            file = open('./images/yt-comment.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/yt-comment.png'))

    @commands.command(description="""Makes a bright filtered avatar""")
    async def bright(self, ctx:Context, member:discord.Member=None):
        
        if member is None:
            avatar = ctx.author.avatar.with_format('png')
        else:
            avatar = member.avatar.with_format('png')

        

        async with ctx.typing():
            response = requests.get(f"https://some-random-api.ml/canvas/brightness?avatar={avatar}")
            file = open('./images/brightness.png', 'wb')
            file.write(response.content)
            file.close()
        await ctx.send(file=discord.File('./images/brightness.png')) 
            
    @commands.command(description="""Makes a bright filtered avatar""")
    async def invert(self, ctx:Context, member:discord.Member=None):
        
        if member is None:
            avatar = ctx.author.avatar.with_format('png')
        else:
            avatar = member.avatar.with_format('png')

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

    @commands.command()
    async def flip(self, ctx, member:discord.Member = None):
        x = await img(ctx, member, 'flip')

        image = cv.imread(x)

        flip = cv.flip(image, 1)    
        cv.imwrite(x, flip)
        await ctx.send(file=discord.File(x))

    @commands.command()
    async def rotate(self, ctx, degrees:float=-180, member:discord.Member=None):
        await img(ctx, member, 'rotate')

        image = cv.imread("./images/rotate.png")
        h, w = image.shape[:2]

        rotation_matrix = cv.getRotationMatrix2D((w/2,h/2), degrees, 1)

        rotated_image = cv.warpAffine(image, rotation_matrix, (w, h))
        cv.imwrite("./images/rotate.png", rotated_image)
        await ctx.send(file=discord.File('./images/rotate.png'))

    @commands.command(aliases=['pixel'])
    async def pixelate(self, ctx, member:discord.Member=None):
        await img(ctx, member, 'pixel')

        image = cv.imread("./images/pixel.png")
        image_scaled = cv.resize(image, None, fx=0.15, fy=0.15)
        image_scaled = cv.resize(image_scaled, (400, 400))
        cv.imwrite('./images/pixel.png', image_scaled)
        await ctx.send(file=discord.File('./images/pixel.png'))
def setup(bot):
  bot.add_cog(Images(bot))
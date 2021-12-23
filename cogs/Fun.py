import disnake, os, requests, json, asyncio, aiohttp
from disnake.ext import commands 
from random import choice, randint
from pyMorseTranslator import translator
from art import text2art
from glitch_this import ImageGlitcher
import cv2 as cv
import numpy as np

from core.utils.utils import thecolor, Json, thebed
from core.Context import Context
from core.utils.emojis import CLOSE
from core.Paginator import Paginator

from youtubesearchpython.__future__  import VideosSearch 

encoder = translator.Encoder()
decoder = translator.Decoder()
glitcher = ImageGlitcher()

async def img(ctx, member, name):
    await ctx.trigger_typing()

    if member is None:
        member = ctx.author
    async with aiohttp.ClientSession() as s:
        async with s.get(str(member.avatar.url)) as r:
            f = open(f'./images/{name}.png', 'wb')
            f.write(await r.read())
            f.close()

    return f"./images/{name}.png"

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['yt_search', 'search'])
    async def ytsearch(self, ctx, *, query):
        vid = VideosSearch(query, limit=10)
        result = await vid.next()

        formatted = []
        for iteration, item in enumerate(result['result'], start=1):
            formatted.append(f"**{iteration}**: [{item['title']}]({item['link']})")
            
        embed = disnake.Embed(timestamp=ctx.message.created_at, description="\n".join(formatted), color=thecolor())
        
        embed.set_author(name=f"Youtube searches for {query}: ", icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed)   


    @commands.command()
    async def glitch(self, ctx, member:disnake.Member=None):
        await img(ctx, member, 'glitch')

        glitch_img = glitcher.glitch_image('./images/glitch.png', 2, color_offset=True, gif=True)
        glitch_img[0].save('./images/glitched.gif',
                            format='GIF',
                            append_images=glitch_img[1:],
                            save_all=True,
                            duration=200,
                            loop=0                            
                            )
        await ctx.send(file=disnake.File('./images/glitched.gif'))

    @commands.command(name='screenshot')
    async def _screenshot(self, ctx, *, url):
        if True:

            urll = f"https://image.thum.io/get/http://{url}"
            return await thebed(ctx, '', url, i=urll)
        await ctx.em("This channel is not nsfw! I dont want to be deleted as a bot because you cheeky peoples couldnt keep your hands to yeselfs!")  

    @commands.command(aliases=['art'])
    async def asciiart(self, ctx:Context, *, text: str):

        if len(text) > 10:
            return await thebed(ctx, '', f"{CLOSE} Length of Text cannot be more than 10 Characters!")

        art = text2art(text)

        if len(art) > 1990:
            return await ctx.send(embed=disnake.Embed(description=f"Oops! ASCII Art crossed more than 2000 Words. Please try a smaller Text.", color=thecolor()))

        await ctx.send(embed=disnake.Embed(description=f"```yaml\n{art}```", color=self.bot.disnakecolor))

    @commands.command()
    async def sudo(self, ctx:Context, member:disnake.Member, *, text):
        await ctx.message.delete()
        for k in await ctx.channel.webhooks():
            if k.user == ctx.me:
                await k.delete()
        webhook = await ctx.channel.create_webhook(name=f"{member}")
        
        await webhook.send(text, username=member.name, avatar_url=member.avatar.url, allowed_mentions=disnake.AllowedMentions(roles=False, users=False, everyone=False))
    
    @commands.command()
    async def minecraft(self, ctx:Context, username):
        try:

            async with ctx.typing():
                response = requests.get(f"https://some-random-api.ml/mc?username={username}")
                fox = response.json()
                my_list = []
                t = 0
                
                for k in fox["name_history"]:
                    
                    #print(fox["name_history"][0][k])
                    my_list.append(f"**{fox['name_history'][t]['name']}** - {fox['name_history'][t]['changedToAt']}")
                    t += 1
                l = "\n - ".join(my_list)
            return await thebed(ctx, f'{username}', f'''
                **All names:** 
                - {l}
                
                ''')
        except:
            await thebed(ctx, '', 'They are not a minecraft player! Enter their in-game username')
        
    @commands.command(aliases=['emojis', 'sentance'])
    async def name(self, ctx:Context, *, name):
        list = []
        for k in name:
            if k == " ":
                list.append(' ')
            else:

                list.append(f':regional_indicator_{k}:')

        await thebed(ctx, 'Name in emojis...', "".join(list))
    
    @commands.command(description="Fake hacks the specified member")
    async def hack(self, ctx:Context, member:disnake.Member=""):
        
        x = False
        key = ""
    
        if not member:
            member = ctx.author
        try:
            act = member.activity.name
            for k in str(act):
                for l in ("'", "`"):
                    if k == l:

                        x = True
                        break
                if not x:

                    key += k
                else:
                    x = False
        except:
            key = "None"
        
        starting_msg = f"hacking member: {member}"
        msg = await ctx.send(f"```py\n{starting_msg}```")
        new_msg_list = f"hacking member: {member}"
        f = randint(100, 900)
        d = randint(10, 90)
        ip = f'192.168.{f}.{d}'
        
        msg_loop = [
        "\nexec hack.", "..",
        f"\npass credentials through mainstream..."
        f"\nname: '{member}'", 
        f"\nping : {self.bot.latency * 1000}", 
        f"\nraise bot account: {member.bot}", 
        f"\nawait object(): '{member.avatar}'", 
        f"\nstatus: ", f"{member.status}", 
        "\nclass User: True",
        f"\ngetattr of class User"
        f"\nactivity: '{key}'", 
        f"\naccount created at: {member.created_at}",
        f"\neval discriminator: {member.discriminator} {member.id}", 
        f"\njoined at: {member.joined_at}",
        "\nhelp: disabled", 
        f"\nname in morse: {encoder.encode(member.name).morse}", 
        f"\nimport os: Failed", 
        f"\nlocalTime: {msg.created_at}",
        "\nbreaching len: sorted(ctx)",
        "\ndef __init__(self):", "\n    grabbing ip...", "   found",
        "\n    pinging public ip...", " hash ip...", " injecting malware...", 
        f"\n    ip: ", f"{str(ip)}", 
        "\n    break"
        f"\n{member.name} has been succesfully hacked."
        ]
        for k in msg_loop:
        
            for end in ('.', '-', ':'):

                if k.endswith(end):
                    new_msg_list += f"{k}"
                    break
                else:
                    
                    new_msg_list += k
                    break
            
            await msg.edit(content=f"```py\n{new_msg_list}```")
    
    @commands.command(aliases=['findemoji', 'emojipicker', 'getemojis'])
    async def pickemoji(self, ctx:Context):
        other = open('./dicts/emojsend.json')
        data = json.load(other)
        x = []
        n = []
        for k in data:
            n.append(f":{str(k)[:-4]}:")
            x.append(data[k])
        slide = 0
        embed = disnake.Embed(title=n[slide], description="Choose emojis for this server! \nIf you press the green tick it \nautomatically adds the emoji to \nthe server by the **name**!", color=thecolor())
        embed.set_image(url=x[slide])
        embed.set_footer(text=f"{slide} / 709")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('⬅')
        await msg.add_reaction('➡')
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        def check(e, u):
            return u == ctx.author and e.message.id==msg.id
        emoji, user = await self.bot.wait_for('reaction_add', check = check)
        while emoji.emoji != '❌':
            if emoji.emoji == "➡":
                slide += 1
                newembed = disnake.Embed(title=n[slide], color=thecolor())
                newembed.set_footer(text=f"{slide} / 709")
                newembed.set_image(url=x[slide])
                await msg.edit(embed=newembed)
                await msg.remove_reaction(emoji.emoji, member=ctx.author)
                
            elif emoji.emoji == "⬅":
                slide -= 1
                newembed = disnake.Embed(title=n[slide], color=thecolor())
                newembed.set_footer(text=f"{slide} / 709")
                newembed.set_image(url=x[slide])
                await msg.edit(embed=newembed)
                await msg.remove_reaction(emoji.emoji, member=ctx.author)
                
            elif emoji.emoji == "✅":
                name = n[slide].strip(':')
                await msg.remove_reaction('✅', member=ctx.author)
                try:

                    with open(f'./emojis/{name}.png', 'rb') as k:
                        
                        y = await ctx.guild.create_custom_emoji(name=name, image=k.read())
                        
                        await ctx.send(f"{y} has been added!")
                except:
                   
                    with open(f'./emojis/{name}.gif', 'rb') as k:

                        y = await ctx.guild.create_custom_emoji(name=name, image=k.read())
                        
                        await ctx.send(f"{y} has been added!")
            
            emoji, user = await self.bot.wait_for('reaction_add',check=check)
        else:
            await msg.clear_reactions()
                
    
    @commands.command(description="Sends the users pp size")
    async def pp(self, ctx:Context):

        with open('./dicts/pp.json', 'r+') as k:
            randomsizeint = randint(1, 12)
            randomsizef = randint(1, 9)
            data = json.load(k)
            if str(ctx.author.id) in data:
                embed = disnake.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=thecolor())
            else:
                data[str(ctx.author.id)] = {
                    "inches": f"{randomsizeint}.{randomsizef}"


                }
                Json(k, data)
                embed = disnake.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=thecolor())
            await ctx.send(embed=embed)
        
    @commands.command(description="Sends the users new pp size")
    async def newpp(self, ctx:Context):
        
        with open('./dicts/pp.json', 'r+') as k:
            randomsizeint = randint(1, 12)
            randomsizef = randint(1, 9)
            data = json.load(k)
            if str(ctx.author.id) not in data:
                data[str(ctx.author.id)] = {
                    "inches": f"{randomsizeint}.{randomsizef}"


                }
                Json(k, data)
                embed = disnake.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=thecolor())
            else:
                data[str(ctx.author.id)] = {
                    "inches": f"{randomsizeint}.{randomsizef}"


                }
                Json(k, data)
                embed = disnake.Embed(title=f"Your new pp is {data[str(ctx.author.id)]['inches']} inches", colour=thecolor())
            await ctx.send(embed=embed)

        
    @commands.command(aliases=['echos'], description="Echo's the message the user sends after sending the command")
    async def echo(self, ctx:Context):

        user = self.bot.get_user(ctx.author.id)
        try:
            embed = disnake.Embed(title="What would you like to echo?", colour=thecolor())
            x = await ctx.send(embed=embed)
            msg = await self.bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            await msg.delete()
            await ctx.message.delete()
            await x.delete()
            
            embed1 = disnake.Embed(title = f"{msg.content}", colour=thecolor())   
            embed1.set_author(name=ctx.author.name, icon_url = user.avatar.url)
            await ctx.send(embed=embed1)
        except asyncio.TimeoutError:
            embed = disnake.Embed(title="Time ran out, restart the echo", colour=thecolor())
            await ctx.send(embed=embed)

    @commands.command(name = 'rand', aliases=['randomnum', 'rant', 'randomnumber', 'random_number'], description="Sends a random number between `<first_number>` and `<second_number>`")
    async def random_num(self, ctx:Context, num1: int, num2: int):
        
        embed = disnake.Embed(title="randomnum", description=randint(num1, num2))
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['coin', 'ht', 'headsandtails', 'Coinflip', 'coin_flip', 'flip_coin', 'fc'], description="Sends heads or tails, 50% chance")
    async def flipcoin(self, ctx:Context): 

        rand = randint(1, 2)
        if rand == 1:
            coin = "Heads"

        elif rand != 1: 
            coin = "Tails"

        embed = disnake.Embed(title=coin, colour=thecolor())
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['rev', 'Reversemessage', 'Message_Reverse', 'Reverse_messgae', 'Reverse_Message'], description="Reverses the `<message>` letters and words (like a mirror)")
    async def reverse(self, ctx:Context, *, message):
    
        def reverse(string):
            return string[::-1]
        embed = disnake.Embed(description=f"{reverse(message)}", colour=thecolor())
        await ctx.send(embed=embed)
        

    @commands.command(description="The specified member takes an L")
    async def l(self, ctx:Context, user:disnake.Member=""):
            if user == "":
                user = self.bot.get_user(ctx.author.id)
            embed = disnake.Embed(description=f"{user.mention} took an L", colour=thecolor())
            msg = await ctx.send(f"{user.mention}")
            await msg.delete()
            await ctx.send(embed=embed)

   
def setup(bot):
  bot.add_cog(Fun(bot))

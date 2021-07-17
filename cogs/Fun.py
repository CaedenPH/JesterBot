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
import randfacts
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from random import choice, randint
from bs4 import BeautifulSoup
from animals import Animals
from traceback import format_exception
from pyMorseTranslator import translator
import vacefron
from art import text2art
from dutils import thecolor, Json, thebed
vace_api = vacefron.Client()

encoder = translator.Encoder()
decoder = translator.Decoder()

import praw
reddit = praw.Reddit(client_id = "GfF3CEfYXsz3yw", client_secret = "_gRjhHHlRcb9uWoaJQbJddtqc-E", username = "Codex_2006", password = "senuka123", user_agent = "Codex")



class Fun(commands.Cog):
    def __init__(self, client):
   

        self.client = client
    @commands.command(aliases=['art'])
    async def asciiart(self, ctx, *, text: str):
        if len(text) > 10:
            return await thebed(ctx, '', f":x: Length of Text cannot be more than 10 Characters!")

        art = text2art(text)

        if len(art) > 1990:
            return await ctx.send(embed=discord.Embed(description=f"Oops! ASCII Art crossed more than 2000 Words. Please try a smaller Text.", color=0x36393F))

        await ctx.send(embed=discord.Embed(description=f"```yaml\n{art}```", color=self.client.discordcolor))
    @commands.command()
    async def sudo(self, ctx, member:discord.Member, *, text):
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=f"{member}")

        await webhook.send(text, username=member.name, avatar_url=member.avatar_url)
    
    @commands.command()
    async def minecraft(self, ctx, username):
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
    async def name(self, ctx, *, name):
        list = []
        for k in name:
            if k == " ":
                list.append(' ')
            else:


                list.append(f':regional_indicator_{k}:')
        await thebed(ctx, 'Name in emojis...', "".join(list))
    
    @commands.command(description="Fake hacks the specified member")
    async def hack(self, ctx, member:discord.Member=""):
        if ctx.guild.name == "Top.gg Verification Center":
            return await thebed(ctx, 'Not completed yet!')
        #LOOP
        
        x = False
        key = ""
    
        if not member:
            member = ctx.author
        act = member.activity
        for k in str(act):
            for l in ("'", "`"):
                
                if k == l:

                    x = True
                    break
            if not x:

                key += k
            else:
                x = False
        
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
        f"\nping : {self.client.latency * 1000}", 
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
        

        
    # @morse.command()
    # async def decode(self, ctx, *, morse_code):
        
        
    #     embed = discord.Embed(colour=thecolor())
    #     embed.set_footer(text=str(ctx.author) + " | Text from Morse [Decoded] |", icon_url=ctx.author.avatar_url)
        
    #     embed.add_field(name="Morse code: ", value=f'```py\n"{morse_code}"\n```', inline=False)
    #     embed.add_field(name="Decrypted result:  ", value=f"```\n{decoder.decode(morse_code).plaintext}\n```")
        
    #     await ctx.send(embed=embed)
    
        
        
 
        
    
    @commands.command(aliases=['findemoji', 'emojipicker', 'getemojis'])
    async def pickemoji(self, ctx):
        

        other = open('./dicts/emojsend.json')
        data = json.load(other)
        x = []
        n = []
        for k in data:
            n.append(f":{str(k)[:-4]}:")
            x.append(data[k])
        slide = 0
        embed = discord.Embed(title=n[slide], description="Choose emojis for this server! \nIf you press the green tick it \nautomatically adds the emoji to \nthe server by the **name**!", color=thecolor())
        embed.set_image(url=x[slide])
        embed.set_footer(text=f"{slide} / 709")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('⬅')
        await msg.add_reaction('➡')
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        def check(e, u):
            return u == ctx.author and e.message.id==msg.id
        emoji, user = await self.client.wait_for('reaction_add', check = check)
        while emoji.emoji != '❌':
            if emoji.emoji == "➡":
                slide += 1
                newembed = discord.Embed(title=n[slide], color=thecolor())
                newembed.set_footer(text=f"{slide} / 709")
                newembed.set_image(url=x[slide])
                await msg.edit(embed=newembed)
                await msg.remove_reaction(emoji.emoji, member=ctx.author)
                
            elif emoji.emoji == "⬅":
                slide -= 1
                newembed = discord.Embed(title=n[slide], color=thecolor())
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
            
            emoji, user = await self.client.wait_for('reaction_add',check=check)
        else:
            await msg.clear_reactions()

    
                
        Json(file1, data)
    
    @commands.command(description="Sends the users pp size")
    async def pp(self, ctx):
        with open('./dicts/pp.json', 'r+') as k:
            randomsizeint = randint(1, 12)
            randomsizef = randint(1, 9)
            data = json.load(k)
            if str(ctx.author.id) in data:
                embed = discord.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=thecolor())
            else:
                data[str(ctx.author.id)] = {
                    "inches": f"{randomsizeint}.{randomsizef}"


                }
                Json(k, data)
                embed = discord.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=thecolor())
            await ctx.send(embed=embed)
        
    @commands.command(description="Sends the users new pp size")
    async def newpp(self, ctx):
        with open('./dicts/pp.json', 'r+') as k:
            randomsizeint = randint(1, 12)
            randomsizef = randint(1, 9)
            data = json.load(k)
            if str(ctx.author.id) not in data:
                data[str(ctx.author.id)] = {
                    "inches": f"{randomsizeint}.{randomsizef}"


                }
                Json(k, data)
                embed = discord.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=thecolor())
            else:
                data[str(ctx.author.id)] = {
                    "inches": f"{randomsizeint}.{randomsizef}"


                }
                Json(k, data)
                embed = discord.Embed(title=f"Your new pp is {data[str(ctx.author.id)]['inches']} inches", colour=thecolor())
            await ctx.send(embed=embed)
    @commands.command()
    async def hello(self, ctx):
        embed = discord.Embed(description=f"hello {ctx.author.mention}", colour=thecolor())
        await ctx.send(embed=embed)
   
    

    
    @commands.command(hidden=True)
    async def online(self, ctx):
        response = requests.get("https://api.mcsrvstat.us/2/play.thelastblockbender.com")
            
        fox = response.json()
        lenf = fox['players']['online']
        x = False
        try:
            embed = discord.Embed(title=lenf, colour=thecolor())
            
            if 'list' in fox['players']:
                foxupdate = (fox["players"]["list"])
                embed.add_field(name=", ".join(foxupdate), value="\u200b") 
           
         

                
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
   
        
        
   

        
    @commands.command(aliases=['echos'], description="Echo's the message the user sends after sending the command")
    async def echo(self, ctx):
        user = self.client.get_user(ctx.author.id)
        try:
            embed = discord.Embed(title="What would you like to echo?", colour=thecolor())
            x = await ctx.send(embed=embed)
            msg = await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            await msg.delete()
            await ctx.message.delete()
            await x.delete()
            
            embed1 = discord.Embed(title = f"{msg.content}", colour=thecolor())   
            embed1.set_author(name=ctx.author.name, icon_url = user.avatar_url)
            await ctx.send(embed=embed1)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Time ran out, restart the echo", colour=thecolor())
            await ctx.send(embed=embed)

            
    
    @commands.command(name = 'rand', aliases=['randomnum', 'rant', 'randomnumber', 'random_number'], description="Sends a random number between `<first_number>` and `<second_number>`")
    async def random_num(self, ctx, num1: int, num2: int):
        
        embed = discord.Embed(title="randomnum", description=randint(num1, num2))
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['flip', 'coin', 'ht', 'headsandtails', 'Coinflip', 'coin_flip', 'flip_coin', 'fc'], description="Sends heads or tails, 50% chance")
    async def flipcoin(self, ctx): 
        

        rand = randint(1, 2)
        if rand == 1:
            coin = "Heads"

        elif rand != 1: 
            coin = "Tails"
        

        embed = discord.Embed(title=coin, colour=thecolor())
        await ctx.send(embed=embed)
    
        
    @commands.command(aliases=['rev', 'Reversemessage', 'Message_Reverse', 'Reverse_messgae', 'Reverse_Message'], description="Reverses the `<message>` letters and words (like a mirror)")
    async def reverse(self, ctx, *, message):

    
        def reverse(string):
            return string[::-1]
        embed = discord.Embed(description=f"{reverse(message)}", colour=thecolor())
        await ctx.send(embed=embed)
        
    
    

    @commands.command(description="The specified member takes an L")
    async def l(self, ctx, user:discord.Member=""):
            if user == "":
                user = self.client.get_user(ctx.author.id)
            embed = discord.Embed(description=f"{user.mention} took an L", colour=thecolor())
            msg = await ctx.send(f"{user.mention}")
            await msg.delete()
            await ctx.send(embed=embed)



   
def setup(client):
  client.add_cog(Fun(client))

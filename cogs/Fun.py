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

vace_api = vacefron.Client()

encoder = translator.Encoder()
decoder = translator.Decoder()

import praw
reddit = praw.Reddit(client_id = "GfF3CEfYXsz3yw", client_secret = "_gRjhHHlRcb9uWoaJQbJddtqc-E", username = "Codex_2006", password = "senuka123", user_agent = "Codex")
def Json(pref, data1):
    pref.seek(0)  # set point at the beginning of the file
    pref.truncate(0)  # clear previous content
    pref.write(json.dumps(data1, indent=4)) # write to file
class TheColor:
    def __init__(self):
        
        with open('./dicts/Color.json', 'r') as k:
            data = json.load(k)
            self.color = data['Color']['color'] 
    
xz = int(TheColor().color, 16)
async def embed(ctx, title, description=""):
    embed = discord.Embed(title=title, color=xz)
    if description:

        embed = discord.Embed(title=title, description=description, color=xz)
    await ctx.send(embed=embed)

class Fun(commands.Cog):
    def __init__(self, client):
   

        self.client = client

    
    @commands.command(help="Fake hacks the specified member")
    async def hack(self, ctx, member:discord.Member=""):
        if ctx.guild.name == "Top.gg Verification Center":
            return await embed1(ctx, 'Not completed yet!')
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
        f"\nname: '{member.name.lower()}'", 
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
        
        
    #     embed = discord.Embed(colour=xz)
    #     embed.set_footer(text=str(ctx.author) + " | Text from Morse [Decoded] |", icon_url=ctx.author.avatar_url)
        
    #     embed.add_field(name="Morse code: ", value=f'```py\n"{morse_code}"\n```', inline=False)
    #     embed.add_field(name="Decrypted result:  ", value=f"```\n{decoder.decode(morse_code).plaintext}\n```")
        
    #     await ctx.send(embed=embed)
    
        
        
 
        
    
   
    @commands.command(help="Sends the users pp size")
    async def pp(self, ctx):
        with open('./dicts/pp.json', 'r+') as k:
            randomsizeint = randint(1, 12)
            randomsizef = randint(1, 9)
            data = json.load(k)
            if str(ctx.author.id) in data:
                embed = discord.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=xz)
            else:
                data[str(ctx.author.id)] = {
                    "inches": f"{randomsizeint}.{randomsizef}"


                }
                Json(k, data)
                embed = discord.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=xz)
            await ctx.send(embed=embed)
        
    @commands.command(help="Sends the users new pp size")
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
                embed = discord.Embed(title=f"Your pp is {data[str(ctx.author.id)]['inches']} inches", colour=xz)
            else:
                data[str(ctx.author.id)] = {
                    "inches": f"{randomsizeint}.{randomsizef}"


                }
                Json(k, data)
                embed = discord.Embed(title=f"Your new pp is {data[str(ctx.author.id)]['inches']} inches", colour=xz)
            await ctx.send(embed=embed)
    @commands.command()
    async def hello(self, ctx):
        embed = discord.Embed(description=f"hello {ctx.author.mention}", colour=xz)
        await ctx.send(embed=embed)
    @commands.command(aliases=['Bow to me', 'BowToMe', 'Bow_To_Me', 'btm'], help="Forces the pinged member to bow down to the user", hidden=True)
    async def bow(self, ctx,member1:discord.Member, member2:discord.Member, *, unne="is jesus"):
        embed = discord.Embed(description=f"Bow to {member1}, {member2} because {member1} {unne}", colour=xz)
        await ctx.send(embed=embed)
    

    
    @commands.command(hidden=True)
    async def online(self, ctx):
        response = requests.get("https://api.mcsrvstat.us/2/play.thelastblockbender.com")
            
        fox = response.json()
        lenf = fox['players']['online']
        x = False
        try:
            embed = discord.Embed(title=lenf, colour=xz)
            
            if 'list' in fox['players']:
                foxupdate = (fox["players"]["list"])
                embed.add_field(name=", ".join(foxupdate), value="\u200b") 
           
         

                
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)
   
        
        
   

        
    @commands.command(aliases=['echos'], help="Echo's the message the user sends after sending the command")
    async def echo(self, ctx):
        user = self.client.get_user(ctx.author.id)
        try:
            embed = discord.Embed(title="What would you like to echo?", colour=xz)
            x = await ctx.send(embed=embed)
            msg = await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            await msg.delete()
            await ctx.message.delete()
            await x.delete()
            
            embed1 = discord.Embed(title = f"{msg.content}", colour=xz)   
            embed1.set_author(name=ctx.author.name, icon_url = user.avatar_url)
            await ctx.send(embed=embed1)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Time ran out, restart the echo", colour=xz)
            await ctx.send(embed=embed)

            
    
    @commands.command(name = 'rand', aliases=['randomnum', 'rant', 'randomnumber', 'random_number'], help="Sends a random number between `<first_number>` and `<second_number>`")
    async def random_num(self, ctx, num1: int, num2: int):
        
        embed = discord.Embed(title="randomnum", description=randint(num1, num2))
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['flip', 'coin', 'ht', 'headsandtails', 'Coinflip', 'coin_flip', 'flip_coin', 'fc'], help="Sends heads or tails, 50% chance")
    async def flipcoin(self, ctx): 
        

        rand = randint(1, 2)
        if rand == 1:
            coin = "Heads"

        elif rand != 1: 
            coin = "Tails"
        

        embed = discord.Embed(title=coin, colour=xz)
        await ctx.send(embed=embed)
    
        
    @commands.command(aliases=['rev', 'Reversemessage', 'Message_Reverse', 'Reverse_messgae', 'Reverse_Message'], help="Reverses the `<message>` letters and words (like a mirror)")
    async def reverse(self, ctx, *, message):

    
        def reverse(string):
            return string[:: -1]
        embed = discord.Embed(title=f"{reverse(message)}", colour=xz)
        await ctx.send(embed=embed)
        
    
    

    @commands.command(help="The specified member takes an L")
    async def l(self, ctx, user:discord.Member=""):
            if user == "":
                user = self.client.get_user(ctx.author.id)
            embed = discord.Embed(description=f"{user.mention} took an L", colour=xz)
            msg = await ctx.send(f"{user.mention}")
            await msg.delete()
            await ctx.send(embed=embed)



    @commands.command(help="Pokes the `<member>` specified")
    async def poke(self, ctx, member: discord.Member=""):
        if member == "":
            embed = discord.Embed(description=f"**{ctx.author.name}** has poked you 😗", colour=xz)
            await ctx.author.send(embed=embed)
            embed = discord.Embed(description=f"The **poke** will be sent to the specified member in aprox {round(self.client.latency * 1000)}ms", colour=xz)
            await ctx.send(embed=embed)     
        else:
            embed = discord.Embed(description=f"**{ctx.author.name}** has poked you 😗", colour=xz)
            await member.send(embed=embed)
            embed = discord.Embed(description=f"The **poke** will be sent to the specified member in aprox **{round(self.client.latency * 1000)}** ms", colour=xz)
            await ctx.send(embed=embed) 

    @commands.command(help="Sends a hug to the `<member>` specified")
    async def hug(self, ctx, member:discord.Member=""):
        if member == "":

            embed = discord.Embed(description=f"**{ctx.author.name}** has given you the gift of a hug 🌷", colour=xz)
            await ctx.author.send(embed=embed)
            embed = discord.Embed(description=f"The **hug** will be sent to the specified member in aprox **{round(self.client.latency * 1000)}**ms", colour=xz)
            await ctx.send(embed=embed) 
        else:

            embed = discord.Embed(description=f"**{ctx.author.name}** has given you the gift of a hug 🌷", colour=xz)
            await member.send(embed=embed)
            embed = discord.Embed(description=f"The **hug** will be sent to the specified member in aprox **{round(self.client.latency * 1000)}**ms", colour=xz)
            await ctx.send(embed=embed) 
def setup(client):
  client.add_cog(Fun(client))

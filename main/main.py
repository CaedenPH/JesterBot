
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
from discord.ext.buttons import Paginator
from traceback import format_exception
import vacefron
import asyncpraw
import randfacts
reddit = asyncpraw.Reddit(client_id = "GfF3CEfYXsz3yw", client_secret = "_gRjhHHlRcb9uWoaJQbJddtqc-E", username = "Codex_2006", password = "senuka123", user_agent = "Codex")
vace_api = vacefron.Client()
class TheColor:
    def __init__(self):
        
        with open('./dicts/Color.json', 'r') as k:
            data = json.load(k)
            self.color = data['Color']['color'] 
    
xz = int(TheColor().color, 16)
async def embed1(ctx, title, description=""):
    embed = discord.Embed(title=title, color=xz)
    if description:

        embed = discord.Embed(title=title, description=description, color=xz)
    await ctx.send(embed=embed)
def Json(pref, data1):
    pref.seek(0)  # set point at the beginning of the file
    pref.truncate(0)  # clear previous content
    pref.write(json.dumps(data1, indent=4)) # write to file
def get_prefix(bot, message):
    with open("./dicts/prefixes.json") as fin:
        prefixes = json.load(fin)
    if str(message.author.id) in prefixes:

        return prefixes[str(message.author.id)]['prefix']
    else:
        return ["^", "."]
    
intents = Intents.all()
intents.members = True
client = commands.Bot(command_prefix = get_prefix, intents=intents, case_insensitive=True)
client.remove_command('help')


for filename in os.listdir("./cogs/"):
    if filename.endswith('.py'):
        if not filename.startswith('dutils'):

            client.load_extension(f'cogs.{filename[:-3]}')




xtt ={}
@client.check
async def check(ctx):
 
  
    with open('./dicts/Check.json') as k:
        data = json.load(k)
       
        if str(ctx.author.id) in data:
            
            if ctx.command.name in data[str(ctx.author.id)]['commands']:
                await embed1(ctx, 'you cant run this command for some reason, possibly blacklisted')
                return False
            else:
                return True
        else:
            return True


@client.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == 298043305927639041:
        embed = discord.Embed(color=discord.Color.dark_gold())
        client.load_extension(f'cogs.{extension}')
        embed.add_field(name="Load Extension", value=f"Loaded cog: ``{extension}`` successfully")
        await ctx.send(embed=embed)

    else:
       await ctx.send("You're not the owner of this bot...")

#unload
@client.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == 298043305927639041:
        client.unload_extension(f'cogs.{extension}')
        embed = discord.Embed(color=discord.Color.dark_gold())
        embed.add_field(name="Unload Extension", value=f"Unloaded cog: ``{extension}`` successfully")
        await ctx.send(embed=embed)

    else:
        await ctx.send("You're not the owner of this bot...")
#reload
@client.command(aliases=['r'], hidden=True)
async def reload(ctx, extension=""):
    if ctx.author.id == 298043305927639041:
        if not extension:
       
            for cog in tuple(client.extensions):
        
                client.reload_extension(cog)
            embed = discord.Embed(color=discord.Color.dark_gold())
            embed.add_field(name="Reload Extension", value=f"Reloaded cogs successfully")
            await ctx.send(embed=embed)
        else:

            client.reload_extension(f'cogs.{extension}')
            embed = discord.Embed(color=discord.Color.dark_gold())
            embed.add_field(name="Reload Extension", value=f"Reloaded cog: ``{extension}`` successfully")
            await ctx.send(embed=embed)
    else: 
        await ctx.send("You're not the owner of this bot...")
def fact():
    fact = randfacts.getFact()
    embed=discord.Embed(color=xz)
    embed.add_field(name="Fact", value=fact)
    return embed

def quote():
        
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    embed=discord.Embed(color=xz)
    embed.add_field(name="Quote", value='*"{quoteText}"*\n{quoteAuthor}'.format(**json.loads(response.text)))
    return embed
 

def joke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    fox = response.json()
    foxupdate = (fox["setup"]) 
    foxupdatey = (fox["punchline"])
    embed = discord.Embed(title="Joke", description=f"{foxupdate} ... {foxupdatey}", colour=xz)
    return embed
@tasks.loop(seconds=3600.0)
async def printer():
    with open('./dicts/ConfigChannel.json') as k:
        data = json.load(k)
        for k in data:
            
            if k not in "emojis":
                for e in data[k]:
                    try:
                        await client.wait_until_ready()
                        t = client.get_channel(int(data[k][e])) 
                        if e == "factchannel":
                            send = fact()
                        elif e == "jokechannel":
                            send = joke()
                        elif e == "pickuplinechannel":
                            subreddit = await reddit.subreddit("pickuplines") 
                            pickupline = await subreddit.random()

                            embed = discord.Embed(color=xz)
                            embed.add_field(name=pickupline.title, value=pickupline.selftext)
                            send = embed
                            
                        elif e == "quotechannel":
                            send = quote()
                        await t.send(embed=send)
                        
                    
                    except:
                        pass
    
printer.start()
@client.after_invoke
async def executed(ctx):
    
    # global scoreded
    await client.wait_until_ready()
    
    if ctx.command.name == "color":
        for cog in tuple(client.extensions):
            
                client.reload_extension(cog)
    await client.wait_until_ready()     
   
    with open('./dicts/Selfscore.json', 'r+') as k:
        loaded1 = json.load(k)
        if str(ctx.author.id) in loaded1:
            pass
        else:
            loaded1[str(ctx.author.id)] = {
            "Name":    ctx.author.name,
            "Guild":    ctx.guild.name,
            "selfscore":  0,
            
        

        }

            k.seek(0)  # set point at the beginning of the file
            k.truncate(0)  # clear previous content
            k.write(json.dumps(loaded1, indent=4)) # write to file

    with open('./dicts/Scoreoverall.json', 'r+') as x:
        data = json.load(x)
        data["Score"]["Score1"] += 1
        x.seek(0)
        x.truncate(0)
        x.write(json.dumps(data, indent=4))



    with open('./dicts/Selfscore.json', 'r+') as f:
        data = json.load(f)
        
        if str(ctx.author.id) in data:
            data[str(ctx.author.id)]['selfscore'] += 1
            f.seek(0)
            f.truncate(0)
            f.write(json.dumps(data, indent=4))


    user = client.get_user(298043305927639041)
    if ctx.author.id != 298043305927639041:
        await user.send(f"Name:{ctx.author.name} \nGuild:{ctx.guild}  \nCommand:{ctx.command.name} \nChannel:{ctx.channel.name}")

    with open('./dicts/Commandsused.json') as y:
        data = json.load(y)
        if str(ctx.command) not in data:
            data[str(ctx.command)] = {
                'score': 1
                
            } 
            
            
            with open('./dicts/Commandsused.json', 'r+') as y:
                
                y.seek(0)
                y.truncate(0)
                y.write(json.dumps(data, indent=4))

        else:
    
            
            with open('./dicts/Commandsused.json', 'r+') as y:
                data[str(ctx.command)]['score'] += 1
                y.seek(0)
                y.truncate(0)
                y.write(json.dumps(data, indent=4))


filed = open("./dicts/Text.txt")
code = filed.read()
client.run(code)







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



# @commands.command()
# async def thecog(ctx):
#     for cog in client.cogs:
#         await ctx.send
xtt ={}
@client.check
async def check(ctx):
    
    # with open('./dicts/Suggest.json') as l:
    #     data = json.load(l)
        
    #     if str(ctx.channel.id) in data and data[str(ctx.channel.id)]['Yes'] == True:
            
    #         if ctx.command.name == "suggest":
    #             xtt[str(ctx.channel.id)] = True
                
    #             user = ctx.author.id
    #             username = client.get_user(user)

    #             try:
                                
    #                 embed = discord.Embed(title="Suggestion", colour=xz)
    #                 embed1 = discord.Embed(title=f"What is the title of your suggestion? Type end at any point to stop and type title to remove the description", colour=xz)
    #                 x = await ctx.send(embed=embed1)
    #                 received_msg = str((await client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
    #                 if received_msg not in ["end", "title"]:
    #                     msg1 = received_msg
    #                     embed2 = discord.Embed(title=f"What is the description of your suggestion? Type end at any point to stop", colour=xz)
    #                     y = await ctx.send(embed=embed2)
    #                     received_msg1 = str((await client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
    #                     if received_msg1 != "end":
    #                         msg2 = received_msg1
    #                         embed.add_field(name="Title", value=msg1, inline=False)
    #                         embed.add_field(name="Description", value=msg2, inline=False)
    #                         # embed.set_thumbnail(url=username.avatar_url_as(size=256))
    #                         embed.set_footer(text=ctx.author.name, icon_url=username.avatar_url)
    #                         # {username.avatar_url_as(size=256)} 
                            
    #                         await x.delete()
    #                         await y.delete()
    #                         await ctx.message.delete()
    #                         await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    #                         msg = await ctx.send(embed=embed)
    #                         await msg.add_reaction("👍")
    #                         await msg.add_reaction("👎")
                            
    #                     else:
    #                         embed3 = discord.Embed(title="Goodbye", colour=xz)
    #                         await x.delete()
    #                         await y.delete()
    #                         await ctx.message.delete()
    #                         await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    #                         msg = await ctx.send(embed=embed3)
                        
    #                 elif received_msg == "end":
    #                     await x.delete()
    #                     await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    #                     embed3 = discord.Embed(title="Goodbye", colour=xz)
    #                     await ctx.send(embed=embed3)
    #                 else:
    #                     embed2 = discord.Embed(title=f"What is the Title of your suggestion? Type end at any point to stop", colour=xz)
    #                     y = await ctx.send(embed=embed2)
    #                     received_msg1 = str((await client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
    #                     if received_msg1 != "end":

    #                         embed.add_field(name="Title", value=received_msg1, inline=False)
                            
    #                         # embed.set_thumbnail(url=username.avatar_url_as(size=256))
    #                         embed.set_footer(text=ctx.author.name, icon_url=username.avatar_url)
    #                         # {username.avatar_url_as(size=256)} 
                            
    #                         await x.delete()
    #                         await y.delete()
    #                         await ctx.message.delete()
    #                         await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    #                         msg = await ctx.send(embed=embed)
    #                         await msg.add_reaction("👍")
    #                         await msg.add_reaction("👎")
    #             except asyncio.TimeoutError:
    #                 embed = discord.Embed(title="Time ran out, restart the ticket", colour=xz)
    #                 await ctx.send(embed=embed)
    #         else:
    #             if not xtt[str(ctx.channel.id)]:

    #                 await ctx.message.delete()
            
    #     else:
    #         pass
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

# @client.event
# async def on_message(message):
#     await client.wait_until_ready()


#     mg = str(message.guild.id)  
    
    

#     mc = str(message.channel.id)
#     with open('./dicts/VerifyChannel.json') as k:
#         data = json.load(k)
    
#         if not data:
#             pass
#         else:
#             if mc in data:
#                 if data[mc]['Yes'] == True:

#                     if message.content != "verify":
#                         await message.delete()
#                     else:
                        
#                         with open('./dicts/Welcome.json') as w:
#                             weldata = json.load(w)
#                             if str(message.guild.id) in weldata and weldata[str(message.guild.id)]['Welcome']:
                                
                            
#                                 role = discord.utils.get(message.guild.roles, id=weldata[str(message.guild.id)]['role'])
#                                 await message.author.add_roles(role)
                            
#                                 role = discord.utils.get(message.guild.roles, id=data[str(message.channel.id)]['URole id'])
                                
                        
                    
#                                 await message.author.remove_roles(role)

                                

#                                 await message.delete()
#                                 if weldata[str(message.guild.id)]['message'] == "":
                                    
#                                     channel = message.guild.get_channel(weldata[str(message.guild.id)]["channel_id"])
#                                     msg = await channel.send(f"{message.author.mention}")
#                                     await msg.delete()
#                                     embed = discord.Embed(title=f"Welcome!", description=f"{message.author.mention} don't forget to type `^rules` to see the rules for the server, but most of all dont forget to have fun at {message.guild}!", colour=int(xz.color, 16))

#                                     embed.set_thumbnail(url=f"{message.guild.icon_url}") 
#                                     embed.set_image(url='https://cdn.discordapp.com/attachments/847528639125258322/855559791384592404/360_F_361521131_tvclR3GrsVQBFVsUe1EPNFgH2MWIN1w7.png')
#                                     embed.set_author(name=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")
#                                     # role = discord.utils.get(member.guild.roles, id=loaded[str(member.guild.id)]['role'])
#                                     await channel.send(embed=embed)
                                
#                                 else:
#                                     channel = member.guild.get_channel(weldata[str(message.guild.id)]["channel_id"])
#                                     await channel.send(f"{weldata[str(message.guild.id)]['message']}")
                                
#                             else:
                            
#                                 role = discord.utils.get(message.guild.roles, id=int(data[str(message.channel.id)]['MRole id']))
#                                 role1 = discord.utils.get(message.guild.roles, id=int(data[str(message.channel.id)]['URole id']))
#                                 await message.author.add_roles(role)
#                                 await message.author.remove_roles(role1)
#                                 await message.delete()
                
#                 else:
#                     pass              
#             else:
#                 pass

#     with open('./dicts/Server.json', 'r+') as l:
#         data = json.load(l)
#         if message.author.id != 828363172717133874: 
#             if mg not in data:
#                 data[mg] = {
#                     "Score": 1


#                 }
#             else:
#                 data[mg]['Score'] += 1
            
#             l.seek(0)
#             l.truncate(0)
#             l.write(json.dumps(data, indent=4))
        

#     with open('./dicts/Suggest.json', 'r+') as l:
#         data = json.load(l)
#         us = client.get_user(828363172717133874)

#         if str(message.channel.id) in data and data[str(message.channel.id)]['Yes'] == True:
        
#             if message.content[1:] not in ['suggest', 's', 'sug'] and message.author.id != 828363172717133874:
#                 await message.delete()
#                 # embed = discord.Embed(title=f"Type ^suggest to make a suggestion! You cannot type in the {message.channel.name}", colour=int(xz.color, 16))
#                 # await message.author.send(embed=embed)
#             # else:
#             #     await client.process_command(suggest)
#         # , {data[message.channel.id]}

#     # if 'Jesterbot' or 'Jester' or 'BestBot' or 'JesterBot' or 'jesterbot' in [message.content]:
#     #     response = requests.get('https://official-joke-api.appspot.com/random_joke')
#     #     fox = response.json()
#     #     foxupdate = (fox["setup"]) 
#     #     foxupdatey = (fox["punchline"])

#     #     x = []
#     #     prefix = await client.get_prefix(message)
#     #     for pref in prefix:
#     #         x.append(f"`{pref}`")
#     #     embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
#     #     │ My default prefix is: `^` │
#     #     │ My prefix for you is: {', '.join(x)} │ 
#     #     │ Type `^prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
        
        
#             else:
#                 await client.process_commands(message)

#         else:
#             await client.process_commands(message)
#     #     """, colour=int(xz.color, 16))
#     #     embed.set_author(name="JesterBot", icon_url=us.avatar_url)

#     #     embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
#     #     embed.set_footer(text="You can get more of these jokes with ^joke!")
#     # ['Jesterbot', 'Jester', 'BestBot', 'JesterBot', 'jesterbot']

#     for item in ('Jesterbot', 'Jester', 'BestBot', 'JesterBot', 'jesterbot', 'jest', 'Jest', 'JB', 'jb', 'Jb'):
#         if item in message.content:

#             msg12 = ""
#         # print()
#             num = 1
            
#             await message.add_reaction("👍")
#             await message.add_reaction("👎")
#             def check(e, u):
#                 return u == message.author and e.message.id==message.id
#             try:

#                 emoji, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
#                 while emoji.emoji not in ["👎"]:
                
#                     x = []
#                     response = requests.get('https://official-joke-api.appspot.com/random_joke')
#                     fox = response.json()
#                     foxupdate = (fox["setup"]) 
#                     foxupdatey = (fox["punchline"])
#                     prefix = await client.get_prefix(message)
#                     for pref in prefix:
#                         x.append(f"`{pref}`")
#                     embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
#                     │ My default prefix is: `^` │
#                     │ My prefix for you is: {', '.join(x)} │ 
#                     │ Type `^prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
                    
                    
                    
#                     """, colour=int(xz.color, 16))
#                     embed.set_author(name="JesterBot", icon_url=us.avatar_url)
            
#                     embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
#                     embed.set_footer(text="You can get more of these jokes with ^joke!")
            
#                     msg12 = await message.channel.send(embed=embed)
#                     num = 2 
#                     await message.remove_reaction(member=message.author, emoji="👍")
#                     emoji, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                    
                
#                 else:
#                     if num == 2:
                        
#                         await msg12.delete()
#                         await message.remove_reaction(member=message.author, emoji="👎")




#             except asyncio.TimeoutError:
#                 print("huh")
#                 await message.remove_reaction(member=message.author, emoji="👍")
#                 await message.remove_reaction(member=message.author, emoji="👎")
        

        

#     if message.mentions:
#         if client.user in message.mentions:
            
#             response = requests.get('https://official-joke-api.appspot.com/random_joke')
#             fox = response.json()
#             foxupdate = (fox["setup"]) 
#             foxupdatey = (fox["punchline"])

#             x = []
#             prefix = await client.get_prefix(message)
#             for pref in prefix:
#                 x.append(f"`{pref}`")
#             embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
#             │ My default prefix is: `^` │
#             │ My prefix for you is: {', '.join(x)} │ 
#             │ Type `^prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
            
            
            
#             """, colour=int(xz.color, 16))
#             embed.set_author(name="JesterBot", icon_url=us.avatar_url)

#             embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
#             embed.set_footer(text="You can get more of these jokes with ^joke!")
#             return await message.channel.send(embed=embed)

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
    # with open('./dicts/Bal.json', 'r+') as k:
    #     data = json.load(k)
    #     if str(ctx.author.id) not in data:
    #         data[str(ctx.author.id)] = {
    #             "Bal": 1,
    #             "Name": ctx.author.name


    #         }
    #     else:
    #         x = randint(1, 10)
    #         data[str(ctx.author.id)]['Bal'] += x
    #     Json(k, data)
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






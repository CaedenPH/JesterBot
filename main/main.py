
import discord, os, requests, json, asyncio
from discord.ext import commands 
from discord.ext import tasks
from discord import Intents
from async_timeout import timeout
import vacefron
import asyncpraw
import randfacts
from dutils import thecolor, Json, thebed

reddit = asyncpraw.Reddit(client_id = "GfF3CEfYXsz3yw", client_secret = "_gRjhHHlRcb9uWoaJQbJddtqc-E", username = "Codex_2006", password = "senuka123", user_agent = "Codex")
vace_api = vacefron.Client()

def get_prefix(bot, message):
    try:
        with open("./dicts/prefixes.json") as fin:
            prefixes = json.load(fin)
    
        if str(message.guild.id) in prefixes:

            if str(message.author.id) in prefixes:

                return prefixes[str(message.author.id)]['prefix']
            else:
                return prefixes[str(message.guild.id)]['prefix']
        else:
            if str(message.author.id) in prefixes:

                return prefixes[str(message.author.id)]['prefix']
            else:
                return ["^", "."]
    except:
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

@client.listen('on_message')
async def precheck(message):

    with open('./dicts/Suggest.json') as k:
        data = json.load(k)
        
        if str(message.channel.id) in data:
            if data[str(message.channel.id)]['Yes']:
                for item in ('suggest', 'sug'):
                    if item in message.content:
                        user = message.author.id
                        username = client.get_user(user)

                        try:
                                        
                            embed = discord.Embed(description="Suggestion", colour=thecolor())
                            embed1 = discord.Embed(description=f"What is the title of your suggestion? Type end at any point to stop and type title to remove the description", colour=thecolor())
                            x = await message.author.send(embed=embed1)
                            received_msg = str((await client.wait_for('message', timeout=60.0, check=lambda m: m.author == message.author)).content).lower()
                            if received_msg not in ["end", "title"]:
                                msg1 = received_msg
                                embed2 = discord.Embed(description=f"What is the description of your suggestion? Type end at any point to stop", colour=thecolor())
                                y = await message.author.send(embed=embed2)
                                received_msg1 = str((await client.wait_for('message', timeout=90.0, check=lambda m: m.author == message.author)).content).lower()
                                if received_msg1 != "end":
                                    msg2 = received_msg1
                                    embed.add_field(name="Title", value=msg1, inline=False)
                                    embed.add_field(name="Description", value=msg2, inline=False)
                                    embed.set_footer(text=message.author.name, icon_url=username.avatar_url)
                                    await thebed(message.author, '', 'Completed!')
                                    
                                    msg = await message.channel.send(embed=embed)
                                    await msg.add_reaction("👍")
                                    await message.delete()
                                    return await msg.add_reaction("👎")
                                    
                                else:
                                    embed3 = discord.Embed(description="Goodbye", colour=thecolor())
                                   
                                    
                                    msg = await message.author.send(embed=embed3)
                                
                            elif received_msg == "end":
                                
                                
                                embed3 = discord.Embed(description="Goodbye", colour=thecolor())
                                await message.delete()
                                return await message.author.send(embed=embed3)
                            else:
                                embed2 = discord.Embed(description=f"What is the Title of your suggestion? Type end at any point to stop", colour=thecolor())
                                y = await message.author.send(embed=embed2)
                                received_msg1 = str((await client.wait_for('message', timeout=90.0, check=lambda m: m.author == message.author)).content).lower()
                                if received_msg1 != "end":

                                    embed.add_field(name="Title", value=received_msg1, inline=False)
                                    
                                    embed.set_footer(text=message.author.name, icon_url=username.avatar_url)
                                    
                                    
                                    msg = await message.channel.send(embed=embed)
                                    await thebed(message.author, '', 'Completed!')
                                    await msg.add_reaction("👍")
                                    await message.delete()
                                    return await msg.add_reaction("👎")
                        except Exception as e:
                            print(e)
                        
                        
                    else:
                        if message.author.id != 828363172717133874:

                            await client.wait_until_ready()
                            try:
                                await message.delete()
                            except:
                                pass

@client.check
async def mycheck(ctx):      

    try:
        ra = ctx.guild.id
    except:
        return await thebed(ctx, '', 'Commands do not work in dms I am afraid!') 
    k = open('./dicts/Admins.json')
    cdata = json.load(k)
    if ctx.command.cog:
        if ctx.command.cog.qualified_name == "Staff" and ctx.author.id not in cdata['admins']:
            return False          
    x = False
    with open('./dicts/Check.json') as k:
        data = json.load(k)
       
        if str(ctx.author.id) in data:
            
            if ctx.command.name in data[str(ctx.author.id)]['commands']:
                await thebed(ctx, 'you cant run this command for some reason, possibly blacklisted')
                return False
            else:
                x = True
        else:
            x = True

    if x:
        
        with open('./dicts/Suggest.json') as k:
            newdata = json.load(k)
        
            if str(ctx.channel.id) in newdata:
                if newdata[str(ctx.channel.id)]['Yes']:
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
    embed=discord.Embed(color=thecolor())
    embed.add_field(name="Fact", value=fact)
    return embed

def quote():
        
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    embed=discord.Embed(color=thecolor())
    embed.add_field(name="Quote", value='*"{quoteText}"*\n{quoteAuthor}'.format(**json.loads(response.text)))
    return embed

def joke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    fox = response.json()
    foxupdate = (fox["setup"]) 
    foxupdatey = (fox["punchline"])
    embed = discord.Embed(title="Joke", description=f"{foxupdate} ... {foxupdatey}", colour=thecolor())
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

                            embed = discord.Embed(color=thecolor())
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
    await client.wait_until_ready()
    user = client.get_user(298043305927639041)
    if ctx.author.id != 298043305927639041:
        await user.send(f"Name:{ctx.author.name} \nGuild:{ctx.guild}  \nCommand:{ctx.command.name} \nChannel:{ctx.channel.name}")
    
    if ctx.command.name == "color":
        for cog in tuple(client.extensions):
            
                client.reload_extension(cog)
   
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

            Json(k, data)

    with open('./dicts/Scoreoverall.json', 'r+') as x:
        data = json.load(x)
        data["Score"]["Score1"] += 1
        Json(x, data)



    with open('./dicts/Selfscore.json', 'r+') as f:
        data = json.load(f)
        
        if str(ctx.author.id) in data:
            data[str(ctx.author.id)]['selfscore'] += 1
            Json(f, data)

    with open('./dicts/Commandsused.json') as y:
        data = json.load(y)
        if str(ctx.command) not in data:
            data[str(ctx.command)] = {
                'score': 1
            } 
            
            with open('./dicts/Commandsused.json', 'r+') as y:
                Json(y, data)
        else:
            
            with open('./dicts/Commandsused.json', 'r+') as y:
                data[str(ctx.command)]['score'] += 1
                Json(y, data)


filed = open("./dicts/Text.txt")
code = filed.read()
client.run(code)

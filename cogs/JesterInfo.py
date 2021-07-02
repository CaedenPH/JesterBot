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
import io
import textwrap
import contextlib
import shutil
from discord.ext.buttons import Paginator
from traceback import format_exception
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
async def embed1(ctx, title, description=""):
    embed = discord.Embed(title=title, color=xz)
    if description:

        embed = discord.Embed(title=title, description=description, color=xz)
    await ctx.send(embed=embed)
class JesterInfo(commands.Cog):
    def __init__(self, client):

        self.client = client
    
   
    @commands.command(hidden=True)
    async def blacklist(self, ctx, user:int, cmd):
        command = self.client.get_command(cmd)
        with open('./dicts/Check.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                data[str(ctx.author.id)]['commands'].append(command.name)
            else:
                data[str(ctx.author.id)] = {
                    'commands': [command.name]
                }
            Json(k, data)
    

        
    @commands.command(aliases=['Ver', 'verions'], help="Sends the version that the discord bot is currently on - Changes frequently as updates occur")
    async def version(self, ctx):
        with open('./dicts/Updates.json', 'r') as x:
            data = json.load(x)
            for m in data:

                embed = discord.Embed(title=f"{data[m]['Version']}", colour=xz)
                await ctx.send(embed=embed)
        
    @commands.command(aliases=['scoreover', 'Overallscore', 'Overall_score'], help="Sends the total number of commands used")
    async def score(self, ctx):
        with open('./dicts/Scoreoverall.json', 'r') as x:
            data = json.load(x)
            embed = discord.Embed(title=f"{data['Score']['Score1']}", colour=xz)
            await ctx.send(embed=embed)
        
    
    @commands.command(help="Sends information about my account")
    async def me(self, ctx, member: discord.Member = ""):
        embed = discord.Embed(title="Your info", colour=0x4286ff)
        if member == "":

            username = ctx.author.name
            userip = ctx.author.id
            
            embed.add_field(name="Name", value=f"{username}", inline=False)
            embed.add_field(name="Id", value=f"{userip}", inline=False)

        else:
            username = member.name
            userip = member.id
            
            embed.add_field(name="Name", value=f"{username}", inline=False)
            embed.add_field(name="Id", value=f"{userip}", inline=False)
            
        await ctx.send(embed=embed)

    @commands.command(aliases=['Servers', 'ServerInfo', 'Server_Info'])
    async def server(self, ctx):
        channel= ctx.channel
        serverinvite = await channel.create_invite()
        serverid = ctx.guild.id
        servername = ctx.guild.name
        embed = discord.Embed(title="Your info", colour=0x4286ff)
        embed.add_field(name="Name", value=f"{servername}", inline=False)
        embed.add_field(name="Id", value=f"{serverid}", inline=False)
        embed.add_field(name="Invite", value=f"{serverinvite}", inline=False)
        # embed.add_field(name=)
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def newup(self, ctx):
        if ctx.author.id == 298043305927639041:
            try:
                embed = discord.Embed(title="Version?")
                await ctx.send(embed=embed)
                ver = await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                with open('./dicts/Updates.json', 'r+') as k:
                    loaded1 = json.load(k)
                    for m in loaded1:
                        if str(m) not in loaded1:
                            pass    
                        else:
                            loaded1[m]["Version"] = ver.content
                                
                                




                            

                            k.seek(0)
                            k.truncate(0)  # clear previous content
                            k.write(json.dumps(loaded1, indent=4)) # write to file
                embed = discord.Embed(title="Bug fixes")
                await ctx.send(embed=embed)
                y = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                while y not in  ["apply", "q"]:
                    embed1 = discord.Embed(title="Bug fixes")
                    await ctx.send(embed=embed1)



                
                    
                    with open('./dicts/Updates.json', 'r+') as k:
                        loaded1 = json.load(k)
                        for m in loaded1:
                            if str(m) not in loaded1:
                                pass    
                            else:
                                loaded1[m]["Bug fixes"] += f"\n- {y}"  

                                k.seek(0)
                                k.truncate(0)  # clear previous content
                                k.write(json.dumps(loaded1, indent=4)) # write to file
                    y = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                else:
                    embed2 = discord.Embed(title="New commands")
                    await ctx.send(embed=embed2)
                    z = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                    while z not in  ["apply", "q"]:
                        embed3 = discord.Embed(title="New commands")
                        await ctx.send(embed=embed3)


                    
                        
                        with open('./dicts/Updates.json', 'r+') as k:
                            loaded1 = json.load(k)
                            for m in loaded1:
                                if str(m) not in loaded1:
                                    pass    
                                else:
                                    loaded1[m]["New commands"] += f"\n- {z}"  

                                    k.seek(0)
                                    k.truncate(0)  # clear previous content
                                    k.write(json.dumps(loaded1, indent=4)) # write to file
                        
                        
                        z = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                    else:
                        embed = discord.Embed(title="Other")
                        await ctx.send(embed=embed)
                        a = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                        while a not in  ["apply", "q"]:
                            embed3 = discord.Embed(title="Other")
                            await ctx.send(embed=embed3)


                        
                            
                            with open('./dicts/Updates.json', 'r+') as k:
                                loaded1 = json.load(k)
                                for m in loaded1:
                                    if str(m) not in loaded1:
                                        pass    
                                    else:
                                        loaded1[m]["Other"] += f"\n- {a}"  

                                        k.seek(0)
                                        k.truncate(0)  # clear previous content
                                        k.write(json.dumps(loaded1, indent=4)) # write to file
                            a = str((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)).content).lower()
                        else:
                            embed4 = discord.Embed(title="Applied")
                            await ctx.send(embed=embed4)
                            
                            
                            
                        
                            

                    
                
            except asyncio.TimeoutError:
                embed = discord.Embed(title="Time ran out, restart the ticket", colour=xz)
                await ctx.send(embed=embed)


    @commands.command(hidden=True)
    async def newver(self, ctx, *, Destroy=""):
        if ctx.author.id == 298043305927639041:
            if Destroy == "":
                with open('./dicts/Updates.json', 'r+') as k:
                    loaded1 = json.load(k)
                    for m in loaded1:
                        if str(m) not in loaded1:
                            pass    
                        else:
                            loaded1[m] = {
                                "Version": "",
                                "Bug fixes": "",
                                "New commands": "",
                                "Other": ""




                            } 

                            k.seek(0)
                            k.truncate(0)  # clear previous content
                            k.write(json.dumps(loaded1, indent=4)) # write to file
                            embed4 = discord.Embed(title="Applied")
                            await ctx.send(embed=embed4)
            else:           
                with open('./dicts/Updates.json', 'r+') as k:
                    loaded1 = json.load(k)
                    for m in loaded1:
                        if str(m) not in loaded1:
                            pass    
                        else:
                            loaded1[m][f"{Destroy}"] = ""

                            k.seek(0)
                            k.truncate(0)  # clear previous content
                            k.write(json.dumps(loaded1, indent=4)) # write to file
                            embed3 = discord.Embed(title="Applied")
                            await ctx.send(embed=embed3)

    @commands.command(aliases=['notes', 'patchnotes', 'Updates', 'Patch_Notes', 'PT', 'up'], help="Sends the most recent update to the bot")
    async def update(self, ctx):
        
        
        with open('./dicts/Updates.json', 'r') as x:
            data = json.load(x)

            for m in data:
            
                if data[m]['Version'] == "":
                    embed = discord.Embed(description="Updates is currently being updated, no data to send", colour=xz)
                    await ctx.send(embed=embed)
                if data[m]['Bug fixes'] == "":
                    embed = discord.Embed(description="Updates is currently being updated, no data to send", colour=xz)
                    await ctx.send(embed=embed)
                if data[m]['New commands'] == "":
                    embed = discord.Embed(description="Updates is currently being updated, no data to send", colour=xz)
                    await ctx.send(embed=embed)
                if data[m]['Other'] == "":
                    embed = discord.Embed(description="Updates is currently being updated, no data to send", colour=xz)
                    await ctx.send(embed=embed)
                else:
                    username = self.client.get_user(828363172717133874)
                    embed = discord.Embed(description=f"**Updates** 🎉", colour=xz)
                    embed.add_field(value=f"{data[m]['Version']}",name = "**Version**", inline=True)
                    
                    embed.add_field(value=f"{data[str(m)]['Bug fixes']}",name = "**Bug fixes**", inline=False)
                    embed.add_field(value=f"{data[str(m)]['New commands']}",name = "**New commands**", inline=True)
                    embed.add_field(value=f"{data[str(m)]['Other']}", name= "**Other**", inline=False)
                    
                    
                    embed.set_footer(text=ctx.author.name, icon_url=username.avatar_url)
                    embed.set_thumbnail(url='https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif')
                    
                    await ctx.send(embed=embed)
       
   

    @commands.command(aliases=['selfruns', 'commandsused', 'Selfrun', 'Self_Score'], help="Sends the ammount of commands that you personally have ran")
    async def selfscore(self, ctx):
        with open('./dicts/Selfscore.json') as f:
            data = json.load(f)
            if str(ctx.author.id) in data:
                embed = discord.Embed(title=f"The ammount of commands you have ran are {data[str(ctx.author.id)]['selfscore']}", colour=xz)
                await ctx.send(embed=embed)
                

            
    # Giveawaytime.start()
    # @commands.command(aliases=['json'], help="Sends some of the json files being used, dm the coder for all the json files")
    # async def jsonfile(self, ctx):

    #     await ctx.send(file=discord.File("./dicts/Selfscore.json"))
    #     await ctx.send(file=discord.File("./dicts/Welcome.json"))
    #     await ctx.send(file=discord.File("./dicts/Scoreoverall.json"))
    
    #     await ctx.send(file=discord.File("./dicts/Reactionrole.json"))
    #     await ctx.send(file=discord.File("./dicts/Updates.json"))
    #     await ctx.send(file=discord.File("./dicts/Commandsused.json"))
    

    @commands.command(aliases=['binv', 'botinv'])
    async def invite(self, ctx):
        embed = discord.Embed(title=f"I am currently in {len(self.client.guilds)} servers!", description="[Official server](https://discord.gg/2654CuU3ZU) │ [Invite me!](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591)", colour = 0xfffff)
        
        embed.set_author(icon_url=ctx.author.avatar_url, name="Invite")

        await ctx.send(embed=embed)



    @commands.command(aliases=['commandtop', 'cmdtop', 'topcmd'])
    async def topcommands(self, ctx):
        score_list = []
        sorted_score_dict = {}
        
        x = []
        y = '\n'
        with open('./dicts/Commandsused.json') as k:
            embed = discord.Embed(colour=0x4286ff)
            embed.set_author(name="Top commands", icon_url=ctx.author.avatar_url)

            data = json.load(k)
            def get_key(item):
                return item[1]['score']
            sorted_scores = sorted(data.items(), key=get_key, reverse=True)[:11]
        
            for item in sorted_scores:
                
                x.append(f"{item[0]}: {item[1]['score']}")
                
                #embed.add_field(name=f"\u200b", value=f"**{item[0]}**: {item[1]['score']}", inline=False)
            embed.add_field(name=f"\u200b", value=f"**{y.join(x)}**", inline=False)

            await ctx.send(embed=embed)

        
                




    @commands.command(aliases=['membtop', 'topmemb', 'memtop'], help="Sends the top members that have used the bot") 
    async def topmembers(self, ctx):
        score_list = []
        sorted_score_dict = {}
        
        x = []
        y = '\n'
        with open('./dicts/Selfscore.json') as k:
            embed = discord.Embed(colour=0x4286ff)
            embed.set_author(name="Top members", icon_url=ctx.author.avatar_url)
            data = json.load(k)
            def get_key(item):
                return item[1]['selfscore']
            sorted_scores = sorted(data.items(), key=get_key, reverse=True)[:11]
            
            for item in sorted_scores:
                for datas in data:
                    if item[0] in datas:
                        
                        name = data[datas]['Name']
                x.append(f"{name}: {item[1]['selfscore']}")
                
                #embed.add_field(name=f"\u200b", value=f"**{item[0]}**: {item[1]['score']}", inline=False)
            embed.add_field(name=f"\u200b", value=f"**{y.join(x)}**", inline=False)

            await ctx.send(embed=embed)


    @commands.command(aliases=['lengthcmd', 'cmdamm'])
    async def lengthcommand(self, ctx):
        num = 0
        for n in self.client.commands:
            if not n.hidden:
                num += 1

        embed = discord.Embed(title=f"The bot has {num} commands", color=xz)
        await ctx.send(embed=embed)


    @commands.command(help="States the developer of the JesterBot")
    async def coder(self, ctx):
        user = self.client.get_user(298043305927639041)
        if user in ctx.guild.members:

            embed = discord.Embed(description=f"{user.mention} is the creator", colour=xz)
        
        else:
            embed = discord.Embed(title=f"{user.name} is the creator", colour=xz)

        await ctx.send(embed=embed)


    @commands.command(hidden=True)
    async def balded(self, ctx):
        if ctx.author.id ==  298043305927639041:
            with open('./dicts/Bal.json', 'r+') as k:
                data = json.load(k)
                await ctx.send(data)
                for key in data:
                
                    if "Bal" in data[key]:
                        await ctx.send(key)

                        x = self.client.get_user(int(key))
                        if not x:
                            pass
                        else:

                            data[key]['Name'] = x.name
                            
                            Json(k, data)
                            await ctx.send(data[key]['Name'])
                    else:
                        pass
        else: 
            await ctx.send("Go away!")

    @commands.command(hidden=True)
    async def baladd(self, ctx, bal:int):
        if ctx.author.id ==  298043305927639041:
            with open('./dicts/Bal.json', 'r+') as k:
                data = json.load(k)
                await ctx.send(data)
                for key in data:
                
                    if "Bal" in data[key]:
                        await ctx.send(key)

                        x = self.client.get_user(int(key))
                        if not x:
                            pass
                        else:

                            data[key]['Bal'] += bal
                            
                            Json(k, data)
                            await ctx.send(data[key]['Bal'])
                    else:
                        pass
        else: 
            await ctx.send("Go away!")
   
    @commands.command(hidden=True)
    async def removefile(self, ctx, filed, dicte:str):
        if ctx.author.id == 298043305927639041:
            with open(f'./dicts/{filed}', 'r+') as k:

            
                
                data = json.load(k)
                
            
                await ctx.send(data)

                for key in data:
                    await ctx.send(key)
                    await ctx.send(data[dicte])
                    await ctx.send(dicte)
                    if dicte == key:
                        del data[dicte]
                        Json(k, data)
        else: 
            await ctx.send("Go away!")

    @commands.command(hidden=True)
    async def addhelp(self, ctx, category=""):
        
        if ctx.author.id == 298043305927639041:
            with open('./dicts/Help.json', 'r+') as k:
                
                data = json.load(k)
                if not category:
                    await ctx.send(data)
                if category in data:
                    received_msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
                    while received_msg != "q":
                        
                        data[category]['Cmds'] += f", `{received_msg}`"
                        Json(k, data)
                        await ctx.send("uh huh")
                        received_msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
                    else:
                        return await ctx.send("done")
                else:
                    await ctx.send("nuh uh")
    @commands.command(hidden=True)
    async def removehelp(self, ctx, category):
        key_list = []
        if ctx.author.id == 298043305927639041:
            with open('./dicts/Help.json', 'r+') as k:
                
                data = json.load(k)
                if category in data:
                    received_msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
                
                    while received_msg != "q":
                        
                        
                        y = data[category]['Cmds'].split(', ')
                        await ctx.send(y)
                        await ctx.send(f"{received_msg}, {data[category]['Cmds']}")
                        if f"`{received_msg}`" in data[category]['Cmds']:
                            await ctx.send('h')
                            y.remove(f'`{received_msg}`')
                            await ctx.send(y)
                            data[category]['Cmds'] = ", ".join(y)
                    
                       

                           
                        
                           
                                
                            Json(k, data)
                   
                        received_msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()

                    else:
                        await ctx.send('k') 
                else:
                    await ctx.send("nuh uh")
    @commands.command(aliases=['python', 'py', 'Python_code', 'pythoncode', 'Pyc', 'py_c'], help="Sends the code to the discord bot")
    async def code(self, ctx):

        await ctx.send(file=discord.File("./dicts/disbot.py")) 
    @commands.command(aliases=['pin', 'pingy', 'ms', 'Latency'], help="Sends the ping of the bot")
    async def ping(self, ctx):
        embed = discord.Embed(description=f"My current ping is **{round(self.client.latency * 1000)}** ms", colour=xz)
        y = 0
        for m in self.client.guilds:
            for e in m.members:
                y += 1
        embed.set_footer(text=f"Servers in: {len(self.client.guilds)} │ Overall users: {y}")
        await ctx.send(embed=embed)
    @commands.command(aliases=['pref', 'prefixs', 'pre', 'prefixes'], help="Change the prefix of the bot for the server!")
    async def prefix(self, ctx, *, prefix=None):
        if not prefix:
            x = []
            us = self.client.user
            async with ctx.typing():
                response = requests.get('https://official-joke-api.appspot.com/random_joke')
                fox = response.json()
                foxupdate = (fox["setup"]) 
                foxupdatey = (fox["punchline"])
                prefix = await self.client.get_prefix(ctx.message)
                for pref in prefix:
                    x.append(f"`{pref}`")
                embed = discord.Embed(title=f"Hello {ctx.author.name}", description=f"""
                │ My default prefix is: `^` │
                │ My prefix for you is: {', '.join(x)} │ 
                │ Type `^prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
                
                
                
                """, colour=xz)
                embed.set_author(name="JesterBot", icon_url=us.avatar_url)
        
                embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
                embed.set_footer(text="You can get more of these jokes with ^joke!")
            return await ctx.send(embed=embed)
        prefix = prefix.split(" ")
       
        print(prefix)
        if prefix:
        
            with open('./dicts/prefixes.json', 'r+') as e:
                data = json.load(e)
                if ctx.guild.id in data:
                    data[str(ctx.author.id)]['prefix'] = prefix

                else:
                    data[str(ctx.author.id)]= {
                        "prefix": prefix


                    }
                Json(e, data)
            prefix1 = []
            for num in prefix:
                prefix1.append(f"`{num}`")
            embed = discord.Embed(description=f"New prefix is {', '.join(prefix1) if prefix else f'{prefix1}'}!, ping me for my prefixes if you forget!", colour=xz)
            embed.set_author(icon_url=ctx.author.avatar_url, name="Prefix")
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def data(self, ctx, file1="", data1="", data2="", int1='False', *, add=""):
        if int1 == 'True':
            add = int(add)
            
        else:
            pass

        x = []
        y = []
     
        if ctx.author.id == 298043305927639041:
            if not file1:
                for file1 in os.listdir('./dicts/'):
                        if file1.endswith('.json'):
                        
                            x.append(f"`{file1[:-5]}`")
                embed = discord.Embed(title="Files", description=", ".join(x), colour=xz)
                await ctx.send(embed=embed)
                
                    
                    
                            
        
                
            else:
                if not data1:

                    with open(f"./dicts/{file1}.json", 'r+') as k:
                        data = json.load(k)
                        the_num = ''
                        for key in data:
                            
                            if len(key) == len('483631842554019841'):
                                the_num = self.client.get_user(int(key))
                                
                                if not the_num:

                                    y.append(f"`{key}` │")
                                else:
                                    y.append(f"`{key}: {the_num}` │")
                            else:
                                y.append(f"`{key}`")
                        embed = discord.Embed(description=", ".join(y))
                        await ctx.send(embed=embed)
                    
                    
                   
                    
                else:
                    with open(f"./dicts/{file1}.json", 'r+') as k:
                        data = json.load(k)
                        if data1 in data:
                            if not data2:
                                embed = discord.Embed(description=data[data1])
                                await ctx.send(embed=embed)
                        
                            else:
                                data[data1][data2] = add
                                await ctx.send('yessir')
                                Json(k, data)
                            
                            

                            

                        else:
                            
                                
                            for key in data:
                                y.append(f"`{key}`")
                            embed = discord.Embed(description=", ".join(y))
                            await ctx.send(embed=embed)
                            
                    

        else:
           
            await ctx.send("You're not the owner!")

    @commands.command(hidden=True)
    async def serversin(self, ctx):
   
        x = []
        num = 0
        for g in self.client.guilds:
            x.append(g.name)
            num += 1
            
       
        await ctx.send(", ".join(x[1:25]))
        await ctx.send(", ".join(x[26:len(x)]))

    @commands.command()
    async def showcmds(self, ctx):
        x = []
        embed = discord.Embed(color=discord.Color.green())
        for command in self.client.commands:
            
            x.append(f"`{command.name}`")
        xnum = 0
        for i in range(0, len(x)):
            xnum += 1
            if xnum == 25:
                if i <= 25:
                    embed.add_field(name=i, value=", ".join(x[0:i]), inline=False)
                else:

                    r = i - 25
                    embed.add_field(name=i, value=", ".join(x[r:i]), inline=False)
                
                xnum = 0
            
        await ctx.send(embed=embed)

        
    @commands.command(aliases=['h', 'commands', 'cmd', 'command', '?', 'helpme', 'helpcommand', 'cmds'])
    async def help(self, ctx, command=""):
        try:
            client_av = self.client.get_user(828363172717133874)
            
            command1 = self.client.get_command(command)
            
            with open('./dicts/Emoji.json') as k:
                data = json.load(k)
                if command == "JesterStaff":
                    the_list1 = ""
                    if ctx.author.id == 298043305927639041:
                    
                        num = 0
                        
                        
                        for cog in self.client.cogs:
                            cog = self.client.get_cog(cog)
                            for cmd in cog.walk_commands():
                                if cmd.hidden:
                                    if num % 2 == 0:
                                        
                                        the_list1 += f"\n - `{cmd}`  │"
                                    else:
                                        the_list1 += f"`{cmd}`"
                                    num += 1
                        
                        
                        embed = discord.Embed(title=cog.qualified_name, description=f"I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `^help <command>`. \n{the_list1}", colour=xz)
                        embed.set_author(name="Help", icon_url = client_av.avatar_url)
                        embed.add_field(name="Links:", value= "[Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)")
                        return await ctx.send(embed=embed)

                cog = self.client.get_cog(command)
                if cog:
                    the_list = ""
                    num = 0
                    
                    for cmd in cog.walk_commands():
                        if not cmd.hidden:  
                            if num % 2 == 0:
                                
                                the_list += f"\n - `{cmd}`  │"
                            else:
                                the_list += f"`{cmd}`"
                            num += 1
                    
                    embed = discord.Embed(title=cog.qualified_name, description=f"I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `^help <command>`. \n{the_list}", colour=xz)
                    embed.set_author(name="Help", icon_url = client_av.avatar_url)
                    embed.add_field(name="Links:", value= "[Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)")
                    return await ctx.send(embed=embed)

                
                else:
                    y = []
                    if command1 == None and command:
                    
                        for cmd in self.client.walk_commands():
                            
                            if cmd.name[:1] == command[:1]:
                                if cmd.hidden:
                                    pass
                                else:


                                
                                    if len(y) == 5:
                                        y.append(f"`{cmd.name}`---")
                                    else:
                                        y.append(f"`{cmd.name}`")
                        my_string = ""
                        n = 0
                        for string in y:
                            
                            
                        
                            my_string += f" \n - {str(string)}"

                        
                            n += 1
                        my_string = my_string.split("---")
                

                
                        num = 1
                        embed = discord.Embed(title="Error!", colour=xz)
                        embed.set_author(icon_url=ctx.author.avatar_url, name=f"{command1} is not a command!")
                        
            
                        if my_string[0] not in [""]:

                            embed.add_field(name="Did you mean:", value=f"{my_string[0]}")
                
                    
                        
                        msg = await ctx.send(embed=embed)
                    
                        if len(my_string) >= 2:
                            if my_string[1] != "":

                                await msg.add_reaction("⬅")
                                await msg.add_reaction("➡")
                                await msg.add_reaction("⛔")
                                try:
                                    emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda e, u:u == ctx.author and e.message.id==msg.id)
                                    
                                    while emoji.emoji != "⛔":
                                        
                                        if emoji.emoji == "➡" and num == 1:
                                    
                                            embed = discord.Embed(title="Error!", colour=xz)
                                            embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                            embed.add_field(name="Did you mean:", value=f"{my_string[1]}")
                                            embed.set_footer(text="Page 2")
                                            await msg.edit(embed=embed)
                                            await msg.remove_reaction(member=ctx.author, emoji="➡")
                                            num = 2

                                        elif emoji.emoji == "⬅" and num == 2:
                                            embed = discord.Embed(title="Error!", colour=xz)
                                            embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                            embed.add_field(name="Did you mean:", value=f"{my_string[0]}")
                                            embed.set_footer(text="Page 1")
                                            await msg.edit(embed=embed)
                                            await msg.remove_reaction(member=ctx.author, emoji="⬅")
                                            num = 1
                                        else:
                                            await msg.remove_reaction(member=ctx.author, emoji="➡")
                                            await msg.remove_reaction(member=ctx.author, emoji="⬅")

                                        emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author)
                                    else:
                                        embed = discord.Embed(title="Error!", description="Goodbye", colour=xz)
                                        embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                        embed.set_footer(text="Have fun!")
                                        return await msg.edit(embed=embed)
                                        
                                except asyncio.TimeoutError:
                                    embed = discord.Embed(title="Error!", description="Session timed out", colour=xz)
                                    embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                    embed.set_footer(text="Have fun!")
                                    return await msg.edit(embed=embed)

                        
                    elif command1 == None and not command:
                        us = ctx.guild.get_member(828363172717133874)
                        if us.guild_permissions.manage_messages:
                            
                            
                            em = discord.Embed(description="**I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `^help <command>`. \nReact with the emoji corresponding to the category to see all the commands in that category. Also make sure to type `^credits` to see the developers!**\nLinks:  [Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)", colour=xz)
                            em.set_author(name="Help", icon_url = client_av.avatar_url)
                            
                            for t in self.client.cogs:
                                if t != "Event":
                                    
                                    emoj = data['emojis'][t]['em']
                                    emoj1 = data['emojis'][t]['description']
                                    em.add_field(name=f"{t} │ {emoj}", value=emoj1)
                            

                            msg = await ctx.send(embed=em)
                            for thecog in self.client.cogs:
                                if thecog != "Event":
                                    cog = self.client.get_cog(thecog)

                                    for k in data['emojis'][thecog]['em']:  
                                        await msg.add_reaction(k)
                            the_list = ""
                            the_list1 = ""
                            try:
                                emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda e, u:u == ctx.author and e.message.id==msg.id)
                                while emoji.emoji != "fw":
                                    
                                    for cog in self.client.cogs:
                                        if cog != "Event":
                                            for k in data['emojis'][cog]['em']:
                                                
                                                if k == emoji.emoji:
                                                    if cog == "JesterStaff":
                                                        num = 0
                                                        
                                                        for dcog in self.client.cogs:
                                                            dcog1 = self.client.get_cog(dcog)
                                                            for cmd in dcog1.walk_commands():
                                                                if cmd.hidden:
                                                                    if num % 2 == 0:
                                                                        
                                                                        the_list1 += f"\n - `{cmd}`  │"
                                                                    else:
                                                                        the_list1 += f"`{cmd}`"
                                                                    num += 1
                                                        
                                                        await msg.remove_reaction(member=ctx.author, emoji=emoji)
                                                        embed = discord.Embed(title=f"{cog} │ {emoji}", description=f"{the_list1}", color=xz)
                                                        
                                                        await msg.edit(embed=embed)
                                                    
                                                    elif cog == "Economy":
                                                        num = 0
                                                        
                                                        
                                                        cog1 = self.client.get_cog(cog)
                                                        for cmd in cog1.walk_commands():
                                                            if not cmd.hidden:
                                                                
                                                                
                                                                

                                                                        
                                                                        
                                                                        
                                                                    
                                                            
                                                                    
                                                                if " " not in cmd.qualified_name:
                                                                    if num % 2 == 0:
                                                                        
                                                                        the_list1 += f"\n - `{cmd}`  │"
                                                                    else:
                                                                        the_list1 += f"`{cmd}`"
                                                                    num += 1
                                                        
                                                                
                                                        
                                                        await msg.remove_reaction(member=ctx.author, emoji=emoji)
                                                        embed = discord.Embed(title=f"{cog} │ {emoji}", description=f"{the_list1}", color=xz)
                                                        
                                                        await msg.edit(embed=embed)

                                                    else:
                                                        the_list = ""
                                                        num = 0
                                                        actualcog = self.client.get_cog(cog)
                                                        for cmd in actualcog.walk_commands():
                                                            if not cmd.hidden:  
                                                                if num % 2 == 0:
                                                                    
                                                                    the_list += f"\n - `{cmd}`  │"
                                                                else:
                                                                    the_list += f"`{cmd}`"
                                                                num += 1
                                                        
                                                        embed = discord.Embed(title=f"{cog} │ {emoji}", description=f"{the_list}", color=xz)
                                                        await msg.remove_reaction(member=ctx.author, emoji=emoji)
                                                        await msg.edit(embed=embed)
                                    the_list = ""
                                    the_list1 = ""
                                    emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda e, u:u == ctx.author and e.message.id==msg.id)
                            except asyncio.TimeoutError:
                                await msg.clear_reactions()
                        else:
                            the_list = []
                            em = discord.Embed(description="**I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `^help <command>`. \nReact with the emoji corresponding to the category to see all the commands in that category. Also make sure to type `^credits` to see the developers!**\nLinks:  [Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)", colour=xz)
                            em.set_author(name="Help", icon_url = client_av.avatar_url)
                            for cog in self.client.cogs:
                                
                                if cog not in ['Music', 'Event']:
                                    
                                    thecog = self.client.get_cog(cog)
                                    for cmd in thecog.walk_commands():
                                        if not cmd.hidden:

                                            the_list.append(f"`{cmd}`")
                                
                                    em.add_field(name=cog, value="│".join(the_list), inline=False)
                                    the_list = []
                            em.add_field(name="Help command", value="The help command looks bad because the main help command requires the `discord.Permission` `manage_messages`... This is because it uses emojis to control it")
                            await ctx.send(embed=em)

                    elif command1 != None and command:
                        alx = []
                        
                        sig = command1.signature
                        thehelp = command1.help
                        alias = command1.aliases
                        if alias:
                            
                            for al in command1.aliases:

                                alx.append(f"`{al}`")
                        client_av = self.client.get_user(828363172717133874)
                        em = discord.Embed(colour=0x4286ff)
                        name = f"{command1.name.capitalize()}"
                        
                        em.add_field(name="Name", value=f"`{name}`", inline=False)
                        em.add_field(name="Alias", value=f"{', '.join(alx)} " if alias else f"`none`", inline=False)
                        em.add_field(name="Usage", value=f"`^{command1.name} {sig}`" if sig else f'`^{command1.name}`', inline=False)
                        em.add_field(name="Description", value=thehelp if thehelp else "Currently no help!", inline=False)
                        em.set_author(name="Help", icon_url = client_av.avatar_url)
                        em.set_footer(text="<> = needed │ [] = not needed")
                        await ctx.send(embed=em)

        except Exception as e:
            print(e)
    @commands.command()
    async def credits(self, ctx):
        coder = self.client.get_user(298043305927639041)
        designer = self.client.get_user(780555299106586634)
        helper = self.client.get_user(483631842554019841)
        helper2 = self.client.get_user(652407551849267200)
        embed = discord.Embed(title="Credits", description=f"""
        **Coder:** *{coder.name}*
        **Designer:** *{designer.name}*
        **Helpers:** *{helper.name}*, *{helper2.name}*
        
        
        
        
        
        """, color=xz)
        await ctx.send(embed=embed)
    @commands.command(hidden=True, aliases=['save', 'backup'])
    async def savebackup(self, ctx):
        x = 1
        for f in os.listdir('../backup'):
            if int(f[-3:]) > x:
                x = int(f[-3:])
            if int(x) >= 100:
                thefile = f'w{x+1}'
            elif int(x) >= 10:
                thefile = f'w0{x+1}'
            else:
                thefile = f'w00{x+1}'
        dirname = f'../backup/{thefile}'
        dirname1 = f'../backup/{thefile}/files'
        os.makedirs(dirname)
        os.makedirs(dirname1)


        for k in os.listdir('./'):
            if k not in ["__pycache__", "test.py", "cogs", "utils", "dicts"]:
                shutil.copy(f'./{k}', dirname1)
                
        for t in os.listdir('./cogs/'):
            if t != "__pycache__":
                shutil.copy(f'./cogs/{t}', dirname)
        await embed1(ctx, 'success', f'you have made a new backup folder called *{dirname}*')
    @commands.command(hidden=True)
    async def file(self, ctx, file):
        await ctx.send(file=discord.File(f"./dicts/{file}"))
    @commands.command(hidden=True)
    async def thecog(self, ctx):
        for thecog in self.client.cogs:

            cog = self.client.get_cog(thecog)

            await ctx.send(thecog)
    @commands.command(hidden=True)
    async def thetest(self, ctx):
        with open('./dicts/Emoji.json', 'r+') as k:
            data = json.load(k)
            data['emojis'] = {
                "Fun": "😎", 
                "Games": "🎮",
                "Moderation": "⚠",
                "Misc": "🤔",
                "Botinfo": "ℹ",
                "Economy": "💰"



            }
            Json(k, data)
   
    @commands.command(hidden=True)
    async def formathelp(self, ctx):
        
        x = 0 
        xy = []
        with open('./dicts/Help.json', 'r+') as K:
            data = json.load(K)
            for key in data:
                await ctx.send(key)
                
                y = data[key]['Cmds'].split(", ")
                await ctx.send(y)

                for t in y:
                    xy.append(f"`{t}`")

                    x += 1
                    if x == len(y):
                        data[key]['Cmds'] = ", ".join(xy)
                        await ctx.send(xy)
                        x = 0
                        xy = []
                    
                   
                        Json(K, data)
            await ctx.send('done')
    

    @commands.command(aliases=['colour'], description="change the color of the embeds!")
    async def color(self, ctx, *, args):
        if args.startswith('0x') and len(args) == 8:
            with open('./dicts/Color.json', 'r+') as k:
                data = json.load(k)
                data['Color']['color'] = args
                Json(k, data)
                embed = discord.Embed(title='changed', color=int(args, 16))
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Color", description='Put `0x` infront of the six letter/number [color](https://www.color-hex.com/)', colour=xz)
            await ctx.send(embed=embed)
def setup(client):
  client.add_cog(JesterInfo(client))

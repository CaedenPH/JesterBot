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
from discord_slash import SlashCommand
from bs4 import BeautifulSoup
YES = False
def Json(pref, data1):
    pref.seek(0)  # set point at the beginning of the file
    pref.truncate(0)  # clear previous content
    pref.write(json.dumps(data1, indent=4)) # write to file
selected_channel = None
class TheColor:
    def __init__(self):
        
        with open('./dicts/Color.json', 'r') as k:
            data = json.load(k)
            self.color = data['Color']['color'] 
    
    
xz = int(TheColor().color, 16)
            
        
class Event(commands.Cog):
    def __init__(self, client):

        self.client = client


       
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        print("Offline :(")

    @commands.Cog.listener()
    async def on_ready(self):
        
        
        guild_ids = []
        for guild1 in self.client.guilds:
            guild_ids.append(guild1.id)
        print(guild_ids)
        print("The bot is ready")
        print()
        selected_channel = self.client.get_guild(830161446523371540).get_channel(830161446523371545)
        # # for server in client.guilds:
        # #     # # chan = random.choice(server.text_channels)
        # #     # # invite = await chan.create_invite()
        # #     # print(server.name)
        # #     # await selected_channel.send(server.name + ' ')
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="^help  // Ping me for prefix"))

        

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        print(f"{channel.guild.name} {channel.name} got deleted")
        


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        chan = choice(guild.text_channels)
        invite = await chan.create_invite()
        selected_channel = self.client.get_guild(830161446523371540).get_channel(830161446523371545)
        print('I have joined', guild.name + '. Here is the invite: ', invite)
        await selected_channel.send(f'I have joined {guild.name}. Here is the invite: {invite}')
            
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print('I left', guild.name)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "🥵" and reaction.message.author == self.client.user:
            await reaction.message.delete()
            embed = discord.Embed(title="\u200b", colour=xz) 
            embed.add_field(name="Magic", value="\u200b") 
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="You do not have permissions to do that!", colour=xz)
            await ctx.send(embed=embed)
        elif isinstance(error, AttributeError):
            pass
        
        elif isinstance(error, commands.CheckFailure):
            pass
        
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f"<{error.param.name}>  is missing:", description=f"`^{ctx.command} {ctx.command.signature}`", colour=xz)
            embed.set_footer(text="<> = needed │ [] = not needed")
            await ctx.send(embed=embed)

        
        
        elif isinstance(error, commands.CommandNotFound):
            with open('./dicts/Suggest.json') as l:
                data = json.load(l)
                if str(ctx.channel.id) in data and data[str(ctx.channel.id)]['Yes'] == True:
                    return 
            y = []
            content = ctx.message.content
            content_replace = content.replace(ctx.prefix, '')
         
            for cmd in self.client.commands:
          
                if  cmd.name[:1] == content_replace[:1]:
                    
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
                
                
            
                # if string.endswith("---"):
                #     my_string += f" \n - `{str(string[:-3])}`"
                    # print(f"`{str(string[:-3])}`")
                my_string += f" \n - {str(string)}"
           
            
            num = 1
            my_string = my_string.split("---")

          
            embed = discord.Embed(title="Error!", colour=xz)
            embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
            
            if my_string[0] not in [""]:

                embed.add_field(name="Did you mean:", value=f"{my_string[0]}")
                
            msg = await ctx.send(embed=embed)
            def check(e, u):
                return u == ctx.author and e.message.id==msg.id

                
            if len(my_string) >= 2:
                if my_string[1] != "":

                    await msg.add_reaction("⬅")
                    await msg.add_reaction("➡")
                    await msg.add_reaction("⛔")
                    try:
                        emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                        
                        
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
            
        
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title=f"They are not a member!", colour=xz)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.RoleNotFound):
            embed = discord.Embed(title=f"That is not a member", colour=xz)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'This command is on cooldown for {error.retry_after:.2f} seconds', colour=xz)
            await ctx.send(embed=embed)
        # elif isinstance(error, commands.):
        #     await ctx.send('g')
        else:

            await ctx.send(error)
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # if payload.member_bot:
        #     pass 

        with open('./dicts/Reactionrole.json') as r:
            data = json.load(r)
            for x in data:
                if data[x]['emoji'] == payload.emoji.name and data[x]['message_id'] == payload.message_id:
                    role = discord.utils.get(self.client.get_guild(payload.guild_id).roles, id=data[x]['role_id'])
                    await self.client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass
        else:
            with open('./dicts/Reactionrole.json') as react:
                data = json.load(react)
                for x in data:
                
                    if data[x]['emoji'] == payload.emoji.name and data[x]['message_id'] == payload.message_id:
                        role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=data[x]['role_id'])
                        await payload.member.add_roles(role)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.client.wait_until_ready()
        if member.bot:
            return
        x = 0
        with open('./dicts/VerifyChannel.json') as k:
            data = json.load(k)
            
            for key in data:
                if "Yes" in data[key]:
                    if data[key]['Yes']:
                        if data[key]['Guild'] == member.guild.id:
                        
                            role = discord.utils.get(member.guild.roles, id=data[key]['URole id'])
                         
                            await member.add_roles(role)
                            x = 1
                            break
                        
                
            if x == 1:
                pass
            else:

                with open('./dicts/Welcome.json') as f:
                    loaded = json.load(f)
                    
                    if str(member.guild.id) in loaded:
                        if 'role' in loaded[str(member.guild.id)]:

                            if loaded[str(member.guild.id)]['message'] == "":
                                
                                channel = member.guild.get_channel(loaded[str(member.guild.id)]["channel_id"])
                                msg = await channel.send(f"{member.mention}")
                                await msg.delete()
                                embed = discord.Embed(title=f"Welcome!", description=f"{member.mention} don't forget to type ^rules to see the rules for the server, but most of all dont forget to have fun at {member.guild}!", colour=xz)
                                
                                embed.set_image(url=f"{member.guild.icon_url}") 
                                embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
                                # role = discord.utils.get(member.guild.roles, id=loaded[str(member.guild.id)]['role'])
                                await channel.send(embed=embed)
                                role = discord.utils.get(member.guild.roles, id=loaded[str(member.guild.id)]['role'])
                                if role:
                                    await member.add_roles(role)
                                else:
                                    pass
                            else:
                                channel = member.guild.get_channel(loaded[str(member.guild.id)]["channel_id"])
                                await channel.send(f"{loaded[str(member.guild.id)]['message']}")
                        else:
                            if loaded[str(member.guild.id)]['message'] == "":
                                channel = member.guild.get_channel(loaded[str(member.guild.id)]["channel_id"])
                                msg = await channel.send(f"{member.mention}")
                                await msg.delete()
                                embed = discord.Embed(description=f"Welcome to {member.guild}! {member.mention}, enjoy your stay!", colour=xz)
                                
                                embed.set_image(url=f"{member.guild.icon_url}") 
                                embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
                                
                                await channel.send(embed=embed)
                                # await member.add_roles(role)
                                # await member.add_roles(role)
                            else:
                                channel = member.guild.get_channel(loaded[str(member.guild.id)]["channel_id"])
                                await channel.send(f"{loaded[str(member.guild.id)]['message']}")
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        await self.client.wait_until_ready()
        with open('./dicts/Levels.json', 'r+') as k:
            data = json.load(k)
            
            if str(message.guild.id) in data:
                if str(message.author.id) in data[str(message.guild.id)]:
                    data[str(message.guild.id)][str(message.author.id)]['points'] += 1

                else:
                    data[str(message.guild.id)][str(message.author.id)] = {
                        "name": message.author.name,
                        "points": 1


                    }
                Json(k, data)
        zx = False

        #mg = str(message.guild.id)  
        
      

        #mc = str(message.channel.id)
        with open('./dicts/VerifyChannel.json') as k:
            data = json.load(k)
        
            
           
            if str(message.channel.id) in data:
                if data[str(message.channel.id)]['Yes'] == True:

                    if message.content != "verify":
                        await message.delete()
                    else:
                        role = discord.utils.get(message.guild.roles, id=data[str(message.channel.id)]['URole id'])
                        for roled in message.author.roles:
                            
                            
                            if roled.name in role.name:
                                zx = True
                                
                            else:
                                pass
                        if zx:

                            with open('./dicts/Welcome.json') as w:
                                weldata = json.load(w)
                                if str(message.guild.id) in weldata and weldata[str(message.guild.id)]['Welcome']:
                                    if 'role' in weldata[str(message.guild.id)]:

                                
                                        role = discord.utils.get(message.guild.roles, id=weldata[str(message.guild.id)]['role'])
                                        await message.author.add_roles(role)
                                    
                                        role = discord.utils.get(message.guild.roles, id=data[str(message.channel.id)]['URole id'])
                                        
                                
                            
                                        await message.author.remove_roles(role)

                                        

                                        await message.delete()
                                        if weldata[str(message.guild.id)]['message'] == "":
                                            
                                            channel = message.guild.get_channel(weldata[str(message.guild.id)]["channel_id"])
                                            msg = await channel.send(f"{message.author.mention}")
                                            await msg.delete()
                                            embed = discord.Embed(title=f"Welcome!", description=f"{message.author.mention} don't forget to type `.rules` to see the rules for the server, but most of all dont forget to have fun at {message.guild}!", colour=xz)

                                            embed.set_thumbnail(url=f"{message.guild.icon_url}") 
                                            embed.set_image(url='https://cdn.discordapp.com/attachments/847528639125258322/855559791384592404/360_F_361521131_tvclR3GrsVQBFVsUe1EPNFgH2MWIN1w7.png')
                                            embed.set_author(name=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")
                                            # role = discord.utils.get(member.guild.roles, id=loaded[str(member.guild.id)]['role'])
                                            await channel.send(embed=embed)
                                        
                                        else:
                                            channel = member.guild.get_channel(weldata[str(message.guild.id)]["channel_id"])
                                            await channel.send(f"{weldata[str(message.guild.id)]['message']}")
                                    
                                else:
                                
                                    role = discord.utils.get(message.guild.roles, id=int(data[str(message.channel.id)]['MRole id']))
                                    role1 = discord.utils.get(message.guild.roles, id=int(data[str(message.channel.id)]['URole id']))
                                    await message.author.add_roles(role)
                                    await message.author.remove_roles(role1)
                                    await message.delete()
                        else:
                            await message.delete()
                        
                

        with open('./dicts/Server.json', 'r+') as l:
            data = json.load(l)
            if message.author.id != 828363172717133874: 
                if str(message.guild.id) not in data:
                    data[str(message.guild.id)] = {
                        "Score": 1


                    }
                else:
                    data[str(message.guild.id)]['Score'] += 1
                
                l.seek(0)
                l.truncate(0)
                l.write(json.dumps(data, indent=4))
            

        with open('./dicts/Suggest.json') as ee:
            data = json.load(ee)
            us = self.client.get_user(828363172717133874)
            
        
            if str(message.channel.id) in data and data[str(message.channel.id)]['Yes'] == True:
                if message.content != "suggest":
                    await message.delete()
            
            
            
                

                    # embed = discord.Embed(title=f"Type .suggest to make a suggestion! You cannot type in the {message.channel.name}", colour=xz)
                    # await message.author.send(embed=embed)
                # else:
                #     await self.client.process_command(suggest)
            # , {data[message.channel.id]}

        # if 'Jesterbot' or 'Jester' or 'BestBot' or 'JesterBot' or 'jesterbot' in [message.content]:
        #     response = requests.get('https://official-joke-api.appspot.com/random_joke')
        #     fox = response.json()
        #     foxupdate = (fox["setup"]) 
        #     foxupdatey = (fox["punchline"])

        #     x = []
        #     prefix = await self.client.get_prefix(message)
        #     for pref in prefix:
        #         x.append(f"`{pref}`")
        #     embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
        #     │ My default prefix is: `.` │
        #     │ My prefix for you is: {', '.join(x)} │ 
        #     │ Type `.prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
            
            
            
        #     """, colour=xz)
        #     embed.set_author(name="JesterBot", icon_url=us.avatar_url)

        #     embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
        #     embed.set_footer(text="You can get more of these jokes with .joke!")
        # ['Jesterbot', 'Jester', 'BestBot', 'JesterBot', 'jesterbot']
        
        for item in ('Jesterbot', 'Jester', 'BestBot', 'JesterBot', 'jesterbot', 'jest', 'Jest', 'JB', 'jb', 'Jb'):
            if item in message.content:

                msg12 = ""
            # print()
                num = 1
                
                await message.add_reaction("👍")
                await message.add_reaction("👎")
                def check(e, u):
                    return u == message.author and e.message.id==message.id
                try:

                    emoji, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
                    while emoji.emoji not in ["👎"]:
                        async with message.channel.typing():
                            x = []
                            response = requests.get('https://official-joke-api.appspot.com/random_joke')
                            fox = response.json()
                            foxupdate = (fox["setup"]) 
                            foxupdatey = (fox["punchline"])
                            prefix = await self.client.get_prefix(message)
                            for pref in prefix:
                                x.append(f"`{pref}`")
                            embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
                            │ My default prefix is: `^`, `.` │
                            │ My prefix for you is: {', '.join(x)} │ 
                            │ Type `.prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
                            
                            
                            
                            """, colour=xz)
                            embed.set_author(name="JesterBot", icon_url=us.avatar_url)
                    
                            embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
                            embed.set_footer(text="You can get more of these jokes with .joke!")
                    
                        msg12 = await message.channel.send(embed=embed)
                        num = 2 
                        await message.remove_reaction(member=message.author, emoji="👍")
                        emoji, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
                        
                    
                    else:
                        if num == 2:
                            
                            await msg12.delete()
                            await message.remove_reaction(member=message.author, emoji="👎")




                except asyncio.TimeoutError:
                    
                    await message.remove_reaction(member=message.author, emoji="👍")
                    await message.remove_reaction(member=message.author, emoji="👎")
            

            

        if message.mentions:
            
            if self.client.user in message.mentions:
                if message.reference:
                    return
                async with message.channel.typing():
                    response = requests.get('https://official-joke-api.appspot.com/random_joke')
                    fox = response.json()
                    foxupdate = (fox["setup"]) 
                    foxupdatey = (fox["punchline"])

                    x = []
                    prefix = await self.client.get_prefix(message)
                    for pref in prefix:
                        x.append(f"`{pref}`")
                    embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
                    │ My default prefix is: `^`, `.` │
                    │ My prefix for you is: {', '.join(x)} │ 
                    │ Type `.prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
                    
                    
                    
                    """, colour=xz)
                    embed.set_author(name="JesterBot", icon_url=us.avatar_url)

                    embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
                    embed.set_footer(text="You can get more of these jokes with .joke!")
                return await message.channel.send(embed=embed)


            
def setup(client):
  client.add_cog(Event(client))

import discord, os, requests, json, asyncio, traceback
from async_timeout import timeout
from random import choice, randint
from core.utils.utils import thecolor, Json, thebed
from core.Context import Context
from core.utils.HIDDEN import dest

from dislash import SlashClient, ActionRow, Button
from discord.ext import commands
import datetime

from core.utils.comedy import joke
   
class Event(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
       
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        chan = choice(guild.text_channels)
        invite = await chan.create_invite()
        selected_channel1 = self.bot.get_guild(830161446523371540).get_channel(865309892776951808)
        print('I have joined', guild.name + '. Here is the invite: ', invite)
        await selected_channel1.send(f'I have joined {guild.name}. Here is the invite: {invite}')
        e = self.bot.get_emoji(863313854150606848)
        j = self.bot.get_emoji(863313855286607932)
        s = self.bot.get_emoji(863313855061164062)
        r = self.bot.get_emoji(863313855119360022)
        t = self.bot.get_emoji(863313855399329812)
        embed = discord.Embed(title=f"{j}{e}{s}{t}{e}{r}", description=f"""
        │ **My prefix is:** `j.` │
        │ Type `j.server_prefix <prefix>, [prefix], etc` 
        to change the prefix for the server │
        
        """, colour=thecolor())
       
        
        embed.add_field(name="Here is a joke for you:", value=f"│ {await joke()} │", inline=False)
        embed.set_footer(text="You can get more of these jokes with j.joke!")
        names = ['general', 'genchat', 'generalchat', 'general-chat', 'general-talk', 'gen', 'talk', 'general-1', '🗣general-chat','🗣', '🗣general']
        for k in guild.text_channels:
            if k.name in names:
                return await k.send(embed=embed)
        await guild.system_channel.send(embed=embed)
        
   
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        pass
    

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "🥵" and reaction.message.author == self.bot.user:
            await reaction.message.delete()
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.wait_until_ready()
        
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
                                embed = discord.Embed(title=f"Welcome!", description=f"{member.mention} don't forget to type `j.rules` to see the rules for the server, but most of all dont forget to have fun at {member.guild}!", colour=thecolor())
                                
                                embed.set_image(url=f"{member.guild.icon_url}") 
                                embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
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
                                embed = discord.Embed(description=f"Welcome to {member.guild}! {member.mention}, enjoy your stay!", colour=thecolor())
                                
                                embed.set_image(url=f"{member.guild.icon_url}") 
                                embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
                                
                                await channel.send(embed=embed)
                                # await member.add_roles(role)
                                # await member.add_roles(role)
                            else:
                                channel = member.guild.get_channel(loaded[str(member.guild.id)]["channel_id"])
                                await channel.send(f"{loaded[str(member.guild.id)]['message']}")
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if str(before.channel) == f"{member}-channel":
            if not after.channel:
                return await before.channel.delete()
        if str(after.channel) == 'Join to create channel:':
            
            if str(after) != str(before):
                await after.channel.clone(name=f'{member}-channel')
                channel = discord.utils.get(self.bot.get_all_channels(), name = f"{member}-channel") 
                guild = member.guild
                await channel.set_permissions(guild.default_role, view_channel=False)
                
                await member.move_to(channel)
                
         
    @commands.Cog.listener()
    async def on_message(self, message):    
        zx = False

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
                                            embed = discord.Embed(title=f"Welcome!", description=f"{message.author.mention} don't forget to type `j.rules` to see the rules for the server, but most of all dont forget to have fun at {message.guild}!", colour=thecolor())

                                            embed.set_thumbnail(url=f"{message.guild.icon_url}") 
                                            embed.set_image(url='https://cdn.discordapp.com/attachments/847528639125258322/855559791384592404/360_F_361521131_tvclR3GrsVQBFVsUe1EPNFgH2MWIN1w7.png')
                                            embed.set_author(name=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")
                                            # role = discord.utils.get(member.guild.roles, id=loaded[str(member.guild.id)]['role'])
                                            await channel.send(embed=embed)
                                        
                                        else:
                                            channel = self.bot.get_channel(weldata[str(message.guild.id)]["channel_id"])
                                            await channel.send(f"{weldata[str(message.guild.id)]['message']}")
                                    
                                else:
                                
                                    role = discord.utils.get(message.guild.roles, id=int(data[str(message.channel.id)]['MRole id']))
                                    role1 = discord.utils.get(message.guild.roles, id=int(data[str(message.channel.id)]['URole id']))
                                    await message.author.add_roles(role)
                                    await message.author.remove_roles(role1)
                                    await message.delete()
                        else:
                            await message.delete()
                        
        us = self.bot.user
        if message.author == self.bot.user:
            return

        for item in ('Jesterbot', 'JesterBot', 'jesterbot'):
            
            if item in message.content:

                msg12 = ""
            # print()
                num = 1
                
                await message.add_reaction("👍")
                await message.add_reaction("👎")
                def check(e, u):
                    return u == message.author and e.message.id==message.id
                try:

                    emoji, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                    while emoji.emoji not in ["👎"]:
                        async with message.channel.typing():
                            x = []
                            
                            prefix = await self.bot.get_prefix(message)
                            for pref in [prefix1 for prefix1 in prefix if not prefix1.startswith('<@')]:
                                x.append(f"`{pref}`")
                            embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
                            │ My default prefix is: `j.` │
                            │ My prefix for you is: {', '.join(x)} │ 
                            │ Type `j.prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
                            
                            
                            
                            """, colour=thecolor())
                            embed.set_author(name="JesterBot", icon_url=us.avatar_url)
                    
                            embed.add_field(name="Also here is a joke for you:", value=f"│ {await joke()} │", inline=False)
                            embed.set_footer(text="You can get more of these jokes with j.joke!")
                    
                        msg12 = await message.channel.send(embed=embed)
                        num = 2 
                        await message.remove_reaction(member=message.author, emoji="👍")
                        emoji, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                    
                    else:
                        if num == 2:
                            await msg12.delete()
                            try:
                                await message.clear_reactions()
                            except:
                                pass
                        else:
                            try:
                                await message.clear_reactions()
                            except:
                                pass
                except asyncio.TimeoutError:
                    try:
                        await message.clear_reactions()
                    except:
                        pass

        if message.mentions:
            
            if message.content in ('<@!828363172717133874>', 'help <@!828363172717133874>'):
                if message.reference:
                    return
                async with message.channel.typing():
                    x = []
                    prefix = await self.bot.get_prefix(message)
                    for pref in [prefix1 for prefix1 in prefix if not prefix1.startswith('<@')]:
                        x.append(f"`{pref}`")
                    embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
                    │ My default prefix is: `j.` │
                    │ My prefix for you is: {', '.join(x)} │ 
                    │ Type `.prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
                    
                    
                    
                    """, colour=thecolor())
                    embed.set_author(name="JesterBot", icon_url=us.avatar_url)

                    embed.add_field(name="Also here is a joke for you:", value=f"│ {await joke()} │", inline=False)
                    embed.set_footer(text="You can get more of these jokes with .joke!")
                return await message.channel.send(embed=embed)

    
            
def setup(bot):
  bot.add_cog(Event(bot))

import discord, os, requests, json, asyncio
from async_timeout import timeout
from random import choice, randint
from dutils import thecolor, Json, thebed
from dislash import SlashClient, ActionRow, Button
from discord.ext import commands
import datetime

   
class Event(commands.Cog):
    def __init__(self, client):

        self.client = client
       
    @commands.Cog.listener()
    async def on_ready(self):

        slash = SlashClient(self.client)
        
        guild_ids = []
        for guild1 in self.client.guilds:
            guild_ids.append(guild1.id)

        selected_channel = self.client.get_guild(830161446523371540).get_channel(830161446523371545)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"pings for prefix // {len(self.client.guilds)} servers"))
        self.client.launch_time = datetime.datetime.utcnow()
        self.client.chan = selected_channel
        self.client.discordcolor = 0x36393F

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        e = self.client.get_emoji(863313854150606848)
        j = self.client.get_emoji(863313855286607932)
        s = self.client.get_emoji(863313855061164062)
        r = self.client.get_emoji(863313855119360022)
        t = self.client.get_emoji(863313855399329812)
        embed = discord.Embed(title=f"{j}{e}{s}{t}{e}{r}", description=f"""
        │ **My prefix is:** `^`, `.` │
        │ Type `^server_prefix <prefix>, [prefix], etc` 
        to change the prefix for the server │
        
        """, colour=thecolor())
       
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        fox = response.json()
        foxupdate = (fox["setup"]) 
        foxupdatey = (fox["punchline"])
        embed.add_field(name="Here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
        embed.set_footer(text="You can get more of these jokes with ^joke!")
        await guild.system_channel.send(embed=embed)
        chan = choice(guild.text_channels)
        invite = await chan.create_invite()
        selected_channel1 = self.client.get_guild(830161446523371540).get_channel(865309892776951808)
        print('I have joined', guild.name + '. Here is the invite: ', invite)
        await selected_channel1.send(f'I have joined {guild.name}. Here is the invite: {invite}')
   
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        pass
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        selected_channel1 = self.client.get_guild(830161446523371540).get_channel(865309892776951808)
        
        await selected_channel1.send(f'I have left {guild.name}.')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "🥵" and reaction.message.author == self.client.user:
            await reaction.message.delete()
            

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description="You do not have permissions to do that!", colour=thecolor())
            await ctx.send(embed=embed)
        elif isinstance(error, AttributeError):
            pass
        elif isinstance(error, commands.CheckFailure):
            pass
        
        elif isinstance(error, commands.MissingRequiredArgument):
            com = str(ctx.command.signature)
            x = com.split(f"{error.param.name}")
            y = ""
            z = "  "
            for k in str(ctx.command):
                z += " "
            for e in error.param.name:
                y += "^"
            
            
            for k in range(0, len(x[0])):
                z += " "
            
            embed = discord.Embed(title=f"<{error.param.name}>  is missing:", description=f"```^{ctx.command} {ctx.command.signature}\n{z}{y}```", colour=thecolor())
            embed.set_footer(text="<> = needed │ [] = not needed")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandNotFound):
            with open('./dicts/Suggest.json') as l:
                data = json.load(l)
                if str(ctx.channel.id) in data and data[str(ctx.channel.id)]['Yes'] == True:
                    return   
            try:
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
                
                    my_string += f" \n - {str(string)}"
            
                
                num = 1
                my_string = my_string.split("---")

            
                embed = discord.Embed(title="Error!", colour=thecolor())
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
                            
                                    embed = discord.Embed(title="Error!", colour=thecolor())
                                    embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                    embed.add_field(name="Did you mean:", value=f"{my_string[1]}")
                                    embed.set_footer(text="Page 2")
                                    await msg.edit(embed=embed)
                                    await msg.remove_reaction(member=ctx.author, emoji="➡")
                                    num = 2

                                elif emoji.emoji == "⬅" and num == 2:
                                    embed = discord.Embed(title="Error!", colour=thecolor())
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
                                embed = discord.Embed(title="Error!", description="Goodbye", colour=thecolor())
                                embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                embed.set_footer(text="Have fun!")
                                return await msg.edit(embed=embed)
                                
                        except asyncio.TimeoutError:
                            embed = discord.Embed(title="Error!", description="Session timed out", colour=thecolor())
                            embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                            embed.set_footer(text="Have fun!")
                            return await msg.edit(embed=embed)
                
            except:
                pass
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(description=f"They are not a **member!**", colour=thecolor())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.RoleNotFound):
            embed = discord.Embed(description=f"That is not a **role!**", colour=thecolor())
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=f'This command is on cooldown for **{error.retry_after:.2f}** seconds', colour=thecolor())
            await ctx.send(embed=embed)
        else:
            k = open('./dicts/Errors.json', 'r+')
            data = json.load(k) 
            num = str(len(data))
            
            data[num] = {'author': ctx.author.name, 'id': ctx.author.id, 'error': str(error), 'error_dir': str(dir(error)), 'command': ctx.command.name}
            Json(k, data)
            await thebed(self.client.chan, f'{ctx.guild}; {ctx.author}; {ctx.command.name}', error)
            await thebed(ctx, '', error)
            
            
    
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
                                embed = discord.Embed(title=f"Welcome!", description=f"{member.mention} don't forget to type `^rules` to see the rules for the server, but most of all dont forget to have fun at {member.guild}!", colour=thecolor())
                                
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
                channel = discord.utils.get(self.client.get_all_channels(), name = f"{member}-channel") 
                guild = member.guild
                await channel.set_permissions(guild.default_role, view_channel=False)
                
                await member.move_to(channel)
                
                
                    
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        await self.client.wait_until_ready()
        
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
                                            embed = discord.Embed(title=f"Welcome!", description=f"{message.author.mention} don't forget to type `^rules` to see the rules for the server, but most of all dont forget to have fun at {message.guild}!", colour=thecolor())

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

        us = self.client.user
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
                            │ Type `^prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
                            
                            
                            
                            """, colour=thecolor())
                            embed.set_author(name="JesterBot", icon_url=us.avatar_url)
                    
                            embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
                            embed.set_footer(text="You can get more of these jokes with ^joke!")
                    
                        msg12 = await message.channel.send(embed=embed)
                        num = 2 
                        await message.remove_reaction(member=message.author, emoji="👍")
                        emoji, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
                    
                    else:
                        if num == 2:
                            await msg12.delete()
                            await message.clear_reactions()
                        else:
                            await message.clear_reactions()

                except asyncio.TimeoutError:
                    await message.clear_reactions()

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
                    
                    
                    
                    """, colour=thecolor())
                    embed.set_author(name="JesterBot", icon_url=us.avatar_url)

                    embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
                    embed.set_footer(text="You can get more of these jokes with .joke!")
                return await message.channel.send(embed=embed)

            
def setup(client):
  client.add_cog(Event(client))

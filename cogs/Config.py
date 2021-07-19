import discord
import json
from discord.ext.commands import has_permissions
from discord.ext import commands 
from discord.utils import get
from async_timeout import timeout
import asyncio
from dutils import thecolor, Json, thebed, Cmds

class Config(commands.Cog):
    def __init__(self, client):
   

        self.client = client
    
    @commands.command(aliases=['Welcomer', 'welcome'], description="Adds a welcome feature into the current channel (everytime someone joins the server it says welcome) - `[message]` is a good welcome message")
    @has_permissions(administrator=True)
    async def welcomechannel(self, ctx, role:discord.Role="",*,  message:str = ""):

        with open('./dicts/Welcome.json', 'r+') as f:
            if role == "":
                loaded = json.load(f)
                loaded[str(ctx.guild.id)] = {
                "message":    message,
                "name":       ctx.guild.name, 
                "channel_id": ctx.channel.id,
                "Welcome": True
            }   
                Json(f, data)
                embed = discord.Embed(title="Added!", colour=thecolor())
                await ctx.send(embed=embed)
            else:

                loaded = json.load(f)
                loaded[str(ctx.guild.id)] = {
                    "message":    message,
                    "name":       ctx.guild.name, 
                    "channel_id": ctx.channel.id,
                    "role": role.id,
                    "Welcome": True
                }   

                Json(k, data)
                embed = discord.Embed(title="Added!", colour=thecolor())
                await ctx.send(embed=embed)

    @commands.command(aliases=['channelconfig'])
    async def config(self, ctx):
        the_list = ""
        the_list1 = ""
        with open('./dicts/ConfigChannel.json', 'r+') as k:
            data = json.load(k)
            a = ""
            for z in data['emojis']:
                a += f"\n{z} │ {data['emojis'][z]['em']}"
            embed = discord.Embed(title="Config channels", description=a, color=thecolor())
            msg = await ctx.send(embed=embed)
            
            for e in data['emojis']:

                for k in data['emojis'][e]:
                    await msg.add_reaction(data['emojis'][e]['em'])
            try:
                emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda e, u:u == ctx.author and e.message.id==msg.id)
                while emoji.emoji != "fw":
                    for e in data['emojis']:
                        
                                    
                            if data['emojis'][e]['em'] == emoji.emoji:
                                    
                                    command1 = self.client.get_command(f'{e}')
                               
                                    sig = command1.signature
                                    alias = command1.aliases
                                    alx = []
                                    
                                    if alias:
                                        
                                        for al in command1.aliases:

                                            alx.append(f"`{al}`")
                                    client_av = self.client.get_user(828363172717133874)
                                    em = discord.Embed(description=Cmds(command1.name).chelp, colour=0x4286ff)
                                    name = f"{command1.name.capitalize()}"
                                    
                                    em.add_field(name="Name", value=f"`{name}`", inline=False)
                                    em.add_field(name="Alias", value=f"{', '.join(alx)} " if alias else f"`none`", inline=False)
                                    em.add_field(name="Usage", value=f"`^{command1.name} {sig}`" if sig else f'`^{command1.name}`', inline=False)
                                    
                                    em.set_author(name="Help", icon_url = client_av.avatar_url)
                                    em.set_footer(text="<> = needed │ [] = not needed")
                                    
                                
                                    
                                    
                                    
                                    
                                    await msg.remove_reaction(member=ctx.author, emoji=emoji)
                                    embed = discord.Embed(title=f"{data['emojis'][e]} │ {emoji}", description=f"{the_list1}", color=thecolor())
                                    
                                    await msg.edit(embed=em)
                                   
                    
                    emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda e, u:u == ctx.author and e.message.id==msg.id)
            except asyncio.TimeoutError:
                await msg.clear_reactions()

    @commands.command()
    @has_permissions(manage_channels=True)
    async def pickuplinechannel(self, ctx, channel:discord.TextChannel=""):
        if not channel: 
            channel = await ctx.guild.create_text_channel(name="Joke Channel")
        with open('./dicts/ConfigChannel.json', 'r+') as k:
            data = json.load(k)
            x = str(ctx.guild.id)
            i = str(channel.id)
            if x in data:

                if 'pickuplinechannel' not in data[x]:
                    data[x]['pickuplinechannel'] = i
                    Json(k, data)
                    return await thebed(ctx, 'Success')
            else:
                data[x] = {
                    'pickuplinechannel': i

                }
                Json(k, data)
                return await thebed(ctx, 'Success')

            await thebed(ctx, 'There is already a pickuplinechannel here or something went wrong')
    @commands.command()
    @has_permissions(manage_channels=True)
    async def jokechannel(self, ctx, channel:discord.TextChannel=""):
        if not channel: 
            channel = await ctx.guild.create_text_channel(name="Joke Channel")
        with open('./dicts/ConfigChannel.json', 'r+') as k:
            data = json.load(k)
            x = str(ctx.guild.id)
            i = str(channel.id)
            if x in data:

                if 'jokechannel' not in data[x]:
                    data[x]['jokechannel'] = i
                    Json(k, data)
                    return await thebed(ctx, 'Success')
            else:
                data[x] = {
                    'jokechannel': i

                }
                Json(k, data)
                return await thebed(ctx, 'Success')

            await thebed(ctx, 'There is already a jokechannel here or something went wrong')
        
    @commands.command()
    @has_permissions(manage_channels=True)
    async def quotechannel(self, ctx, channel:discord.TextChannel=""):
        if not channel: 
            channel = await ctx.guild.create_text_channel(name="Joke Channel")
        with open('./dicts/ConfigChannel.json', 'r+') as k:
            data = json.load(k)
            x = str(ctx.guild.id)
            i = str(channel.id)
            if x in data:

                if 'quotechannel' not in data[x]:
                    data[x]['quotechannel'] = i
                    Json(k, data)
                    return await thebed(ctx, 'Success')
            else:
                data[x] = {
                    'quotechannel': i

                }
                Json(k, data)
                return await thebed(ctx, 'Success')

            await thebed(ctx, 'There is already a quotechannel here or something went wrong')
        
    @commands.command()
    @has_permissions(manage_channels=True)
    async def factchannel(self, ctx, channel:discord.TextChannel=""):
        if not channel: 
            channel = await ctx.guild.create_text_channel(name="Joke Channel")
        with open('./dicts/ConfigChannel.json', 'r+') as k:
            data = json.load(k)
            x = str(ctx.guild.id)
            i = str(channel.id)
            if x in data:

                if 'factchannel' not in data[x]:
                    data[x]['factchannel'] = i
                    Json(k, data)
                    return await thebed(ctx, 'Success')
            else:
                data[x] = {
                    'factchannel': i

                }
                Json(k, data)
                return await thebed(ctx, 'Success')

            await thebed(ctx, 'There is already a factchannel here or something went wrong')






            
  
    @commands.command(aliases=['Unwelcome', 'Stop_Welcome'], description="Removes the ^welcome command")
    async def remove_welcome(self, ctx):
        with open('./dicts/Welcome.json', 'r+') as f:
            data = json.load(f)
            
            if str(ctx.guild.id) in data:
                data[str(ctx.guild.id)]['Welcome'] = False
                Json(f, data)
                embed = discord.Embed(title="Re`moved!", colour=thecolor())
                await ctx.send(embed=embed)
    @has_permissions(manage_channels=True)
    @commands.command(description="Makes the channel specified a suggestion channel - members can only type ^suggest or their message gets deleted. Nice and orderly")
    async def suggestchannel(self, ctx, channel:discord.TextChannel):

        with open('./dicts/Suggest.json', 'r+') as k:
            data = json.load(k)
            if str(channel.id) not in data:

                data[str(channel.id)] = {
                    "Yes": True,
                    


                }
                Json(k, data)
                if channel.id == ctx.channel.id:
                    pass
                else:
                    embed = discord.Embed(title="Applied", colour=thecolor())
                    await ctx.send(embed=embed)
                await channel.purge(limit=10000)
                embed1 = discord.Embed(title="Suggest", description="""
                This channel is now a suggestion only channel. 
                This means that you can only type `suggest`, which will formally create a ticket that only you can reply to. After giving a title and a description, your suggestion will be sent.
                Any messages that aren't `suggest` are automatically deleted
                """, colour=thecolor())
                x = await channel.send(embed=embed1)
                await x.pin()
                await channel.purge(limit=1)
            else:
                if data[str(channel.id)]['Yes'] == False:
                    data[str(channel.id)]['Yes'] = True
                    Json(k, data)
                    embed = discord.Embed(title="Applied", colour=thecolor())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Already applied", colour=thecolor())
                await ctx.send(embed=embed)


    @has_permissions(manage_channels=True)
    @commands.command(aliases=['removesuggestchannel', 'rschannel', 'remschannel'], description="Removes the channel specified as a suggestion channel")
    async def delsuggestchannel(self, ctx, channel:discord.TextChannel):

        with open('./dicts/Suggest.json', 'r+') as k:
            data = json.load(k)
            if str(channel.id) not in data:
            
                embed = discord.Embed(title="Already removed", colour=thecolor())
            else:
                data[str(channel.id)]['Yes'] = False
        
                Json(k, data)
                embed = discord.Embed(title="Removed", colour=thecolor())

            await ctx.send(embed=embed)

    @commands.command(aliases=['verify'], description="""
    Creates a channel/uses an existing channel to make the server be secure by adding the need to say `verify` to access the server...Remove with `^removeverify` 
    1. If channel is not given, this command will create a role called `⚘ Member ⚘` and a role called `⚘ Unverified ⚘`
    2. It will create a channel called `⚘ verify ⚘`
    3. When a new member joins they will only see the channel `⚘ verify ⚘`, and if they write `verify` they can text in and see all other channels""")
    @has_permissions(administrator=True)
    async def verifychannel(self, ctx, channel:discord.TextChannel=None, role:discord.Role=""):
        embed = discord.Embed(title="Warning", description="While this command can help your server by adding a verification, it can also add roles and channels you may not like the look of. To get more information type `^help verifychannel`. To proceed type y", colour=thecolor())
        await ctx.send(embed=embed)
        received_msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
        if received_msg != "y":
      
            embed = discord.Embed(title="Goodbye!", colour=thecolor())
            return await ctx.send(embed=embed)
        
        with open('./dicts/VerifyChannel.json') as k:
            data = json.load(k)
            
            for key in data:
                if "Yes" in data[key]:
                    if data[key]['Yes']:
                        if data[key]['Guild'] == ctx.guild.id:
                         
                            return await ctx.send('There is already a verify here!')
        if not channel:
            channel = await ctx.guild.create_text_channel(name="⚘ verify ⚘")                   
        with open('./dicts/VerifyChannel.json', 'r+') as k:
            print('works')
            if role == "":
                await ctx.guild.create_role(name="⚘ Member ⚘", permissions=discord.Permissions(send_messages=True))
            membrole = discord.utils.get(ctx.guild.roles, name="⚘ Member ⚘")
            await ctx.guild.create_role(name="⚘ Unverified ⚘", permissions=discord.Permissions(send_messages=False))
            Urole = discord.utils.get(ctx.guild.roles, name="⚘ Unverified ⚘")
            for x in ctx.guild.channels:
                if x.id == channel.id:
                    await x.set_permissions(membrole, send_messages=False, read_message_history=False, read_messages=False)
                else:

                    await x.set_permissions(membrole, speak=True, send_messages=True, read_message_history=True, read_messages=True)
                if x.id != channel.id:
                    await x.set_permissions(Urole, send_messages=False, read_message_history=False, read_messages=False)
                else:
                    await x.set_permissions(Urole, speak=True, send_messages=True, read_message_history=True, read_messages=True)

            every = discord.utils.get(ctx.guild.roles, name="@everyone")
            for y in ctx.guild.channels:
                await y.set_permissions(every, speak=True, send_messages=True, read_message_history=True, read_messages=True)
            with open('./dicts/Welcome.json') as w:
                weldata = json.load(w)
                if str(ctx.guild.id) in weldata:
                    g = discord.utils.get(ctx.guild.roles, id=weldata[str(ctx.guild.id)]['role'])
                    for z in ctx.guild.channels:
                        if z.id == channel.id:
                            await z.set_permissions(g, send_messages=False, read_message_history=False, read_messages=False)
                        else:

                            await z.set_permissions(g, speak=True, send_messages=True, read_message_history=True, read_messages=True)

            data = json.load(k)
            if str(channel.id) in data:
                embed = discord.Embed(title=f"Already applied!")
            else:
                data[str(channel.id)] = {
                    "Yes": True,
                    "MRole id": membrole.id,
                    "URole id": Urole.id,
                    "Guild": ctx.guild.id
                }

            Json(k, data)
        
            await channel.purge(limit=10000)
            embed1 = discord.Embed(title="Verify", description="""
            This channel is a verify channel. 
            Type `verify` to get acess to the server!
            Have fun and make sure to follow the rules.
            """, colour=thecolor())
            x = await channel.send(embed=embed1)
            await x.pin()
            embed = discord.Embed(title=f"Applied!")
            await ctx.send(embed=embed)
            await channel.purge(limit=1)

    @commands.command(aliases=['remverify'], description="removes the need for a verification")
    @has_permissions(administrator=True)
    async def removeverify(self, ctx):

        with open('./dicts/VerifyChannel.json', 'r+') as k:
            data = json.load(k)
            for key in data:
                if data[key]['Guild'] == ctx.guild.id:
                    del data[key]
                    Json(k, data)
                    embed = discord.Embed(title=f"Removed!", color=thecolor())
                    return await ctx.send(embed=embed)
                    
                
            await thebed(ctx, 'There was never a verify!')

    @commands.command()
    async def leavechannel(self, ctx, channel:discord.TextChannel=""):
        
        with open('./dicts/LeaveChannel.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.guild.id) in data:
                return await thebed(ctx, 'Leaving', 'This server is already registered!')
            else:

                if not channel:
                    channel = await ctx.guild.create_text_channel(name="Leaving Channel")
                data[str(ctx.guild.id)] = {
                    "id": channel.id
                }
                Json(k, data)
        await thebed(channel, 'This is a leaving channel, everyone who leaves will be announced here...')

    @commands.command()
    async def removeleavechannel(self, ctx, channel:discord.TextChannel):
        with open('./dicts/LeaveChannel.json', 'r+') as k:

            data = json.load(k)
            if str(ctx.guild.id) not in data:
                return await thebed(ctx, 'Leaving', 'There was never a leaving channel here!')
            del data[str(ctx.guild.id)]
            await thebed(ctx, 'Done!')

    @commands.Cog.listener()
    async def on_member_remove(self, memb):
        with open('./dicts/LeaveChannel.json', 'r+') as k:
            data = json.load(k)
           
            if str(memb.guild.id) in data:
                channel = self.client.get_channel(data[str(memb.guild.id)]['id'])
                await thebed(channel, 'Goodbye', f'You wil be missed *{memb.name}*...')

    
def setup(client):
  client.add_cog(Config(client))

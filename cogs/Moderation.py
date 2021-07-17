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
from datetime import datetime
from dutils import thecolor, Json, thebed
class Pag(Paginator):
    async def teardown(self):
        try:
            
            await self.page.clear_reactions()
            
        except discord.HTTPException:
            pass

class Mod(commands.Cog):
    def __init__(self, client):
        
        self.client = client
        

    @has_permissions(administrator=True)
    @commands.command(aliases=['del', 'deletes'], description="Deletes the specified channel, if no channel is specified - the current channel. Sends a warning.")
    async def delete(self, ctx, channel_id:int=""):
        embed = discord.Embed(title=f"This will delete the current channel, are you sure you want to procede? Type y if you do", colour=thecolor())
        await ctx.send(embed=embed)
        msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
        if msg == "y":
            
            if channel_id == "":
                
                await self.client.get_channel(self, ctx.channel.id).delete()
                
            else:
                
                x = await self.client.get_channel(channel_id).delete()
                embed = discord.Embed(title=f"{x} got deleted", colour=thecolor())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Goodbye", colour=thecolor())
            await ctx.send(embed=embed)
   
        
    @has_permissions(administrator=True)
    @commands.command(aliases=['nicks'], hidden=True)
    async def nick(self, ctx, member: discord.Member, *, nick):
        await member.edit(nick=nick)
        embed = discord.Embed(description=f'Nickname was changed for {member.mention} ', colour=thecolor())
        await ctx.send(embed=embed)
    
    @has_permissions(administrator=True)
    @commands.command(hidden=True, description="Deletes the specified invite", aliases=['deleteinv', 'invdelete', 'revokeinv', 'delinv', 'Invdel', 'Revinv', 'Invrev', 'Revokeinvite', 'Revoke_invite', 'xinv', 'X_inv', 'invitex', 'xinvite', 'Inv_x'])
    async def delete_invite(self, ctx, invite:str):
        embed = discord.Embed(title=f"Deleted invite", colour=thecolor())
        await ctx.send(embed=embed)
        await self.client.delete_invite(invite)

    @has_permissions(manage_messages=True)
    @commands.command(name='purge', aliases=['Message_delete', 'Msg_Del'], description="Purges the ammount of messages sent")
    async def _purge (self, ctx, amount=80):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title='Purge Sucsessful', value=f'Purge has been sucsessful.', colour =thecolor())
        embed.add_field(name='Congrats!', value='Your purge has been sucsessful')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def close(self, ctx):
        if ctx.author.id == 298043305927639041:
            embed = discord.Embed(title=f"Goodbye", colour=thecolor())
            await ctx.send(embed=embed)
            
            await self.client.close()

    @has_permissions(ban_members=True)
    @commands.command(aliases=['b', 'banhammer', 'bann'], description="Bans the specified member - Reason goes in the audit log")
    async def ban(self, ctx,member : discord.Member,*, reason = "No reason provided"):
        await member.send("You have been banned: " + reason)
        await member.ban(reason=reason)
        embed = discord.Embed(title="Banned", description=f"{member.mention}  got banned.", colour=thecolor())
        embed.add_field(name="Reason:", value=reason)
        user = ctx.author 
        await ctx.send(embed=embed)

    @has_permissions(ban_members=True)
    @commands.command(aliases=['ub', 'Revoke_Ban'], description="Unbans the specified member - Reason goes in the audit log")
    async def unban(self, ctx, user_id: int, *, reason = "No reason provided"):
        user = await ctx.bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        embed = discord.Embed(title="Unbanned", description=f"{user}  got unbanned.", colour=thecolor())
        embed.add_field(name="Reason:", value=reason)
        await ctx.send(embed=embed)
        await user.send("You have been unbanned")
    
    
    @has_permissions(manage_roles=True)
    @commands.command(aliases=['add', '+role', 'add_role'])
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):

        await member.add_roles(role)
        embed = discord.Embed(title="Addrole", description=f"{member.mention} got a role.", colour=thecolor())
        embed.add_field(name="Member:", value=member.mention, inline=False)
        embed.add_field(name="Role:", value=role.mention, inline=False)
        await ctx.send(embed=embed)
        
    @has_permissions(move_members=True)
    @commands.command(aliases=['m', 'move'], description="Moves a member from their current vc to the channel specified. If no channel has been specified it will kick the member from the vc.")
    async def move_to(self, ctx, member: discord.Member, channel: str): 
        await member.move_to(discord.utils.get(self, ctx.guild.voice_channels, name=channel))
        embed = discord.Embed(title="Moved", description=f"{member.mention} got moved. to {channel}", colour=thecolor())
        await ctx.send(embed=embed)

    @commands.command()
    async def deletemessages(self, ctx, user:discord.Member, limit=10):
        embed = discord.Embed(title="Working....", color=thecolor())
        x = await ctx.send(embed=embed)
        for channel in ctx.guild.text_channels:
            

            async for c in channel.history(limit=limit):
                if c.author == user:
                    await c.delete()
        embed = discord.Embed(title='Completed', description=f'{limit} messages from {user} are deleted in every channel', color=thecolor())
        await x.edit(embed=embed)


    @commands.command(name='purgewithoutmessage', aliases=['purge1'], hidden=True)
    async def _purge1 (self, ctx, amount=80, member:discord.Member=""):
        await ctx.channel.purge(limit=amount)

    @has_permissions(administrator=True)
    @commands.command(description="Set the prefix for JesterBot for the entire server (personal prefix changes are not affected")
    async def server_prefix(self, ctx, *, prefix=None):
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
                
                
                
                """, colour=thecolor())
                embed.set_author(name="JesterBot", icon_url=us.avatar_url)
        
                embed.add_field(name="Also here is a joke for you:", value=f"│ {foxupdate} ... {foxupdatey} │", inline=False)
                embed.set_footer(text="You can get more of these jokes with ^joke!")
            return await ctx.send(embed=embed)
        prefix = prefix.split(" ")
       
       
        if prefix:
        
            with open('./dicts/prefixes.json', 'r+') as e:
                data = json.load(e)
                if str(ctx.guild.id) in data:
                    data[str(ctx.guild.id)]['prefix'] = prefix

                else:
                    data[str(ctx.guild.id)]= {
                        "prefix": prefix


                    }
                Json(e, data)
            prefix1 = []
            for num in prefix:
                prefix1.append(f"`{num}`")
            embed = discord.Embed(description=f"New prefix for this server is {', '.join(prefix1) if prefix else f'{prefix1}'}!, ping me for my prefixes if you forget!", colour=thecolor())
            embed.set_author(icon_url=ctx.author.avatar_url, name="Prefix")
            await ctx.send(embed=embed)
    


    @commands.command(aliases=['k'], description="Kicks the specified member - Reason goes in the audit log")
    @has_permissions(kick_members=True)
    async def kick(self, ctx,member : discord.Member,*, reason = "No reason provided"):
        if member.bot:
            pass
        else:
            await member.send("You have been kicked: " + reason)
        await member.kick(reason=reason)
        embed = discord.Embed(title="Kicked", description=f"{member.mention}  got kicked.", colour=thecolor())
        embed.add_field(name="Reason:", value=reason)
        await ctx.send(embed=embed)



   
                
        

    @commands.command(aliases=['permrmute'], description="Indefinitely permreactmutes the member from adding reactions to messages")
    @has_permissions(manage_messages=True)
    async def permreactmute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="ReactMuted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="ReactMuted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=True, send_messages=True, read_message_history=True, read_messages=True, add_reactions=False)
        embed = discord.Embed(title="Muted", description=f"{member.mention} was react muted ", colour=thecolor())
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f"You have been reaction muted from: {guild.name} Reason: {reason}")


    @commands.command(description="Indefinitely mutes the member from sending messages")
    @has_permissions(manage_messages=True)
    async def permmute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False, read_messages=True)
        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=thecolor())
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" you have been muted from: {guild.name} Reason: {reason}")



    @commands.command(aliases=['unrmute', 'runmute'], description="Unreactmutes `<member>`")
    @has_permissions(manage_messages=True)
    async def unreactmute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild

        Reactmuted = discord.utils.get(guild.roles, name="ReactMuted")
    
        if Reactmuted not in member.roles:
            embed = discord.Embed(title="Member is not muted", description=f"{member.mention} is not react muted", colour=thecolor())
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted", colour=thecolor())
            embed.add_field(name="Reason:", value=reason, inline=False)
            await ctx.send(embed=embed)
            await member.remove_roles(Reactmuted, reason=reason)
            await member.send(f"You have been reaction muted from: {guild.name} Reason: {reason}")


    @commands.command(aliases=['unmut'], description="Unmutes `<member>`")
    @has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        Reactmuted = discord.utils.get(guild.roles, name="Muted")
    
        
        if Reactmuted not in member.roles:
            embed = discord.Embed(title="Member is not muted", description=f"{member.mention} is not muted", colour=thecolor())
            await ctx.send(embed=embed)

        else:

            embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted", colour=thecolor())
            embed.add_field(name="Reason:", value=reason, inline=False)
            await ctx.send(embed=embed)
            await member.remove_roles(Reactmuted, reason=reason)
            await member.send(f"You have been reaction muted from: {guild.name} Reason: {reason}")

    @commands.command(aliases=['tempmute'], description="Mutes the member from sending messages for `<time>` Format `time` like `1s` (second), `1m` (minute), `1h`(hour), 1d` (day)")
    @has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, time, *, reason=None):
        async with ctx.typing():

        
            if not reason:
                reason="No reason given"
            #Now timed mute manipulation
            try:
                seconds = time[:-1] #Gets the numbers from the time argument, start to -1
                duration = time[-1] #Gets the timed maniulation, s, m, h, d


                if duration == "s":
                    new_seconds = int(seconds) * 1
                elif duration == "m":
                    new_seconds = int(seconds) * 60
                elif duration == "h":
                    new_seconds = int(seconds) * 3600
                    
                elif duration == "d":
                    new_seconds = int(seconds) * 86400
                else:
                    embed = discord.Embed(title="Invalid duration input", colour=thecolor())
                    await ctx.send(embed=embed)
                    return

                
                
                
            except Exception as e:
                
                await ctx.send("Invalid time input")
                return  
            guild = ctx.guild
            Muted = discord.utils.get(guild.roles, name="Muted")
            lis = 1
            role_list = []
            for role in member.roles:
                if role.name != "@everyone":
                    role_list.append(role)
                    await member.remove_roles(role)
            if not Muted:
                Muted = await guild.create_role(name="Muted")
                for channel in guild.channels:
                    await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=False, read_messages=False)
                
            
                    
            await member.add_roles(Muted, reason=reason)
            muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted by {ctx.author.mention} for {reason} to {time}", colour=thecolor())
        await ctx.send(embed=muted_embed)
            
        await asyncio.sleep(int(new_seconds))
        await member.remove_roles(Muted)
        unmute_embed = discord.Embed(title="Mute over!", description=f'{ctx.author.mention} muted to {member.mention} for {reason} is over after {time}', colour=thecolor())
        await ctx.send(embed=unmute_embed)
        for role in role_list:
            await member.add_roles(role)

    @commands.command(aliases=['rmute'], description="Reactmutes the member from adding reactions to messages for `<time>` Format `time` like `1s` (second), `1m` (minute), `1h`(hour), 1d` (day)")
    @has_permissions(manage_messages=True)
    async def reactmute(self, ctx, member: discord.Member, time, *, reason="no reason"):
    
        
    

        #Now timed mute manipulation
        try:
            seconds = time[:-1] #Gets the numbers from the time argument, start to -1
            duration = time[-1] #Gets the timed maniulation, s, m, h, d
            if duration == "s":
                seconds = seconds * 1
            elif duration == "m":
                seconds = seconds * 60
            elif duration == "h":
                seconds = seconds * 60 * 60
            elif duration == "d":
                seconds = seconds * 86400
            else:
                embed = discord.Embed(title="Invalid duration input", colour=thecolor())
                await ctx.send(embed=embed)
                return
        except Exception as e:
            
            await ctx.send("Invalid time input")
            return
        guild = ctx.guild
        Muted = discord.utils.get(guild.roles, name="ReactMuted")
        if not Muted:
            Muted = await guild.create_role(name="ReactMuted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        await member.add_roles(Muted, reason=reason)
        muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted by {ctx.author.mention} for {reason} for {time}", colour=thecolor())
        await ctx.send(embed=muted_embed)
    
        
        await asyncio.sleep(int(seconds))
        await member.remove_roles(Muted)
        unmute_embed = discord.Embed(title="Mute over!", description=f'{ctx.author.mention} reactmuted {member.mention} for {reason} is over after {time}', colour=thecolor())
        await ctx.send(embed=unmute_embed)


    @has_permissions(administrator=True)
    @commands.command(aliases=['give_role', 'gv', 'give_rol'], description="Gives every member in the guild the specified role")
    async def give_roles(self, ctx, role:discord.Role):
        embed = discord.Embed(title="Working...", colour=thecolor())
        await ctx.send(embed=embed)
        role = discord.utils.get(ctx.guild.roles, id = role.id)
        for member in ctx.guild.members:
            await member.add_roles(role)
        embed = discord.Embed(title="Done", colour=thecolor())
        await ctx.send(embed=embed)

    


    @commands.command(description="Sends a list of all the server roles and positions (hierachy)")
    async def showroles(self, ctx):
        x = ""
        for role in ctx.guild.roles:
        
            if role.name != "@everyone":
                x += (f"`{role.name} - {role.position}` \n")
        # embed = discord.Embed(title=, colour=thecolor())
        # embed.add_field(value=f"{', '.join(x)}")
        # await ctx.send(embed=embed)
        if len(x) < 200:
                await ctx.send(x)
        
        else:
            pager = Pag(
                timeout=100,
                #entries=[f"`{result[1:][:-1]}`"[i: i + 2000] for i in range(0, len(result), 2000)],
                entries=[x[i: i + 1000] for i in range(0, len(x), 1000)],
                length = 1,
                prefix = "```py\n", 
                suffix = "```",
                colour=thecolor()
                )
            await pager.start(ctx)

    @commands.command(hidden=True)
    async def showroleperm(self, ctx, roled="member"):
        role = discord.utils.get(self, ctx.guild.roles, name=roled)
        
        for channel in ctx.guild.text_channels:
           pass
        embed = discord.Embed(description=role.permissions.name, colour=thecolor())
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        await ctx.send(embed=embed)
        await ctx.send(role.position)

    @commands.command()
    async def showrolepermid(self, ctx, id1:int):
        x = []
        for role in ctx.guild.roles:
            x.append(role.position)
        role = discord.utils.get(ctx.guild.roles, id=id1)
        
        for channel in ctx.guild.text_channels:
            pass

        embed = discord.Embed(description=role.name, colour=thecolor())
        embed.set_author(name=f"{role.position} / {max(x)}")
        await ctx.send(embed=embed)

    @commands.command()
    async def position(self, ctx, member:discord.Member):
        x = []
        for role in member.roles:
            if role.position != 0:
                x.append(f"**{role.name}** ---> {role.position}")
            
        embed = discord.Embed(description=" │ ".join(x), colour=thecolor())
        await ctx.send(embed=embed)

    
    @commands.command(hidden=True)
    async def get_person(self, ctx, id1):
        x = self.client.get_user(id1)
        await ctx.send(x.name)

   




def setup(client):
  client.add_cog(Mod(client))
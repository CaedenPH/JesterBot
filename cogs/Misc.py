import discord, os, requests, json, asyncio
from discord.ext import commands 
from async_timeout import timeout
from random import choice
from dutils import thecolor, Json, thebed
from discord import Webhook, AsyncWebhookAdapter

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def invited(self, ctx, user:discord.Member=None):
        if not user:
            user = ctx.author
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == user:
                totalInvites += i.uses
        await thebed(ctx, "", f"{user.name} has invited **{totalInvites}** member{'' if totalInvites == 1 else 's'} to the server!")

    @commands.command(aliases=['Channel_info', 'InfoChannel'])
    async def channel(self, ctx):

        channelname = ctx.channel.name
        channelid = ctx.channel.id

        servername = ctx.guild.name
        embed = discord.Embed(title="Your info", colour=thecolor())
        embed.add_field(name="Name", value=f"{channelname}", inline=False)
        embed.add_field(name="Id", value=f"{channelid}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(description="Make a secure password with a length that you can choose")
    async def password(self, ctx, lengthofpassword:int=12):
        
        my_list = ['!', '?', '#']
        for c in range(97, 123):
            my_list.append(chr(c))
        for e in range(1, 9):
            my_list.append(e)
        for t in range(65, 91):
            my_list.append(chr(t))
       
        password = ""
        while len(password) != lengthofpassword:
            password += str(choice(my_list))
        x = await ctx.author.send(password)
        await thebed(ctx, 'Password', f'||{x.jump_url}||')

    @commands.command(aliases=['stat'], description="Sends statistics about the server")
    async def stats(self, ctx):

        members, bots = [m for m in ctx.guild.members if not m.bot], [m for m in ctx.guild.members if not m.bot]
        embed = discord.Embed(title="Stats", color = thecolor())
        embed.add_field(name="Server statistics", value=f"""
    Text Channels: {len(ctx.guild.text_channels)}
    Voice Channels: {len(ctx.guild.voice_channels)}
    Total Channels: {len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)}
    Members (bots excluded): {len(members)}
    Bots: {len([m for m in ctx.guild.members if m.bot])}
    Roles in the server: {len(ctx.guild.roles)}
        """)
        await ctx.send(embed=embed)
    
    
    @commands.command(aliases=['Server_icon', 'Icon_server', 'Guild_icon', 'Server_Avatar', 'avg', 'guildav', 'gc'], description="Sends the avatar of the server (profile pic)", hidden=True)
    async def avatarguild(self, ctx):
        embed = discord.Embed(title='Guild icon', color=thecolor())
        embed.set_image(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
    @commands.command(aliases=['messages'], description="Says how many messages have been sent since the bot joined")
    async def servermessages(self, ctx, server=""):
        join = ctx.guild.get_member(828363172717133874)
        when = "24th of June 2021"
        joinedat = ""
        for k in str(join.joined_at):
            joinedat += k
        if int(joinedat[5:7]) > 6:
            if int(joinedat[7:9]) > 12:
                when = str(join.joined_at)
      
        with open('./dicts/Server.json') as k:
            data = json.load(k)
                
            if not server:

                embed = discord.Embed(title=f"{data[str(ctx.guild.id)]['Score']} messages since the {when}", colour=thecolor())
            else:
                embed = discord.Embed(title=f"{data[server]['Score']} messages since {when}", colour=thecolor())
            await ctx.send(embed=embed)

    @commands.command(aliases=['s', 'Sugg', 'Sug', 'Suggester'], description="Follow the instructions and a suggestion will appear")
    async def suggest(self, ctx):

        user = ctx.author.id
        username = self.client.get_user(user)

        try:
                        
            embed = discord.Embed(title="Suggestion", colour=thecolor())
            embed1 = discord.Embed(title=f"What is the title of your suggestion? Type end at any point to stop and type title to remove the description", colour=thecolor())
            x = await ctx.send(embed=embed1)
            received_msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
            if received_msg not in ["end", "title"]:
                msg1 = received_msg
                embed2 = discord.Embed(title=f"What is the description of your suggestion? Type end at any point to stop", colour=thecolor())
                y = await ctx.send(embed=embed2)
                received_msg1 = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                if received_msg1 != "end":
                    msg2 = received_msg1
                    embed.add_field(name="Title", value=msg1, inline=False)
                    embed.add_field(name="Description", value=msg2, inline=False)
                    embed.set_footer(text=ctx.author.name, icon_url=username.avatar_url)
                    
                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction("👍")
                    await msg.add_reaction("👎")
                    
                else:
                    embed3 = discord.Embed(title="Goodbye", colour=thecolor())
                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    msg = await ctx.send(embed=embed3)
                
            elif received_msg == "end":
                await x.delete()
                await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                embed3 = discord.Embed(title="Goodbye", colour=thecolor())
                await ctx.send(embed=embed3)
            else:
                embed2 = discord.Embed(title=f"What is the Title of your suggestion? Type end at any point to stop", colour=thecolor())
                y = await ctx.send(embed=embed2)
                received_msg1 = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                if received_msg1 != "end":

                    embed.add_field(name="Title", value=received_msg1, inline=False)
                    
                    embed.set_footer(text=ctx.author.name, icon_url=username.avatar_url)
                    
                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction("👍")
                    await msg.add_reaction("👎")
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Time ran out, restart the ticket", colour=thecolor())
            await ctx.send(embed=embed)
   
    @commands.command()
    async def rules(self, ctx):
        embed = discord.Embed(title="Standard Rules", description="", color=0xffd1dc)
        embed.add_field(name="`1` NSFW ", value="All NSFW outside of an nsfw channel is banned and you will be muted and even banned up to the severity of the content.", inline=False)
    
        embed.add_field(name="`2` Hate ", value="All forms of racism and homophobia will result in a ban with potential ban appeal in the near future after the ban.", inline=False)
    
        embed.add_field(name="`3` Toxicm ", value="Unless you're being toxic as a joke it's prohibited, please report anyone is is harassing//bullying you please report to any of the staff members!", inline=False)
    
        embed.add_field(name="`4` Advertising", value="Any form of advertising will be a kick & mute for every person, doesn't matter if it's in dms, chat, etc.", inline=False)
    
        embed.set_image(url = "https://i.pinimg.com/originals/09/9a/57/099a57d2fe430ea56cdc5ed4979ff909.gif")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def booster(self, ctx):
        embed = discord.Embed(title="Booster perks", description="Boosting this server can help give us many other perks! Although it's not required we would love for you to boost us!", color=0xffd1dc)
        embed.add_field(name="`1` Free role ", value="When you boost you'll be able to choose a role for you and a friend!", inline=False)
    
        embed.add_field(name="`2` Giveaway restrictions ", value="You will be able to bypass all giveaway restrictions!", inline=False)
    
        embed.add_field(name="`3` Role ", value="Custom booster role that is above members!", inline=False)
    
        embed.add_field(name="`4` Hugs", value="You'll get free hugs <3", inline=False)
    
        embed.set_image(url = "https://support.discord.com/hc/article_attachments/360029033111/nitro_tank_gif.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def nitro(self, ctx):
        embed = discord.Embed(title="Nitro perks", description="Nitro can improve discord experience and give many fun perks!", color=0xffd1dc)
        embed.add_field(name="`1` Live streams", value="Screen share on PC in `720p 60fps` or `1080p 30fps` - Stream at source", inline=False)
        embed.add_field(name="`2` Gif", value="Upload and use animated avatars and emojis", inline=False)
        embed.add_field(name="`3` Custom emojis", value="Share custom emojis across all servers", inline=False)
        embed.add_field(name="`4` Large file uploads", value="Larger file upload size from 8mb to 100mb with nitro or 50mb with nitro classic", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/803430815714902060/852926789981437982/image0.png")
        await ctx.send(embed=embed)
   
def setup(client):
  client.add_cog(Misc(client))

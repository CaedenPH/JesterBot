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
from discord.ext.buttons import Paginator
from traceback import format_exception
import animals
import vacefron

vace_api = vacefron.Client()

class Pag(Paginator):
    async def teardown(self):
        try:
            
            await self.page.clear_reactions()
            
        except discord.HTTPException:
            pass
def Json(pref, data1):
    pref.seek(0)  # set point at the beginning of the file
    pref.truncate(0)  # clear previous content
    pref.write(json.dumps(data1, indent=4)) # write to file
class TheColor:
    def __init__(self):
        
        with open('./dicts/Color.json', 'r') as k:
            data = json.load(k)
            self.color = data['Color']['color'] 
    
async def embed(ctx, title, description=""):
    embed = discord.Embed(title=title, color=xz)
    if description:

        embed = discord.Embed(title=title, description=description, color=xz)
    await ctx.send(embed=embed)   
xz = int(TheColor().color, 16)
class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client   
    @commands.command()
    async def name(self, ctx, *, name):
        list = []
        for k in name:
            if k == " ":
                list.append(' ')
            else:


                list.append(f':regional_indicator_{k}:')
        await embed(ctx, 'Name in emojis...', "".join(list))
    @commands.command()
    async def level(self, ctx, memb:discord.Member=""):
        if not memb:
            memb = ctx.author
        with open('./dicts/Levels.json') as k:
            data = json.load(k)
            if str(ctx.guild.id) in data:
                p = data[str(ctx.guild.id)][str(memb.id)]['points']
                x = data[str(ctx.guild.id)]['rankup']
                level = round(p / x)
                level1 = p / x
                embed = discord.Embed(title=f"Levels for {memb.name}", description=f"**Level:** {level} \n**Points:** {level1} / 20", color=xz)
                await ctx.send(embed=embed)
    
    
    @commands.command(hidden=True)
    async def raiseerror(self, ctx, error):
        raise error
    @commands.command(aliases=['Server_icon', 'Icon_server', 'Guild_icon', 'Server_Avatar', 'avg', 'guildav', 'gc'], help="Sends the avatar of the server (profile pic)", hidden=True)
    async def avatarguild(self, ctx):
        embed = discord.Embed(title='Guild icon', color=xz)
        embed.set_image(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
    @commands.command(aliases=['messages'], help="Says how many messages have been sent since the bot joined")
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
                
            if server == "":

            

                embed = discord.Embed(title=f"{data[str(ctx.guild.id)]['Score']} messages since the {when}", colour=xz)
            else:
                embed = discord.Embed(title=f"{data[server]['Score']} messages since {when}", colour=xz)
            await ctx.send(embed=embed)

    
    @commands.command(aliases=['s', 'Sugg', 'Sug', 'Suggester'], help="Follow the instructions and a suggestion will appear")
    async def suggest(self, ctx):
        user = ctx.author.id
        username = self.client.get_user(user)

        try:
                        
            embed = discord.Embed(title="Suggestion", colour=xz)
            embed1 = discord.Embed(title=f"What is the title of your suggestion? Type end at any point to stop and type title to remove the description", colour=xz)
            x = await ctx.send(embed=embed1)
            received_msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
            if received_msg not in ["end", "title"]:
                msg1 = received_msg
                embed2 = discord.Embed(title=f"What is the description of your suggestion? Type end at any point to stop", colour=xz)
                y = await ctx.send(embed=embed2)
                received_msg1 = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                if received_msg1 != "end":
                    msg2 = received_msg1
                    embed.add_field(name="Title", value=msg1, inline=False)
                    embed.add_field(name="Description", value=msg2, inline=False)
                    # embed.set_thumbnail(url=username.avatar_url_as(size=256))
                    embed.set_footer(text=ctx.author.name, icon_url=username.avatar_url)
                    # {username.avatar_url_as(size=256)} 
                    
                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction("👍")
                    await msg.add_reaction("👎")
                    
                else:
                    embed3 = discord.Embed(title="Goodbye", colour=xz)
                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    msg = await ctx.send(embed=embed3)
                
            elif received_msg == "end":
                await x.delete()
                await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                embed3 = discord.Embed(title="Goodbye", colour=xz)
                await ctx.send(embed=embed3)
            else:
                embed2 = discord.Embed(title=f"What is the Title of your suggestion? Type end at any point to stop", colour=xz)
                y = await ctx.send(embed=embed2)
                received_msg1 = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                if received_msg1 != "end":

                    embed.add_field(name="Title", value=received_msg1, inline=False)
                    
                    # embed.set_thumbnail(url=username.avatar_url_as(size=256))
                    embed.set_footer(text=ctx.author.name, icon_url=username.avatar_url)
                    # {username.avatar_url_as(size=256)} 
                    
                    await x.delete()
                    await y.delete()
                    await ctx.message.delete()
                    await ctx.channel.purge(limit=2, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction("👍")
                    await msg.add_reaction("👎")
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Time ran out, restart the ticket", colour=xz)
            await ctx.send(embed=embed)
   
    @commands.command()
    async def rules(self, ctx):
        embed = discord.Embed(title="Standard Rules", description="", color=0xffd1dc)
        embed.add_field(name="`1` NSFW ", value="All NSFW outside of <#851561842417467392> is banned and you will be muted and even banned up to the severity of the content.", inline=False)
    
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
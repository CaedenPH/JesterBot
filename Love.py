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
from dutils import color, Json, thebed


# def Json(pref, data1):
#     pref.seek(0)  # set point at the beginning of the file
#     pref.truncate(0)  # clear previous content
#     pref.write(json.dumps(data1, indent=4)) # write to file
# class TheColor:
#     def __init__(self):
        
#         with open('./dicts/Color.json', 'r') as k:
#             data = json.load(k)
#             self.color = data['Color']['color'] 
    
# async def embed1(ctx, title, description=""):
#     embed = discord.Embed(title=title, color=color())
#     if description:

#         embed = discord.Embed(title=title, description=description, color=color())
#     await ctx.send(embed=embed)
# color() = int(TheColor().color, 16)
class Love(commands.Cog):
    def __init__(self, client):

        self.client = client

    @commands.command()
    async def love(self, ctx):
        await thebed(ctx, 'Name 1')
        received_msg = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
        await thebed(ctx, 'Name 2?')
        received_msg1 = str((await self.client.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content).lower()
        try:
            x = int(received_msg)
            z = int(received_msg1)
            await thebed(ctx, 'That isnt a name...')
        except:
            first_letter1 = received_msg[:1]
            last_letter1 = received_msg[-1:]
            first_letter2 = received_msg1[:1]
            last_letter2 = received_msg1[-1:]
            result1 = (ord(first_letter1)) - 85
            result2 = (ord(last_letter1)) - 85
            result3 = (ord(first_letter2)) - 85
            result4 = (ord(last_letter2)) - 85

            over = result1 + result2
            over1 = result3 + result4

            over2 = over + over1

            for k in ('e', 'l', 'i', 's', 'a'):
                if k in received_msg:
                    over2 += 3
                if k in received_msg1:
                    over2 += 3
           
            if over2 > 100:
                over2 -= 71

            
            await thebed(ctx, f"Compatabiliy between {received_msg} and {received_msg1}" , f"**Percentage:** {over2}%")
            

            
    @commands.command(aliases=['marrage'])
    async def family(self, ctx):
        File = GetUser('Love.json', f'{str(ctx.author.id)}', 'marriage')
        if File.family:

            embed = discord.Embed(title="👨 Family 👩", description=f"**{ctx.author.name}** x **{File.family}** \n They have been married since {File.data[str(ctx.author.id)]['since']}", color=color())
            embed.set_footer(text="\nMay ever hapiness bless them")
            await ctx.send(embed=embed)
        else:
            await thebed(ctx, 'Marriage', 'You are single bro...')
        
        
        
    @commands.command()
    async def marry(self, ctx, member:discord.Member):
        if member == ctx.author:
            return await thebed(ctx, 'You cannot marry yourself...')
        embed = discord.Embed(title="🎉 Marriage 🎉", description=f"**{member.name}** do you accept **{ctx.author.name}** to be your partner? React with this message if you want to get married", colour=color())
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('💖')
        partner = member
        try:
            emoji, user = await self.client.wait_for('reaction_add', timeout=300.0, check=lambda e, u:u == member and e.message.id==msg.id)
            File = GetUser('Love.json')
            
            if str(ctx.author.id) in File.data:
                arr = File.data[str(ctx.author.id)]['id']
                del File.data[str(arr)]
                us = self.client.get_user(int(arr))
                await us.send(f'You got divorced from {ctx.author.name} and they married {member.name}!')
                File.data[str(ctx.author.id)]['marriage'] = partner.name    
                File.data[str(member.id)]['id'] = str(partner.id)
                File.data[str(ctx.author.id)]['since'] = str(ctx.message.created_at)
                
            
            else:
                File.data[str(ctx.author.id)] = {
                    'marriage': partner.name,
                    'since': str(ctx.message.created_at),
                    'id': str(partner.id)


                }
                
           
            
            if str(member.id) in File.data:
                File.data[str(member.id)]['marriage'] = ctx.author.name
                File.data[str(member.id)]['id'] = str(ctx.author.id)
                File.data[str(member.id)]['since'] = str(ctx.message.created_at)
            
            else:
                
                File.data[str(member.id)] = {
                    'marriage': ctx.author.name,
                    'since': str(ctx.message.created_at),
                    'id': str(ctx.author.id)


                }
            
            Json(File.file, File.data)
            em = discord.Embed(title="Success!", description="Ah, the wonders of life, congratulations on getting married!", color=color())
            em.set_image(url="https://giphy.com/clips/livingsingle-7GN899Bf6g98SdFpra")
            await ctx.send(embed=em)
        except asyncio.TimeoutError:
            await thebed(ctx, 'Marriage', f'Oh no! {member} did not respond in time! Try again at a time that {member.name} is available...')

        
        
    @commands.command()
    async def divorce(self, ctx):
        File = GetUser('Love.json')
        if str(ctx.author.id) in File.data:
            marr = File.data[str(ctx.author.id)]['id']
            
            del File.data[str(marr)]
            del File.data[str(ctx.author.id)]
           
            Json(File.file, File.data)
            await thebed(ctx, 'Divorce...', 'They were such a good couple :(')
        else:
            await thebed(ctx, 'Marriage', 'You are single bro...')

def setup(client):
  client.add_cog(Love(client))

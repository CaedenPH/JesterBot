import discord, os, requests, json, asyncio
from async_timeout import timeout
from random import choice, randint
from dutils import thecolor, Json, thebed
from discord.ext import commands 
from discord_components import DiscordComponents
from datetime import datetime
   
class Snipe(commands.Cog):
    def __init__(self, client):

        self.client = client


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open('./dicts/Snipe.json', 'r+') as k:
            data = json.load(k)   
            g = str(message.guild.id)
            c = str(message.channel.id)
            if g in data:
                if c in data[g]:

                    data[g][c]['list'].append(message.content)
                    data[g][c]['author'].append(message.author.name)
                    data[g][c]['id'].append(message.author.id)
                    data[g][c]['time'].append(str(message.created_at))
                

                else:
                    data[g][c] = {
                        'list': [message.content],
                        'author': [message.author.name],
                        'id': [message.author.id],
                        'time': [str(message.created_at)]

                    } 
                    
            else:
                data[g] = {
                    c: {
                        'list': [message.content],
                        'author': [message.author.name],
                        'id': [message.author.id],
                        'time': [str(message.created_at)]

                    }
                }
            Json(k, data)
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        with open('./dicts/ESnipe.json', 'r+') as k:
            data = json.load(k)   
            g = str(before.guild.id)
            c = str(before.channel.id)
            if g in data:
                if c in data[g]:

                    data[g][c]['before'].append(before.content)
                    data[g][c]['after'].append(after.content)
                    data[g][c]['author'].append(before.author.name)
                    data[g][c]['id'].append(before.author.id)
                    data[g][c]['time'].append(str(before.created_at))
                

                else:
                    data[g][c] = {
                        
                        'author': [before.author.name],
                        'id': [before.author.id],
                        'time': [str(before.created_at)],
                        'after': [after.content],
                        'before': [before.content]

                    } 
                    
            else:
                data[g] = {
                    c: {
                        'list': [before.content],
                        'author': [before.author.name],
                        'id': [before.author.id],
                        'time': [str(before.created_at)],
                        'after': [after.content],
                        'before': [before.content]

                    }
                }
            Json(k, data)

    @commands.command(aliases=['esnipe'])
    async def editsnipe(self, ctx, ammount:int=1):
        with open('./dicts/Snipe.json') as k:
            data = json.load(k)
            g = str(ctx.guild.id) 
            c = str(ctx.channel.id)
            if g in data:
                if c in data[g]:
                    if len(data[g][c]['id']) >= ammount:
                        us = self.client.get_user(data[g][c]['id'][len(data[g][c]['before'])-ammount])
                        embed = discord.Embed(description=f"**{data[g][c]['author'][len(data[g][c]['before'])-ammount]} said:** {data[g][c]['before'][len(data[g][c]['before'])-ammount]} \n**Then edited it to:** {data[g][c]['after'][len(data[g][c]['after'])-ammount]}", color=thecolor())
                        embed.set_footer(text="At: " + str(data[g][c]['time'][len(data[g][c]['before'])-ammount][:-7]))
                        embed.set_author(icon_url=us.avatar_url, name="Most recent message:")
                        return await ctx.send(embed=embed)
                    else:
                        await ctx.message.add_reaction('❌')
                        return await thebed(ctx, '', 'The sniped messages dont go back that far!')

            await thebed(ctx, '', 'No deleted messages were ever here!')
    @commands.command(aliases=['eaim'])
    async def editaim(self, ctx, user:discord.Member):
        with open('./dicts/Snipe.json') as k:
            data = json.load(k)
            g = str(ctx.guild.id) 
            c = str(ctx.channel.id)
            
            if g in data:
                if c in data[g]:
                    t = len(data[g][c]['id'])
                  
                    for e in data[g][c]['id'][::-1]:
                        if e == user.id:
                            us = self.client.get_user(data[g][c]['id'][t-1])
                            embed = discord.Embed(description=f"**{data[g][c]['author'][t-1]} said:** {data[g][c]['before'][t-1]}\n**Then changed it to: **{data[g][c]['after'][t-1]}", color=thecolor())
                            embed.set_footer(text="At: " + str(data[g][c]['time'][t-1][:-7]))
                            embed.set_author(icon_url=us.avatar_url, name="Most recent message:")
                            return await ctx.send(embed=embed)
                            
                            
                        t -= 1


            await thebed(ctx, '', 'No deleted messages were ever here!')         
    @commands.command()
    async def snipe(self, ctx, ammount:int=1):
        with open('./dicts/Snipe.json') as k:
            data = json.load(k)
            g = str(ctx.guild.id) 
            c = str(ctx.channel.id)
            if g in data:
                if c in data[g]:
                    if len(data[g][c]['id']) >= ammount:
                        us = self.client.get_user(data[g][c]['id'][len(data[g][c]['list'])-ammount])
                        embed = discord.Embed(description=f"**{data[g][c]['author'][len(data[g][c]['list'])-ammount]} said:** {data[g][c]['list'][len(data[g][c]['list'])-ammount]}", color=thecolor())
                        embed.set_footer(text="At: " + str(data[g][c]['time'][len(data[g][c]['list'])-ammount][:-7]))
                        embed.set_author(icon_url=us.avatar_url, name="Most recent message:")
                        return await ctx.send(embed=embed)
                    else:
                        await ctx.message.add_reaction('❌')
                        return await thebed(ctx, '', 'The sniped messages dont go back that far!')

            await thebed(ctx, '', 'No deleted messages were ever here!')
    
    @commands.command()
    async def aim(self, ctx, user:discord.Member):
        with open('./dicts/Snipe.json') as k:
            data = json.load(k)
            g = str(ctx.guild.id) 
            c = str(ctx.channel.id)
            
            if g in data:
                if c in data[g]:
                    t = len(data[g][c]['id'])
                  
                    for e in data[g][c]['id'][::-1]:
                        if e == user.id:
                            us = self.client.get_user(data[g][c]['id'][t-1])
                            embed = discord.Embed(description=f"**{data[g][c]['author'][t-1]} said:** {data[g][c]['list'][t-1]}", color=thecolor())
                            embed.set_footer(text="At: " + str(data[g][c]['time'][t-1][:-7]))
                            embed.set_author(icon_url=us.avatar_url, name="Most recent message:")
                            return await ctx.send(embed=embed)
                            
                            
                        t -= 1


            await thebed(ctx, '', 'No deleted messages were ever here!')




def setup(client):
  client.add_cog(Snipe(client))

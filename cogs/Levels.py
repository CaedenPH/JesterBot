import discord, os, requests, json, asyncio
from discord.ext import commands 
import randfacts
from random import choice, randint
import vacefron
import asyncpraw
from dutils import thecolor, Json, thebed
reddit = asyncpraw.Reddit(client_id = "GfF3CEfYXsz3yw", client_secret = "_gRjhHHlRcb9uWoaJQbJddtqc-E", username = "Codex_2006", password = "senuka123", user_agent = "Codex")
vace_api = vacefron.Client()


class Levels(commands.Cog):
    def __init__(self, client):

        self.client = client
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
                embed = discord.Embed(title=f"Levels for {memb.name}", description=f"**Level:** {level} \n**Points:** {level1} / 20", color=thecolor())
                await ctx.send(embed=embed)
    
    
    @commands.command()
    async def levels(self, ctx, rankup:int=20):
        with open('./dicts/Levels.json', 'r+') as k:
            data = json.load(k)
            g = str(ctx.guild.id)
            if g in data:
                return await thebed(ctx, '', 'This server is already registered!')
            data[g] = {
                "true": True,
                "rankup": rankup

            }
            Json(k, data)
            await thebed(ctx, '', 'Applied!')
            
    @commands.command()
    async def removelevels(self, ctx):
        with open('./dicts/Levels.json', 'r+') as k:
            data = json.load(k)
            g = str(ctx.guild.id)
            if g not in data:
                return await thebed(ctx, '', 'This server was never registered!')
            del data[g]
            Json(k, data)
            await thebed(ctx, '', 'Removed!')


def setup(client):
  client.add_cog(Levels(client))

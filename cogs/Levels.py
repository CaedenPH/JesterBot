import discord, os, requests, json, asyncio
from discord.ext import commands 
import randfacts
from random import choice, randint
import vacefron
import asyncpraw
from discord.ext.commands import has_permissions
from dutils import thecolor, Json, thebed
reddit = asyncpraw.Reddit("shh")
vace_api = vacefron.Client()


class Levels(commands.Cog):
    def __init__(self, client):

        self.client = client
    @commands.command(aliases=['levels', 'lvl', 'levl', 'lvel'])
    async def level(self, ctx, memb:discord.Member=""):
        if not memb:
            memb = ctx.author
        with open('./dicts/Levels.json') as k:
            data = json.load(k)
            if str(ctx.guild.id) in data:
                
                p = data[str(ctx.guild.id)][str(memb.id)]['points']
                x = data[str(ctx.guild.id)]['rankup']
                level = p
                level1 = level / x
                embed = discord.Embed(title=f"", description=f"**Messages sent:** {level} \n**Level:** {level1}", color=thecolor())
                name = memb.name
                n = ""
                for zx in name:
                    e = zx.lower()
                    if ord(e) >= 97 and ord(e) <= 123:
                        n += e
                        
                embed.set_author(icon_url=memb.avatar_url, name=f"Levels for {n}")
                await ctx.send(embed=embed)
            else:
                await thebed(ctx, '', 'No levels config!')
    @commands.Cog.listener('on_message')
    async def leveltest(self, message):
        try:
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
        except:
            pass
    @commands.command(aliases=['configlevel'])
    @has_permissions(manage_messages=True)
    async def configlevels(self, ctx, rankup:int=20):
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
    @has_permissions(manage_messages=True)
    async def removelevels(self, ctx):
        with open('./dicts/Levels.json', 'r+') as k:
            data = json.load(k)
            g = str(ctx.guild.id)
            if g not in data:
                return await thebed(ctx, '', 'This server was never registered!')
            del data[g]
            Json(k, data)
            await thebed(ctx, '', 'Removed!')

    @commands.command(aliases=['leveltop', 'lb'])
    async def leaderboard(self, ctx):
        with open('./dicts/Levels.json') as k:
            

            data = json.load(k)
            if not str(ctx.guild.id) in data:
                return await thebed(ctx, '', 'You do not have a levels config! Type `configlevels` to add one!')
            score_list = []
            sorted_score_dict = {}
            
            x = []
            y = '\n'
        
            def get_key(item):
                return item[1]['points']
            rank = data[str(ctx.guild.id)]['rankup']
            del data[str(ctx.guild.id)]['true']
            del data[str(ctx.guild.id)]['rankup']
            
            sorted_scores = sorted(data[str(ctx.guild.id)].items(), key=get_key, reverse=True)[:11]
        
            for item in sorted_scores:
                lvl = item[1]['points'] / rank
                x.append(f"**{item[1]['name']}:** Level {str(lvl)[:1]}")
            await thebed(ctx, 'Leaderboard', "\n".join(x))
def setup(client):
  client.add_cog(Levels(client))

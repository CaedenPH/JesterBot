import discord, os, requests, json, asyncio
from discord.ext import commands 
import randfacts
from random import choice, randint
import vacefron
import asyncpraw
from dutils import thecolor, Json, thebed
reddit = asyncpraw.Reddit(client_id = "GfF3CEfYXsz3yw", client_secret = "_gRjhHHlRcb9uWoaJQbJddtqc-E", username = "Codex_2006", password = "senuka123", user_agent = "Codex")
vace_api = vacefron.Client()


class Feedback(commands.Cog):
    def __init__(self, client):

        self.client = client
    @commands.command()
    async def feedback(self, ctx, *, feedback):
        with open('./dicts/Feedback.json', 'r+') as k:
            data = json.load(k)
            data['feedback']['message'].append(feedback)
            data['feedback']['author'].append(ctx.author.name)
            Json(k, data)

            await thebed(ctx, '', 'Sent!')

    @commands.command()
    async def viewfeedback(self, ctx, distance:int=0):
        with open('./dicts/Feedback.json', 'r+') as k:
            data = json.load(k)
            await thebed(ctx, 'Feedback', f'*`{distance}`*: "{data["feedback"]["message"][distance]}", submitted by **{data["feedback"]["author"][distance]}**')





def setup(client):
  client.add_cog(Feedback(client))

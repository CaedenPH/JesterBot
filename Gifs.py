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
import randfacts
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from random import choice, randint
import io
import textwrap
import contextlib
from discord.ext.buttons import Paginator
from traceback import format_exception
import vacefron
import asyncpraw
#from dutils import color, Json, embed1, GetUser
reddit = asyncpraw.Reddit(client_id = "GfF3CEfYXsz3yw", client_secret = "_gRjhHHlRcb9uWoaJQbJddtqc-E", username = "Codex_2006", password = "senuka123", user_agent = "Codex")
vace_api = vacefron.Client()
def Json(pref, data1):
    pref.seek(0)  # set point at the beginning of the file
    pref.truncate(0)  # clear previous content
    pref.write(json.dumps(data1, indent=4)) # write to file

class TheColor:
    
    def __init__(self):
        
        with open('./dicts/Color.json', 'r') as k:
            data = json.load(k)
            self.color = data['Color']['color'] 
    
    
xz = int(TheColor().color, 16)

class JesterJokes(commands.Cog):
    def __init__(self, client):

        self.client = client

    @commands.command(aliases=['ranfact', 'rf', 'randomfact'], help="""Returns a random fact [ranfact, rf]""")
    async def fact(self, ctx):
        

        fact = randfacts.getFact()
        embed=discord.Embed(color=discord.Color.random())
        embed.add_field(name="Random Fact", value=fact)
        await ctx.send(embed=embed)

    
    @commands.command(help="""Returns a random quote""")
    async def quote(self, ctx):
        
        response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
        embed=discord.Embed(color=discord.Color.random())
        embed.add_field(name="Quote", value='*"{quoteText}"*\n ---  {quoteAuthor} --- '.format(**json.loads(response.text)))
        await ctx.send(embed=embed)
   
    @commands.command(help="""Returns a random quote""")
    async def quote1(self, ctx):
        
        response = requests.get('https://zenquotes.io/api/quotes/[your_key]')
        fox = response.json()
        embed=discord.Embed(color=discord.Color.random())
        embed.add_field(name="Quote", value=f"{fox[1]['q']}")
        await ctx.send(embed=embed)
   

    @commands.command(help="""Returns a random Pickup Line.""")
    async def redit(self, ctx, *, redt):
        async with ctx.typing():
            subreddit = await reddit.subreddit(redt)
            pickupline = await subreddit.random()
            

            if pickupline.title:
                if pickupline.selftext:
                    embed = discord.Embed(title=pickupline.title, description=pickupline.selftext ,color=discord.Color.random())
                else:
                    embed = discord.Embed(title=pickupline.title, description=pickupline.selftext, color=discord.Color.random())
            if pickupline.selftext:
                embed = discord.Embed(title=pickupline.selftext, color=discord.Color.random())
            embed.set_author(name=redt)
        await ctx.send(embed=embed)
    @commands.command(aliases=['pl', 'pickup', 'pickline'], help="""Returns a random Pickup Line.""")
    async def pickup_line(self, ctx):
        async with ctx.typing():
            subreddit = await reddit.subreddit("pickuplines")
            pickupline = await subreddit.random()

            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name=pickupline.title, value=pickupline.selftext)
        await ctx.send(embed=embed)
    @commands.command(aliases=['insultme', 'Mean', 'Insult_Me'], help="The specified member gets insulted")
    async def insult(self, ctx, user:discord.Member=""):
        
        
        m = self.client.get_user(828363172717133874)
        if user == "":
            user = self.client.get_user(ctx.author.id)
        
        if user == m:
            embed = discord.Embed(colour=xz)
            user = self.client.get_user(ctx.author.id)
            embed = discord.Embed(title="You shmuck...I am god")
            await ctx.send(embed=embed)
        else:

            response = requests.get('https://insult.mattbas.org/api/insult.json')
            fox = response.json()
            foxupdate = (fox["insult"]) 
            embed = discord.Embed(description=f"{user.mention} {foxupdate}", colour=xz)
            
            
            await ctx.send(embed=embed)

    @commands.command(aliases=['dis', 'Diss'], help="The specified member gets dissed")
    async def disthem(self, ctx, user:discord.Member=""):
        if user == "":
            user = self.client.get_user(ctx.author.id)
        response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        fox = response.json()
        foxupdate = (fox["insult"]) 
        
        embed = discord.Embed(description=f"{user.mention} {foxupdate}", colour=xz)
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['Chuck_norris', 'Chucky', 'norris'], help="Sends a random chuck norris joke/fact")
    async def chuck(self, ctx, user:discord.Member=""):
        if user == "":
            user = self.client.get_user(ctx.author.id)
        response = requests.get('https://api.chucknorris.io/jokes/random')
        fox = response.json()
        foxupdate = (fox["value"]) 
        
        embed = discord.Embed(description=f"{foxupdate}", colour=xz)
    
        await ctx.send(embed=embed)
    @commands.command(aliases=['adj', 'random_adj','randadj', 'Rand_Adj', 'random_adjective'], help="Sends a random adjective")
    async def adjective(self, ctx):
        
        response = requests.get('https://raw.githubusercontent.com/dariusk/corpora/master/data/words/adjs.json')
        fox = response.json()
        foxupdate = (fox["adjs"]) 
    
        embed = discord.Embed(title=f"{foxupdate[randint(1, 950)]}", colour=xz)
        
        await ctx.send(embed=embed)
    @commands.command(aliases=['smck', 'slap', 'BitchSlap', 'Hit', 'Spank'], help="The specified member gets slapped - Sends a random giffy")
    async def smack(self, ctx, user:discord.Member=""):
        if user == "":
            user = self.client.get_user(ctx.author.id)
        
        url = ['https://media.giphy.com/media/l5JdQaCUXTGy7AIGHq/giphy.gif','https://media.giphy.com/media/11N2zX8Swp3csg/giphy.gif', 'https://media.giphy.com/media/xUA7b9Wc1uaT52QfO8/giphy.gif', 'https://media.giphy.com/media/3oEduOWVxygmeDIKPu/giphy.gif', 'https://media.giphy.com/media/Qumf2QovTD4QxHPjy5/giphy.gif', 'https://media.giphy.com/media/uqSU9IEYEKAbS/giphy.gif', 'https://media.giphy.com/media/lX03hULhgCYQ8/giphy.gif', 'https://media.giphy.com/media/mEtSQlxqBtWWA/giphy.gif', 'https://media.giphy.com/media/gSIz6gGLhguOY/giphy.gif', 'https://media.giphy.com/media/uG3lKkAuh53wc/giphy.gif', 'https://media.giphy.com/media/P1EomtpqQW34c/giphy.gif', 'https://media.giphy.com/media/vxvNnIYFcYqEE/giphy.gif', '']
        
        embed = discord.Embed(description=f"{user.mention} got smacked", colour=xz)
        embed.set_image(url=choice(url))
        await ctx.send(embed=embed)
    @commands.command(aliases=['jokes'], help="Sends a random joke")
    async def joke(self, ctx):
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        fox = response.json()
        foxupdate = (fox["setup"]) 
        foxupdatey = (fox["punchline"])
        embed = discord.Embed(title="Joke", description=f"{foxupdate} ... {foxupdatey}", colour=xz)
        await ctx.send(embed=embed)
def setup(client):
  client.add_cog(JesterJokes(client))

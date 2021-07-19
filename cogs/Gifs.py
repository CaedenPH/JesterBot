import discord, os, requests, json, asyncio
from discord.ext import commands 
import randfacts
from random import choice, randint
import vacefron
import asyncpraw
from dutils import thecolor, Json, thebed

vace_api = vacefron.Client()


class JesterJokes(commands.Cog):
    def __init__(self, client):

        self.client = client

    @commands.command(aliases=['ranfact', 'rf', 'randomfact'], description="""Returns a random fact [ranfact, rf]""")
    async def fact(self, ctx):
        

        fact = randfacts.getFact()
        embed=discord.Embed(color=thecolor())
        embed.add_field(name="Random Fact", value=fact)
        await ctx.send(embed=embed)

    
    @commands.command(description="""Returns a random quote""")
    async def quote(self, ctx):
        
        response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
        embed=discord.Embed(color=thecolor())
        embed.add_field(name="Quote", value='*"{quoteText}"*\n ---  {quoteAuthor} --- '.format(**json.loads(response.text)))
        await ctx.send(embed=embed)
   
    @commands.command(description="""Returns a random quote""")
    async def quote1(self, ctx):
        
        response = requests.get('https://zenquotes.io/api/quotes/[your_key]')
        fox = response.json()
        embed=discord.Embed(color=thecolor())
        embed.add_field(name="Quote", value=f"{fox[1]['q']}")
        await ctx.send(embed=embed)
   
    @commands.command(description="""Returns a random Pickup Line.""")
    async def redit(self, ctx, *, redt):
        async with ctx.typing():
            subreddit = await reddit.subreddit(redt)
            pickupline = await subreddit.random()
            

            if pickupline.title:
                if pickupline.selftext:
                    embed = discord.Embed(title=pickupline.title, description=pickupline.selftext ,color=thecolor())
                else:
                    embed = discord.Embed(title=pickupline.title, description=pickupline.selftext, color=thecolor())
            if pickupline.selftext:
                embed = discord.Embed(title=pickupline.selftext, color=thecolor())
            embed.set_author(name=redt)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pl', 'pickup', 'pickline'], description="""Returns a random Pickup Line.""")
    async def pickup_line(self, ctx):
        async with ctx.typing():
            subreddit = await reddit.subreddit("pickuplines")
            pickupline = await subreddit.random()

            embed = discord.Embed(color=thecolor())
            embed.add_field(name=pickupline.title, value=pickupline.selftext)
        await ctx.send(embed=embed)

    @commands.command(aliases=['insultme', 'Mean', 'Insult_Me'], description="The specified member gets insulted")
    async def insult(self, ctx, user:discord.Member=""):
        
        
        m = self.client.get_user(828363172717133874)
        if user == "":
            user = self.client.get_user(ctx.author.id)
        
        if user == m:
            embed = discord.Embed(colour=thecolor())
            user = self.client.get_user(ctx.author.id)
            embed = discord.Embed(title="You shmuck...I am god")
            await ctx.send(embed=embed)
        else:

            response = requests.get('https://insult.mattbas.org/api/insult.json')
            fox = response.json()
            foxupdate = (fox["insult"]) 
            embed = discord.Embed(description=f"{user.mention} {foxupdate}", colour=thecolor())
            
            
            await ctx.send(embed=embed)

    @commands.command(aliases=['dis', 'Diss'], description="The specified member gets dissed")
    async def disthem(self, ctx, user:discord.Member=""):
        if user == "":
            user = self.client.get_user(ctx.author.id)
        response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        fox = response.json()
        foxupdate = (fox["insult"]) 
        
        embed = discord.Embed(description=f"{user.mention} {foxupdate}", colour=thecolor())
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['Chuck_norris', 'Chucky', 'norris'], description="Sends a random chuck norris joke/fact")
    async def chuck(self, ctx, user:discord.Member=""):
        if user == "":
            user = self.client.get_user(ctx.author.id)
        response = requests.get('https://api.chucknorris.io/jokes/random')
        fox = response.json()
        foxupdate = (fox["value"]) 
        
        embed = discord.Embed(description=f"{foxupdate}", colour=thecolor())
    
        await ctx.send(embed=embed)

    @commands.command(aliases=['adj', 'random_adj','randadj', 'Rand_Adj', 'random_adjective'], description="Sends a random adjective")
    async def adjective(self, ctx):
        
        response = requests.get('https://raw.githubusercontent.com/dariusk/corpora/master/data/words/adjs.json')
        fox = response.json()
        foxupdate = (fox["adjs"]) 
    
        embed = discord.Embed(title=f"{foxupdate[randint(1, 950)]}", colour=thecolor())
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['smck', 'slap', 'BitchSlap', 'Hit', 'Spank'], description="The specified member gets slapped - Sends a random giffy")
    async def smack(self, ctx, user:discord.Member=""):
        if user == "":
            user = self.client.get_user(ctx.author.id)
        
        url = ['https://media.giphy.com/media/l5JdQaCUXTGy7AIGHq/giphy.gif','https://media.giphy.com/media/11N2zX8Swp3csg/giphy.gif', 'https://media.giphy.com/media/xUA7b9Wc1uaT52QfO8/giphy.gif', 'https://media.giphy.com/media/3oEduOWVxygmeDIKPu/giphy.gif', 'https://media.giphy.com/media/Qumf2QovTD4QxHPjy5/giphy.gif', 'https://media.giphy.com/media/uqSU9IEYEKAbS/giphy.gif', 'https://media.giphy.com/media/lX03hULhgCYQ8/giphy.gif', 'https://media.giphy.com/media/mEtSQlxqBtWWA/giphy.gif', 'https://media.giphy.com/media/gSIz6gGLhguOY/giphy.gif', 'https://media.giphy.com/media/uG3lKkAuh53wc/giphy.gif', 'https://media.giphy.com/media/P1EomtpqQW34c/giphy.gif', 'https://media.giphy.com/media/vxvNnIYFcYqEE/giphy.gif', '']
        
        embed = discord.Embed(description=f"{user.mention} got smacked", colour=thecolor())
        embed.set_image(url=choice(url))
        await ctx.send(embed=embed)

    @commands.command(aliases=['jokes'], description="Sends a random joke")
    async def joke(self, ctx):
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        fox = response.json()
        foxupdate = (fox["setup"]) 
        foxupdatey = (fox["punchline"])
        embed = discord.Embed(title="Joke", description=f"{foxupdate} ... {foxupdatey}", colour=thecolor())
        await ctx.send(embed=embed)
        
def setup(client):
  client.add_cog(JesterJokes(client))

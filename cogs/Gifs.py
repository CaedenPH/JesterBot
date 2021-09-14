import discord, os, requests, json, asyncio
from discord.ext import commands 
from random import choice, randint

from core.utils.utils import thecolor, Json, thebed
from core.utils.comedy import fact, quote, joke, pickup
from core.Context import Context
from core.utils.comedy import joke


class JesterJokes(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command(aliases=['ranfact', 'rf', 'randomfact'], description="""Returns a random fact [ranfact, rf]""")
    async def fact(self, ctx:Context):
        
        embed = fact()
        await ctx.send(embed=embed)

    
    @commands.command(description="""Returns a random quote""")
    async def quote(self, ctx:Context):
        
        embed = quote()
        await ctx.send(embed=embed)
   
    @commands.command(description="""Returns a random quote""")
    async def quote1(self, ctx:Context):
        
        response = requests.get('https://zenquotes.io/api/quotes/[your_key]')
        fox = response.json()
        embed=discord.Embed(color=thecolor())
        embed.add_field(name="Quote", value=f"{fox[1]['q']}")
        await ctx.send(embed=embed)
   

    @commands.command(aliases=['pl', 'pickup', 'pickline'], description="""Returns a random Pickup Line.""")
    async def pickup_line(self, ctx:Context):
        
        embed = await pickup()
        await ctx.send(embed=embed)

    @commands.command(aliases=['insultme', 'Mean', 'Insult_Me'], description="The specified member gets insulted")
    async def insult(self, ctx:Context, user:discord.Member=""):
        
        
        m = self.bot.get_user(828363172717133874)
        if user == "":
            user = self.bot.get_user(ctx.author.id)
        
        if user == m:
            embed = discord.Embed(colour=thecolor())
            user = self.bot.get_user(ctx.author.id)
            embed = discord.Embed(title="You shmuck...I am god")
            await ctx.send(embed=embed)
        else:

            response = requests.get('https://insult.mattbas.org/api/insult.json')
            fox = response.json()
            foxupdate = (fox["insult"]) 
            embed = discord.Embed(description=f"{user.mention} {foxupdate}", colour=thecolor())
            
            
            await ctx.send(embed=embed)

    @commands.command(aliases=['dis', 'Diss'], description="The specified member gets dissed")
    async def disthem(self, ctx:Context, user:discord.Member=""):
        if user == "":
            user = self.bot.get_user(ctx.author.id)
        response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        fox = response.json()
        foxupdate = (fox["insult"]) 
        
        embed = discord.Embed(description=f"{user.mention} {foxupdate}", colour=thecolor())
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['Chuck_norris', 'Chucky', 'norris'], description="Sends a random chuck norris joke/fact")
    async def chuck(self, ctx:Context, user:discord.Member=""):
        if user == "":
            user = self.bot.get_user(ctx.author.id)
        response = requests.get('https://api.chucknorris.io/jokes/random')
        fox = response.json()
        foxupdate = (fox["value"]) 
        
        embed = discord.Embed(description=f"{foxupdate}", colour=thecolor())
    
        await ctx.send(embed=embed)

    @commands.command(aliases=['adj', 'random_adj','randadj', 'Rand_Adj', 'random_adjective'], description="Sends a random adjective")
    async def adjective(self, ctx:Context):
        
        response = requests.get('https://raw.githubusercontent.com/dariusk/corpora/master/data/words/adjs.json')
        fox = response.json()
        foxupdate = (fox["adjs"]) 
    
        embed = discord.Embed(title=f"{foxupdate[randint(1, 950)]}", colour=thecolor())
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['smck', 'slap', 'BitchSlap', 'Hit', 'Spank'], description="The specified member gets slapped - Sends a random giffy")
    async def smack(self, ctx:Context, user:discord.Member=""):
        if user == "":
            user = self.bot.get_user(ctx.author.id)
        
        url = ['https://media.giphy.com/media/l5JdQaCUXTGy7AIGHq/giphy.gif','https://media.giphy.com/media/11N2zX8Swp3csg/giphy.gif', 'https://media.giphy.com/media/xUA7b9Wc1uaT52QfO8/giphy.gif', 'https://media.giphy.com/media/3oEduOWVxygmeDIKPu/giphy.gif', 'https://media.giphy.com/media/Qumf2QovTD4QxHPjy5/giphy.gif', 'https://media.giphy.com/media/uqSU9IEYEKAbS/giphy.gif', 'https://media.giphy.com/media/lX03hULhgCYQ8/giphy.gif', 'https://media.giphy.com/media/mEtSQlxqBtWWA/giphy.gif', 'https://media.giphy.com/media/gSIz6gGLhguOY/giphy.gif', 'https://media.giphy.com/media/uG3lKkAuh53wc/giphy.gif', 'https://media.giphy.com/media/P1EomtpqQW34c/giphy.gif', 'https://media.giphy.com/media/vxvNnIYFcYqEE/giphy.gif', '']
        
        embed = discord.Embed(description=f"{user.mention} got smacked", colour=thecolor())
        embed.set_image(url=choice(url))
        await ctx.send(embed=embed)

    @commands.command(aliases=['jokes', 'joke'], description="Sends a random joke")
    async def _joke(self, ctx:Context):
        
        await thebed(ctx, 'Joke', await joke())

def setup(bot):
  bot.add_cog(JesterJokes(bot))

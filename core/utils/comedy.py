import vacefron, randfacts, asyncpraw, datetime, json, requests
import discord

from .utils import thecolor

vace_api = vacefron.Client()

def fact():
    fact = randfacts.get_fact()
    embed=discord.Embed(color=thecolor())
    embed.add_field(name="Fact", value=fact)
    return embed

def quote():
        
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
    embed=discord.Embed(color=thecolor())
    embed.add_field(name="Quote", value='*"{quoteText}"*\n{quoteAuthor}'.format(**json.loads(response.text)))
    return embed

def joke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    fox = response.json()
    foxupdate = (fox["setup"]) 
    foxupdatey = (fox["punchline"])
    embed = discord.Embed(title="Joke", description=f"{foxupdate} ... {foxupdatey}", colour=thecolor())
    return embed

async def pickup():
    subreddit = await reddit.subreddit("pickuplines") 
    pickupline = await subreddit.random()

    embed = discord.Embed(color=thecolor())
    embed.add_field(name=pickupline.title, value=pickupline.selftext)
    return embed
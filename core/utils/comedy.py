import vacefron, randfacts, asyncpraw, datetime, json, requests
import disnake
from jokeapi import Jokes

from .utils import thecolor
from core.utils.HIDDEN import *

reddit = asyncpraw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=user_agent,
)
vace_api = vacefron.Client()


def fact():
    fact = randfacts.get_fact()
    embed = disnake.Embed(color=thecolor())
    embed.add_field(name="Fact", value=fact)
    return embed


def quote():

    response = requests.get(
        "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
    )
    embed = disnake.Embed(color=thecolor())
    embed.add_field(
        name="Quote",
        value='*"{quoteText}"*\n{quoteAuthor}'.format(**json.loads(response.text)),
    )
    return embed


async def joke():
    j = await Jokes()
    joke = await j.get_joke()
    if joke["type"] == "single":
        return joke["joke"]
    return f"**{joke['setup']}** - {joke['delivery']}"


async def pickup():
    subreddit = await reddit.subreddit("pickuplines")
    pickupline = await subreddit.random()

    embed = disnake.Embed(color=thecolor())
    embed.add_field(name=pickupline.title, value=pickupline.selftext)
    return embed

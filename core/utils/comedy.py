import vacefron
import randfacts
import asyncpraw
import json
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


def fact() -> disnake.Embed:
    fact = randfacts.get_fact()

    embed = disnake.Embed(color=thecolor())
    embed.add_field(name="Fact", value=fact)
    return embed


async def quote(bot) -> disnake.Embed:
    async with bot.client.get(
        url="http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
    ) as response:
        embed = disnake.Embed(color=thecolor())
        embed.add_field(
            name="Quote",
            value='*"{quoteText}"*\n{quoteAuthor}'.format(
                **json.loads(await response.read())
            ),
        )
        return embed


async def joke() -> str:
    j = await Jokes()
    joke = await j.get_joke()

    if joke["type"] == "single":
        return joke["joke"]
    return f"**{joke['setup']}** - {joke['delivery']}"


async def pickup(bot) -> disnake.Embed:
    async with bot.client.get(
        url="http://getpickuplines.herokuapp.com/lines/random"
    ) as response:
        json = await response.json()

    embed = disnake.Embed(color=thecolor())
    embed.add_field(name="Pickup line", value=json["line"])
    return embed

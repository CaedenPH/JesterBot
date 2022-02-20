import re
import randfacts
import json
import disnake

from jokeapi import Jokes
from .utils import get_colour


async def fact() -> str:
    return randfacts.get_fact()


async def quote(bot) -> str:
    async with bot.client.get(url="http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en") as response:
        return '*"{quoteText}"*\n{quoteAuthor}'.format(**json.loads(await response.read()))


async def joke() -> str:
    j = await Jokes()
    joke = await j.get_joke()

    if joke["type"] == "single":
        return joke["joke"]
    return f"**{joke['setup']}** - {joke['delivery']}"


async def pickup(bot) -> str:
    async with bot.client.get(url="http://getpickuplines.herokuapp.com/lines/random") as response:
        json = await response.json()
    return json["line"]

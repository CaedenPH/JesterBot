import json
from discord.ext import commands

def get_prefix(bot, message):

    try:
        with open("./dicts/prefixes.json") as fin:
            prefixes = json.load(fin)
        pref = ''
        if str(message.guild.id) in prefixes:

            if str(message.author.id) in prefixes:

                pref = prefixes[str(message.author.id)]['prefix']
            else:
                pref = prefixes[str(message.guild.id)]['prefix']
        else:
            if str(message.author.id) in prefixes:

                pref = prefixes[str(message.author.id)]['prefix']
            else:
                pref = ['j.']
    except:
        if str(message.author.id) in prefixes:

            pref = prefixes[str(message.author.id)]['prefix']
        else:
            pref = ['j.']

    return commands.when_mentioned_or(*pref)(bot, message)

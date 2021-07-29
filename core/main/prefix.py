import json
def get_prefix(bot, message):
    try:
        with open("./dicts/prefixes.json") as fin:
            prefixes = json.load(fin)
    
        if str(message.guild.id) in prefixes:

            if str(message.author.id) in prefixes:

                return prefixes[str(message.author.id)]['prefix']
            else:
                return prefixes[str(message.guild.id)]['prefix']
        else:
            if str(message.author.id) in prefixes:

                return prefixes[str(message.author.id)]['prefix']
            else:
                return ["j."]
    except:
        if str(message.author.id) in prefixes:

            return prefixes[str(message.author.id)]['prefix']
        else:
            return ["j."]
import discord
from discord.ext import commands

#import InfixParser
import json
import io
import textwrap
import contextlib
from traceback import format_exception

from core.utils.utils import Json, thecolor
from core.Paginator import Paginator 

def clean_code(content:str):
    content = content.strip('`')
    return content


async def run_eval(ctx, code, **kwargs):
    _eval = kwargs.get('_eval')

    local_variables = {
        "discord": discord,
        "commands": commands, 
        "bot": ctx.bot, 
        "client": ctx.bot,
        "ctx": ctx, 
        "channel": ctx.channel, 
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message

    }

    if code == "reset":

        with open('./dicts/Num.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                data[str(ctx.author.id)]['Score'] = 0
                z = data[str(ctx.author.id)]['Score']
            else:
                data[str(ctx.author.id)] = {
                    "Name": ctx.author.name,
                    "Score": 0

                }
            Json(k, data)
            return await ctx.send('reset')
    else:

        with open('./dicts/Num.json', 'r+') as k:
            data = json.load(k)
            if str(ctx.author.id) in data:
                data[str(ctx.author.id)]['Score'] += 1
                z = data[str(ctx.author.id)]['Score']
            else:
                data[str(ctx.author.id)] = {
                    "Name": ctx.author.name,
                    "Score": 1

                }
            Json(k, data)
    
    code = clean_code(code)
        
    stdout = io.StringIO()

    pref = await ctx.bot.get_prefix(ctx.message)
    message = ctx.message.content.strip(pref[0])[2:]

    if _eval == 'dir':
        code = f"print(dir({code}))"
        message = message[1:]
            
    elif _eval == 'return':
        code = f"return {code}"
        message = message[1:]
        
    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}",  local_variables, 
            )
            obj = await local_variables["func"]()
        
            result = f"{stdout.getvalue()}{obj}\n"
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))
        pass

    theresult = result.split('None')


    if len(result) < 2000:
        msg = f"```py\nIn[{z}]: {message}\nOut[{z}]: {theresult[0]}\n```"
    else:
        y = Paginator(ctx)
        return await y.paginate(content=theresult[0], name='Eval')

    return msg
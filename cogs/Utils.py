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
import randfacts
import io
import textwrap
import contextlib
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from random import choice, randint
from bs4 import BeautifulSoup
from animals import Animals
from traceback import format_exception
from pyMorseTranslator import translator
from discord.ext.buttons import Paginator   
import pytz
import datetime
from datetime import datetime
#from dutils import color, Json, embed1, GetUser

class Pag(Paginator):
    async def teardown(self):
        try:
            
            await self.page.clear_reactions()
            
        except discord.HTTPException:
            pass

encoder = translator.Encoder()
decoder = translator.Decoder()


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

    
class Utils(commands.Cog):
    def __init__(self, client):
   
        self.client = client
    
    @commands.command(aliases=['evalcalc', 'calc'], description='run code')
    async def calculator(self, ctx, *, code):
     
        z = 0
 

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
                await ctx.send('reset')
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
            x = False
            def clean_code(content):
                if content.startswith("```") and content.endswith("```"):
                    return "\n".join(content.split("\n")[1:][:-3])
                else:
                    return content
            if ctx.author.id != 298043305927639041:
                for item in ('import', 'file', 'range', 'print', 'delete', 'truncate', 'open'):
                       
                    if item in code:
                        x = True 
                        
            if x:
                embed = discord.Embed(title="This is a calculator!", colour=xz)
                embed.set_image(url="https://cdn.discordapp.com/attachments/836812307971571762/846334605669826600/unknown.png")
                return await ctx.send(embed=embed)
            code = clean_code(code)
            
            if ctx.author.id == 298043305927639041:

                local_variables = {
                    "discord": discord,
                    "commands": commands, 
                    "bot": self.client, 
                    "client": self.client,
                    "ctx": ctx, 
                    "channel": ctx.channel, 
                    "author": ctx.author,
                    "guild": ctx.guild,
                    "message": ctx.message

                }
            else:
                 local_variables = {
                    "discord": discord,
                    "commands": commands, 
                    "ctx": ctx, 
                    "channel": ctx.channel, 
                    "author": ctx.author,
                    "guild": ctx.guild,
                    "message": ctx.message

                }

    
            

            stdout = io.StringIO()
            
            if ctx.message.content[6:].startswith('run'):
                if ctx.message.content[5::].startswith('print'):
                
                    code = f"return {ctx.message.content[11::][:-1]}"
                
                    pass
                elif ctx.message.content[5::].startswith('return'):
                    pass
                else:
                    code = f"return {code}"

            else:

                if ctx.message.content[6::].startswith('print'):
                    
                    code = f"return {ctx.message.content[12::][:-1]}"
                    
                    pass
                elif ctx.message.content[6::].startswith('return'):
                    pass
                else:
                    code = f"return {code}"
              

            
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
            if ctx.message.content[1:].startswith('run'):
                y = ctx.message.content[5::]
             
            else:
                y = ctx.message.content[6::]
            
            new_result = result.split(', ')
            # await ctx.send(new_result)
            my_list = []
            for key in new_result:
                
                my_list.append(f"'{key[1:][:-1]}")
   

           
            if len(result) < 2000:
                 await ctx.send(f"```py\nIn[{z}]: {y}\nOut[{z}]: {result}\n```")
            else:
                pager = Pag(
                    timeout=100,
                    #entries=[f"`{result[1:][:-1]}`"[i: i + 2000] for i in range(0, len(result), 2000)],
                    entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
                    length = 1,
                    prefix = "```py\n", 
                    suffix = "```",
                    colour=xz
                    )


                await pager.start(ctx) 
    @commands.command(aliases=['stock', 'market'], help="Sends information about the stocks specified") 
    async def stocks(self, ctx, stock:str=""):
        async with ctx.typing():

            if stock == "":
                embed = discord.Embed(title="Type the stock symbol (e.g AAPL = apple)", description="[Stocks](https://swingtradebot.com/equities)", colour=xz)
                
           
            else:
                
                tickerSymbol = stock
                tickerData = yf.Ticker(tickerSymbol)
            
                
                if 'longName' in tickerData.info:

                    embed = discord.Embed(title=f"{tickerData.info['longName']}", colour=xz)
                    embed.set_author(icon_url=ctx.author.avatar_url, name="Stock market")
                    
                    if 'fullTimeEmployees' in tickerData.info: 
                        embed.add_field(name="Employees", value=f"{tickerData.info['fullTimeEmployees']}", inline=False)
                    
                        if 'country' in tickerData.info:
                            embed.add_field(name="Value", value=f"Market Cap: *${tickerData.info['marketCap']}*\nLow: *${tickerData.info['fiftyTwoWeekLow']}*\nHigh: *${tickerData.info['fiftyTwoWeekHigh']}*", inline=False)
                            embed.add_field(name="Location", value=f"{tickerData.info['country']}, {tickerData.info['state']}, {tickerData.info['city']}", inline=False)
                            embed.add_field(name="Shares", value=f"{tickerData.info['sharesShort']}", inline=False)
                            embed.set_thumbnail(url=tickerData.info['logo_url'])
                   
                        else:
                            embed = discord.Embed(title=f"{stock} doesn't have enough info!", colour=xz)
                       


                    else:
                        if 'country' in tickerData.info:
                            embed.add_field(name="Value", value=f"Market Cap: *${tickerData.info['marketCap']}*\nLow: *${tickerData.info['fiftyTwoWeekLow']}*\nHigh: *${tickerData.info['fiftyTwoWeekHigh']}*", inline=False)
                            embed.add_field(name="Location", value=f"{tickerData.info['country']}, {tickerData.info['state']}, {tickerData.info['city']}", inline=False)
                            embed.add_field(name="Shares", value=f"{tickerData.info['sharesShort']}", inline=False)
                            
                            
                        else:
                            embed = discord.Embed(title=f"{stock} doesn't have enough info!", colour=xz)
                            
                            
                else:
                    embed = discord.Embed(title=f"{stock} couldn't be found!", colour=xz)
        await ctx.send(embed=embed)
    @commands.command(aliases=['fib'], help="Sends the numbers of the fibinaci upto the number provided")
    async def fibinaci(self, ctx, upto=10000000000000):
        x = []
        
        if upto > 10000000000:
            upto = 1000000000
        else:

            def fib(n):
                # if x in []:
                #     pass
                # else:

                a,b = 0, 1
                while a < n:
                    x.append(str(a))
                    
                    a, b = b, a+b

            fib(upto)
        
            embed = discord.Embed(title="Fibinaci", description=f"**{', '.join(x)}**", colour=xz)
            await ctx.send(embed=embed)
    @commands.command(aliases=['av', 'avatars'], help="Sends the mentioned users avatar or if none is specified, the usrs avatar")
    async def avatar(self, ctx, user:discord.Member = ""):
        if user == "":
            user = ctx.author.id
            username = self.client.get_user(user)
            embed = discord.Embed(title=f"Avatar", colour=xz)
            embed.set_author(name=username.name, icon_url=username.avatar_url)
            embed.set_image(url=username.avatar_url)
            await ctx.send(embed=embed)
        
        else:

            username = self.client.get_user(user.id)
            embed = discord.Embed(title=f"Avatar", colour=xz)
            embed.set_author(name=username.name, icon_url=username.avatar_url)
            embed.set_image(url=username.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['tz', 'time', 'zone'], help="Sends the current time of the [origin]. To get all of the places recognisable, leave `origin` blank")
    async def timezone(self, ctx, origin=None):
        try:


            if not origin:
                var = ""
                num = 0
                result = pytz.all_timezones
                for key in result:
                    num += 1
                    if num == len(result):

                        var += f"{result}"
                    else:
                        
                        var += f"{result}, "

                pager = Pag(
                    timeout=100,
                    #entries=[f"`{result[1:][:-1]}`"[i: i + 2000] for i in range(0, len(result), 2000)],
                    entries=[var[i: i + 2000] for i in range(0, len(var), 2000)],
                    length = 1,
                    prefix = "```py\n", 
                    suffix = "```",
                    colour=xz
                    )


                return await pager.start(ctx) 
            tz_NY = pytz.timezone(origin) 
            now = datetime.now(tz_NY)
            x = str(now)
            _date = x[:10]
            _time = x[11:19]         
            embed = discord.Embed(title=f"**Time:** {_time} │ **Date:** {_date}", colour=xz)  
            embed.set_author(name="Datetime", icon_url=ctx.author.avatar_url)
            
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"**TimeZoneError: {e}**", colour=xz)
            await ctx.send(embed=embed)

        
    @commands.command()
    async def pager(self, ctx, *, args):
        pager = Pag(
            timeout = 100,
            entries = [args],
            length = 1


        )
        await pager.start(ctx)
    @commands.command(aliases=['bin'])
    async def binary(self, ctx, text):
        a_string = text
        a_byte_array = bytearray(a_string, "utf8")
        byte_list = []
        for byte in a_byte_array:
            binary_representation = bin(byte)
            byte_list. append(binary_representation) 
        await ctx.send(", ".join(byte_list))
    
    @commands.command(help="""ASCII was developed from telegraph code. Work on the ASCII standard began in May 1961. The first edition of the standard was published in 1963. Compared to earlier telegraph codes, the proposed Bell code and ASCII were both ordered for more convenient sorting (i.e., alphabetization) of lists.

The use of ASCII format for Network Interchange was described in 1969. That document was formally elevated to an Internet Standard in 2015.

Originally based on the English alphabet, ASCII encodes 128 specified characters into seven-bit integers as shown by the ASCII chart above. Ninety-five of the encoded characters are printable: these include the digits 0 to 9, lowercase letters a to z, uppercase letters A to Z, and punctuation symbols. 

For example, lowercase i would be represented in the ASCII encoding by binary 1101001 = hexadecimal 69 (i is the ninth letter) = decimal 105.
To get the ascii table type ^ascii

Source: [Website](https://en.wikipedia.org/wiki/ASCII)
    """)
    async def ascii(self, ctx, *, text=None):
        x = []
        p = []
        num = 0
        if not text:
            
            for i in range(1, 256):
                num += 1
                if num <= 32:
                    pass
                else:


                    x.append(f"{chr(i)}")
            embed = discord.Embed(title="Ascii:", description="\n*starting from 32 because characters prior to that number are not used, therefore sending blanks* \n" + f'```py\n{", ".join(x)}```', colour=xz)
            embed.set_footer(text="Type ^help ascii to get information about what the ascii table is. | `,` signifies a new character.")
            return await ctx.send(embed=embed)
                        
        
       
        z = text.split(' ')
        for c in z:
            
            for t in c:
                p.append(str(ord(t)))
               
            x.append(f"\n`{c}: {'-'.join(p)}`")
            p = []
        embed = discord.Embed(title="Ascii:", description=", ".join(x), colour=xz)
        embed.set_footer(text="Type ^help ascii to get information about what the ascii table is. | '-' signifies a new character.")
        await ctx.send(embed=embed)
        

    @commands.command(aliases=["morse_code", 'mcode'], help="""Encode or decode text/morse code into morse code/plain text, type .morse for help""")
    async def morse(self, ctx):
        
        
        
        embed = discord.Embed(description="Type ^encode <text> to encode some text")

        
    @commands.command(help="""Encode some plain text into Morse code""")
    async def encode(self, ctx, *, text):
        
        
        embed = discord.Embed(title=f"Morse [Coded]: ", description=f"```bash\n{encoder.encode(text).morse}```", colour=xz)
        embed.set_footer(text=str(ctx.author) + " | Morse from Text [Encoded] ", icon_url=ctx.author.avatar_url)
        
        #embed.add_field(name="Input: ", value=f'```py\n"{text}"\n```', inline=False)
        #embed.add_field(name="Output:  ", value=f"```\n{encoder.encode(text).morse}\n```")
        
        await ctx.send(embed=embed)


    @commands.command(aliases=['eval2'], description='run code')
    async def evaldir(self, ctx, *, code):
        x = False
        item1 = ('import', 'file', 'truncate', 'remove', 'delete', 'open', 'input')
        if ctx.author.id != 298043305927639041:
        
            for item in ('import', 'file', 'truncate', 'remove', 'delete', 'open', 'input'):
                
                if item in code:
                    x = True    
        if x:
            return await ctx.send(item1)
        z = 0
 

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
                await ctx.send('reset')
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

            
            def clean_code(content):
                if content.startswith("```") and content.endswith("```"):
                    return "\n".join(content.split("\n")[1:][:-3])
                else:
                    return content
            
        
        code = clean_code(code)
        
        if ctx.author.id == 298043305927639041:

            local_variables = {
                "discord": discord,
                "commands": commands, 
                "bot": self.client, 
                "client": self.client,
                "ctx": ctx, 
                "channel": ctx.channel, 
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message,
                "datetime": datetime

            }
        else:
                local_variables = {
                "discord": discord,
                "commands": commands, 
                "ctx": ctx, 
                "channel": ctx.channel, 
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message

            }
        
        code = f"return dir({code})"
        stdout = io.StringIO()
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
        if ctx.message.content[1:].startswith('run'):
            y = ctx.message.content[5::]
            
        else:
            y = ctx.message.content[6::]
        
        new_result = result.split(', ')
        # await ctx.send(new_result)
        my_list = []
        for key in new_result:
            
            my_list.append(f"'{key[1:][:-1]}")


        
        if len(result) < 2000:
                await ctx.send(f"```py\nIn[{z}]: {y}\nOut[{z}]: {result}\n```")
        else:
            pager = Pag(
                timeout=100,
                #entries=[f"`{result[1:][:-1]}`"[i: i + 2000] for i in range(0, len(result), 2000)],
                entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
                length = 1,
                prefix = "```py\n", 
                suffix = "```",
                colour=xz
                )


            await pager.start(ctx) 
    @commands.command(aliases=['eval1'], description='run code')
    async def evalreturn(self, ctx, *, code):
        x = False
        item1 = ('import', 'file', 'truncate', 'remove', 'delete', 'open', 'input')
        if ctx.author.id != 298043305927639041:
        
            for item in ('import', 'file', 'truncate', 'remove', 'delete', 'open', 'input'):
                
                if item in code:
                    x = True    
        if x:
            return await ctx.send(item1)
        z = 0
 

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
                await ctx.send('reset')
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
            x = False
            def clean_code(content):
                if content.startswith("```") and content.endswith("```"):
                    
                    return code.strip('```')
                else:
                    return content
                
            code = clean_code(code)
            
            if ctx.author.id == 298043305927639041:

                local_variables = {
                    "discord": discord,
                    "commands": commands, 
                    "bot": self.client, 
                    "client": self.client,
                    "ctx": ctx, 
                    "channel": ctx.channel, 
                    "author": ctx.author,
                    "guild": ctx.guild,
                    "message": ctx.message

                }
            else:
                 local_variables = {
                    "discord": discord,
                    "commands": commands, 
                    "ctx": ctx, 
                    "channel": ctx.channel, 
                    "author": ctx.author,
                    "guild": ctx.guild,
                    "message": ctx.message

                }

    
            

            stdout = io.StringIO()
            
            if ctx.message.content[6:].startswith('run'):
                if ctx.message.content[5::].startswith('print'):
                
                    code = f"return {ctx.message.content[11::][:-1]}"
                
                    pass
                elif ctx.message.content[5::].startswith('return'):
                    pass
                else:
                    code = f"return {code}"

            else:

                if ctx.message.content[6::].startswith('print'):
                    
                    code = f"return {ctx.message.content[12::][:-1]}"
                    
                    pass
                elif ctx.message.content[6::].startswith('return'):
                    pass
                else:
                    code = f"return {code}"
              

            
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
            if ctx.message.content[1:].startswith('run'):
                y = ctx.message.content[5::]
             
            else:
                y = ctx.message.content[6::]
            
            new_result = result.split(', ')
            # await ctx.send(new_result)
            my_list = []
            for key in new_result:
                
                my_list.append(f"'{key[1:][:-1]}")
   

           
            if len(result) < 2000:
                 await ctx.send(f"```py\nIn[{z}]: {y}\nOut[{z}]: {result}\n```")
            else:
                pager = Pag(
                    timeout=100,
                    #entries=[f"`{result[1:][:-1]}`"[i: i + 2000] for i in range(0, len(result), 2000)],
                    entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
                    length = 1,
                    prefix = "```py\n", 
                    suffix = "```",
                    colour=xz
                    )


                await pager.start(ctx) 

    
    @commands.command(description='run code')
    async def eval(self, ctx, *, code):
        x = False
        item1 = ('import', 'file', 'truncate', 'remove', 'delete', 'open', 'input')
        if ctx.author.id != 298043305927639041:
        
            for item in ('import', 'file', 'truncate', 'remove', 'delete', 'open', 'input'):
                
                if item in code:
                    x = True    
        if x:
            return await ctx.send(item1)

        z = 0


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
                await ctx.send('reset')
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
    
       
        def clean_code(content):
            if content.startswith("```") and content.endswith("```"):
                
                return content.strip('```')
            else:
                return content
                
        
                

        
        

                    
        
        
        code = clean_code(code)
        
        if ctx.author.id == 298043305927639041:

            local_variables = {
                "discord": discord,
                "commands": commands, 
                "bot": self.client, 
                "client": self.client,
                "ctx": ctx, 
                "channel": ctx.channel, 
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message,
                "datetime": datetime

            }
        else:
                local_variables = {
                "discord": discord,
                "commands": commands, 
                "ctx": ctx, 
                "channel": ctx.channel, 
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message

            }
        
            
        stdout = io.StringIO()
            
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

    
        if ctx.message.content[1:].startswith('run'):
            y = ctx.message.content[5::]
        
        else:
            y = ctx.message.content[6::]
        
        new_result = result.split(', ')
        # await ctx.send(new_result)
        my_list = []
        for key in new_result:
            
            my_list.append(f"'{key[1:][:-1]}")

        ty = y.strip('```')
    
        if len(result) < 2000:
            await ctx.send(f"```py\nIn[{z}]: {ty}\nOut[{z}]: {theresult[0]}\n```")
        else:
            pager = Pag(
                timeout=100,
                #entries=[f"`{result[1:][:-1]}`"[i: i + 2000] for i in range(0, len(result), 2000)],
                entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
                length = 1,
                prefix = "```py\n", 
                suffix = "```",
                colour=xz
                )


            await pager.start(ctx)
    

def setup(client):
  client.add_cog(Utils(client))

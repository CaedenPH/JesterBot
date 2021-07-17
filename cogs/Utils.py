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
from dutils import thecolor, Json, thebed
from dpymenus import Page, PaginatedMenu
import simpleeval

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        
        return content.strip('```')
    else:
        return content
class Pag(Paginator):
    async def teardown(self):
        try:
            
            await self.page.clear_reactions()
            
        except discord.HTTPException:
            pass

encoder = translator.Encoder()
decoder = translator.Decoder()


class Utils(commands.Cog):
    def __init__(self, client):
   
        self.client = client
        
    @commands.command()
    async def calc(self, ctx, *, math=""):
        if not math:
            return await thebed(ctx, '', "**The current list of available eval operations**", i="https://cdn.discordapp.com/attachments/836812307971571762/846334605669826600/unknown.png")
       
        result = simpleeval.simple_eval(math)
        embed = discord.Embed(color=discord.Color.green())
        embed.set_footer(text=str(ctx.author) + " | Evaluation", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Your expression: ", value=f'```yaml\n"{math}"\n```', inline=False)
        embed.add_field(name="Result: ", value=f"```\n{result}\n```")
        await ctx.send(embed=embed)
    @commands.command(aliases=['stock', 'market'], description="Sends information about the stocks specified") 
    async def stocks(self, ctx, stock:str=""):
        async with ctx.typing():

            if stock == "":
                embed = discord.Embed(title="Type the stock symbol (e.g AAPL = apple)", description="[Stocks](https://swingtradebot.com/equities)", colour=thecolor())
                
           
            else:
                
                tickerSymbol = stock
                tickerData = yf.Ticker(tickerSymbol)
            
                
                if 'longName' in tickerData.info:

                    embed = discord.Embed(title=f"{tickerData.info['longName']}", colour=thecolor())
                    embed.set_author(icon_url=ctx.author.avatar_url, name="Stock market")
                    
                    if 'fullTimeEmployees' in tickerData.info: 
                        embed.add_field(name="Employees", value=f"{tickerData.info['fullTimeEmployees']}", inline=False)
                    
                        if 'country' in tickerData.info:
                            embed.add_field(name="Value", value=f"Market Cap: *${tickerData.info['marketCap']}*\nLow: *${tickerData.info['fiftyTwoWeekLow']}*\nHigh: *${tickerData.info['fiftyTwoWeekHigh']}*", inline=False)
                            embed.add_field(name="Location", value=f"{tickerData.info['country']}, {tickerData.info['state']}, {tickerData.info['city']}", inline=False)
                            embed.add_field(name="Shares", value=f"{tickerData.info['sharesShort']}", inline=False)
                            embed.set_thumbnail(url=tickerData.info['logo_url'])
                   
                        else:
                            embed = discord.Embed(title=f"{stock} doesn't have enough info!", colour=thecolor())
                       


                    else:
                        if 'country' in tickerData.info:
                            embed.add_field(name="Value", value=f"Market Cap: *${tickerData.info['marketCap']}*\nLow: *${tickerData.info['fiftyTwoWeekLow']}*\nHigh: *${tickerData.info['fiftyTwoWeekHigh']}*", inline=False)
                            embed.add_field(name="Location", value=f"{tickerData.info['country']}, {tickerData.info['state']}, {tickerData.info['city']}", inline=False)
                            embed.add_field(name="Shares", value=f"{tickerData.info['sharesShort']}", inline=False)
                            
                            
                        else:
                            embed = discord.Embed(title=f"{stock} doesn't have enough info!", colour=thecolor())
                            
                            
                else:
                    embed = discord.Embed(title=f"{stock} couldn't be found!", colour=thecolor())
        await ctx.send(embed=embed)
    @commands.command(aliases=['fib'], description="Sends the numbers of the fibinaci upto the number provided")
    async def fibonacci(self, ctx, upto=10000000000000):
        x = []
        
        if upto > 10000000000:
            upto = 1000000000
        

            
                # if x in []:
                #     pass
                # else:

        a,b = 0, 1
        while a < upto:
            x.append(str(a))
            
            a, b = b, a+b

        
    
        embed = discord.Embed(title="Fibinaci", description=f"{', '.join(x)}", colour=thecolor())
        await ctx.send(embed=embed)
    @commands.command(aliases=['av', 'avatars'], description="Sends the mentioned users avatar or if none is specified, the usrs avatar")
    async def avatar(self, ctx, user:discord.Member = ""):
        if user == "":
            user = ctx.author.id
            username = self.client.get_user(user)
            embed = discord.Embed(title=f"Avatar", colour=thecolor())
            embed.set_author(name=username.name, icon_url=username.avatar_url)
            embed.set_image(url=username.avatar_url)
            await ctx.send(embed=embed)
        
        else:

            username = self.client.get_user(user.id)
            embed = discord.Embed(title=f"Avatar", colour=thecolor())
            embed.set_author(name=username.name, icon_url=username.avatar_url)
            embed.set_image(url=username.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['tz', 'time', 'zone'], description="Sends the current time of the [origin]. To get all of the places recognisable, leave `origin` blank")
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
                    colour=thecolor()
                    )


                return await pager.start(ctx) 
            tz_NY = pytz.timezone(origin) 
            now = datetime.now(tz_NY)
            x = str(now)
            _date = x[:10]
            _time = x[11:19]         
            embed = discord.Embed(title=f"**Time:** {_time} │ **Date:** {_date}", colour=thecolor())  
            embed.set_author(name="Datetime", icon_url=ctx.author.avatar_url)
            
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error", description=f"**TimeZoneError: {e}**", colour=thecolor())
            await ctx.send(embed=embed)

        
    @commands.command(hidden=True)
    async def pager(self, ctx, *, args):
        pager = Pag(
            timeout = 100,
            entries = [args],
            length = 1


        )
        await pager.start(ctx)
    @commands.command(aliases=['bin'])
    async def binary(self, ctx, *, text):
       
        
        response = requests.get(f'https://some-random-api.ml/binary?text={text}')
        fox = response.json()
        embed=discord.Embed(color=thecolor())
        embed.add_field(name="Binary", value=f"{fox['binary']}")
        await ctx.send(embed=embed)
   

    @commands.command(aliases=['unbin'])
    async def unbinary(self, ctx, *, nums:str):
      
        
        response = requests.get(f'https://some-random-api.ml/binary?decode={nums}')
        fox = response.json()
        embed=discord.Embed(color=thecolor())
        embed.add_field(name="Decoded from binary", value=f"{fox['text']}") 
        await ctx.send(embed=embed)
   
    
    @commands.command(description="""ASCII was developed from telegraph code. Work on the ASCII standard began in May 1961. The first edition of the standard was published in 1963. Compared to earlier telegraph codes, the proposed Bell code and ASCII were both ordered for more convenient sorting (i.e., alphabetization) of lists.

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
            embed = discord.Embed(title="Ascii:", description="\n*starting from 32 because characters prior to that number are not used, therefore sending blanks* \n" + f'```py\n{", ".join(x)}```', colour=thecolor())
            embed.set_footer(text="Type ^help ascii to get information about what the ascii table is. | `,` signifies a new character.")
            return await ctx.send(embed=embed)
                        
        
       
        z = text.split(' ')
        for c in z:
            
            for t in c:
                p.append(str(ord(t)))
               
            x.append(f"\n`{c}: {'-'.join(p)}`")
            p = []
        embed = discord.Embed(title="Ascii:", description=", ".join(x), colour=thecolor())
        embed.set_footer(text="Type ^help ascii to get information about what the ascii table is. | '-' signifies a new character.")
        await ctx.send(embed=embed)
        

    @commands.command(aliases=["morse_code", 'mcode'], description="""Encode or decode text/morse code into morse code/plain text, type .morse for help""")
    async def morse(self, ctx, *, string):
        
        TEXT_TO_MORSE = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....',
            'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-',
            'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..',
            '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..',
            '9':'----.', '0':'-----', ',':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.',
            ')':'-.--.-', ':': '---...', "'": '.----.', "’": ".----.", '"': '.-..-.', ' ': '.......', '!': '-.-.--',
            '@': '.--.-.', '$': '...-..-', '&': '.-...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '_': '..--.-'
        }

        MORSE_TO_TEXT = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
            '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q',
            '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z',
            '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
            '-----': '0', '--..--': ',', '.-.-.-': '.', '..--..': '?', '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')',
            '---...': ':', '.----.': "'", '.-..-.': '"', '.......': ' ', '-.-.--': '!', '.--.-.': '@', '...-..-': '$', '.-...': '&',
            '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '..--.-': '_'
        }

        _tempset = set(string)
        check = True
        for char in _tempset:
            if char not in ['.', '-', ' ']:
                check = False
        
        if check is True:
            _templist = str(string).split(' ')
            converted = "".join(MORSE_TO_TEXT[str(i)] for i in _templist)

            await thebed(ctx, 'Morse ---> Text', f"```yaml\n{converted}```")
        else:
            _templist = []
            for char in str(string):
                _templist.append(char)
            try:
                converted = " ".join(TEXT_TO_MORSE[str(i).upper()] for i in _templist)
                if len(converted) <= 1998:
                    await thebed(ctx, 'Text ---> Morse', f"```yaml\n{converted}```")
                else:
                    entries = [f"`{converted[i:i+1998]}`" for i in range(0, len(converted), 1998)]
                    pager = StringPaginator(
                        pages=entries,
                        timeout=60
                    )
                    await pager.start(ctx)
            except KeyError as e:
                return await ctx.reply(f":x: The String contains some characters which cannot be converted into Morse!\n> If you think that's a Mistake, please report it to my Developers, they'll Review and fix it :)")




        
        
       

    @commands.command(aliases=['eval2', 'e2'], description='run code', hidden=True)
    async def evaldir(self, ctx, *, code):
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
        x = False
        with open('./dicts/Admins.json', 'r+') as k:
            data = json.load(k)
            
            for k in data['admins']:
                if ctx.author.id == k:
                    x = True
                    
            
            

        

        

        if not x:
            return
 

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

            
            
        
        code = clean_code(code)
        
    

        
      
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
        pre = await self.client.get_prefix(ctx.message)
        if ctx.message.content.strip(pre[0]).startswith('eval1'):
            y = ctx.message.content[6::]
            
            
            
        else:
            y = ctx.message.content[3::]
        
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
                colour=thecolor()
                )


            await pager.start(ctx) 
    @commands.command(aliases=['eval1', 'e1'], description='run code', hidden=True)
    async def evalreturn(self, ctx, *, code):
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
        x = False
        with open('./dicts/Admins.json', 'r+') as k:
            data = json.load(k)
            
            for k in data['admins']:
                if ctx.author.id == k:
                    x = True
                    
            
            

        

        

        if not x:
            return
 

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
            
                
            code = clean_code(code)
            
            

           
        
    
            

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
            
            
            #await self.client.chan.send(ctx.message.content.strip(pre[0]))
            pre = await self.client.get_prefix(ctx.message)
            
            if ctx.message.content.strip(pre[0]).startswith('eval1'):
                y = ctx.message.content[6::]
                
                
             
            else:
                y = ctx.message.content[3::]
            
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
                    colour=thecolor()
                    )


                await pager.start(ctx) 

    @commands.command(hidden=True)
    async def wcog(self, ctx, n):
        cmd = self.client.get_command(n)
        await ctx.send(cmd.cog.qualified_name)
    @commands.command(description='run code', hidden=True, aliases=['e'])
    async def eval(self, ctx, *, code):
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
        x = False
        with open('./dicts/Admins.json', 'r+') as k:
            data = json.load(k)
            
            for k in data['admins']:
                if ctx.author.id == k:
                    x = True
                    
            
            

        

        

        if not x:
            return

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

    
        pre = await self.client.get_prefix(ctx.message)
        if ctx.message.content.strip(pre[0]).startswith('eval'):
            y = ctx.message.content[6::]
            
            
            
        else:
            y = ctx.message.content[3::]
        

        ty = y.strip('```')
    
        if len(result) < 1800:
            await ctx.send(f"```py\nIn[{z}]: {ty}\nOut[{z}]: {theresult[0]}\n```")
        else:
            pager = Pag(
                timeout=100,
                #entries=[f"`{result[1:][:-1]}`"[i: i + 2000] for i in range(0, len(result), 2000)],
                entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
                length = 1,
                prefix = "```py\n", 
                suffix = "```",
                colour=thecolor()
                )


            await pager.start(ctx)
    @commands.command()
    async def dpy(self, ctx):


        page1 = Page(title='Page 1', description='First page test!')
        page1.add_field(name='Example A', value='Example B')

        page2 = Page(title='Page 2', description='Second page test!')
        page2.add_field(name='Example C', value='Example D')

        page3 = Page(title='Page 3', description='Third page test!')
        page3.add_field(name='Example E', value='Example F')

        menu = PaginatedMenu(ctx)
        menu.add_pages([page1, page2, page3])

        await menu.open()
    

def setup(client):
  client.add_cog(Utils(client))

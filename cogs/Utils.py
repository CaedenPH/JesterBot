from discord.ext.commands import context
from core.utils.emojis import CLOSE
import discord, os, requests, json, asyncio
from discord.ext import commands 

from pyMorseTranslator import translator
import pytz
from datetime import datetime

from core.utils.utils import thecolor, Json, thebed
from core.utils.commands.eval import run_eval
from core.Paginator import Paginator
from core.Context import Context

from dislash import *
import simpleeval
import yfinance as yf
import re
from typing import Tuple, Union
import unicodedata
import numpy as np

import wikipedia
import googletrans



sub = { 
                            '0': '⁰',
                            '1': '¹',
                            '2': '²',
                            '3': '³',
                            '4': '⁴',
                            '5': '⁵',
                            '6': '⁶',
                            '7': '⁷',
                            '8': '⁸',
                            '9': '⁹',
                            '-': '⁻'
                        }
calc = {}

def but(mode):
    style = ButtonStyle.grey
    style1 = ButtonStyle.green
    style2 = ButtonStyle.blurple
    
    row_1 = ActionRow()
    
    
    if mode != 'alg':
        row_2 = ActionRow()
        row_3 = ActionRow()
        if mode != 'sci':
            
            row_4 = ActionRow()
            row_5 = ActionRow()
    

    if mode == 'comp':
        for i in range(1, 10):
            if i <= 3:
                row_1.add_button(label=str(i), custom_id=str(i), style=style)
            elif i >= 3 and i <= 6:
                row_2.add_button(label=str(i), custom_id=str(i), style=style)
            else:
                row_3.add_button(label=str(i), custom_id=str(i), style=style)
        row_4.add_button(label="0", custom_id="0", style=style)
        row_4.add_button(label=".", custom_id=".", style=style)
        row_4.add_button(label="=", custom_id="=", style=style)

        row_1.add_button(label="* ", custom_id="*", style=style1)
        row_2.add_button(label="-", custom_id="-", style=style1)
        row_3.add_button(label="+", custom_id="+", style=style1)
        row_2.add_button(label="²", custom_id="²", style=style1)
        row_4.add_button(label="/", custom_id="/", style=style1)
        
        row_1.add_button(label="√", custom_id="√", style=style1)
    
    i = 0

    if mode == 'alg':
        style = ButtonStyle.green
        for e in ['x', 'y', 'z', ' --> ', ',']:
            
            row_1.add_button(label=str(e), custom_id=str(e), style=style)
            
           

            i += 1
        
    elif mode == 'sci':
        style = ButtonStyle.blurple
        i = 0
        for e in ['sin', 'cos', 'tan', 'sin⁻¹', 'cos', 'tan⁻¹', 'xⁿ', 'ₓ√ⁿ', 'π', '%', 'log', '!']:
            if i < 4:
                row_1.add_button(label=str(e), custom_id=str(e), style=style)
            elif i >= 4 and i <= 7:
                row_2.add_button(label=str(e), custom_id=str(e), style=style)
            else:
                row_3.add_button(label=str(e), custom_id=str(e), style=style)
    
            i += 1
        
        

       
    else:

        row_3.add_button(label="⌫", custom_id="Back", style=ButtonStyle.red)
        row_4.add_button(label="Clear", custom_id="Clear", style=ButtonStyle.red)
        

        row_5.add_button(label="(", custom_id="(", style=style2)
        row_5.add_button(label=")", custom_id=")", style=style2)
        
        row_5.add_button(label="Alg", custom_id="Alg", style=ButtonStyle.red)
        row_5.add_button(label="Sci", custom_id="Sci", style=ButtonStyle.red)
        row_5.add_button(label="Exit", custom_id="Exit", style=ButtonStyle.red)
    if mode == 'alg':

        return row_1
    elif mode == 'sci':
        return row_1, row_2, row_3
    return row_1, row_2, row_3, row_4, row_5





encoder = translator.Encoder()
decoder = translator.Decoder()


class Utils(commands.Cog):
    def __init__(self, bot):
   
        self.bot = bot

    @commands.command(name='plot')
    async def _plot(self, ctx:Context, xvals, yvals):
        xList = []
        yList = []
        for varx in xvals:
            xList.append(varx)
        for vary in yvals:
            yList.append(vary)
        xList.sort()
        yList.sort()
        x = np.array(xList)
        y = np.array(yList)
        arr = np.vstack((x, y))
        plt.plot(arr[0], arr[1])
        plt.title(f'{ctx.message.author}\'s Graph')
        file = open('./dicts/Name.json', 'r+')
        data = json.load(file)
        data['score'] += 1
        name = data['score']
        Json(file, data) 
        plt.savefig(fname=f"./graphs/{str(name)}.png")
        await ctx.send(file=discord.File(f"./graphs/{str(name)}.png"))
        #os.remove('plot.png')

    @commands.command(aliases=['wiki'])
    async def wikipedia(self, ctx, *, query):
        await ctx.em(wikipedia.summary(query))



    @commands.command(aliases=['trans', 'lang'])
    async def translate(self, ctx, _destination):
        translator = googletrans.Translator()
        
        await ctx.em(f'What language would you like to translate? **To:** {_destination}')
        msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)

        product = translator.translate(msg.content, dest=_destination)
        await ctx.em(product)





    @commands.command()
    async def charinfo(self, ctx:Context, *, characters: str):
        """Shows you information on up to 50 unicode characters."""
        match = re.match(r"<(a?):(\w+):(\d+)>", characters)
        if match:
            return await thebed(ctx, '', 'Custom emojis are not allowed')

        if len(characters) > 50:
            return await thebed(ctx, '', f"Too many characters ({len(characters)}/50)")

        def get_info(char: str) -> Tuple[str, str]:
            digit = f"{ord(char):x}"
            if len(digit) <= 4:
                u_code = f"\\u{digit:>04}"
            else:
                u_code = f"\\U{digit:>08}"
            url = f"https://www.compart.com/en/unicode/U+{digit:>04}"
            name = f"[{unicodedata.name(char, '')}]({url})"
            info = f"`{u_code.ljust(10)}`: {name} - {discord.utils.escape_markdown(char)}"
            return info, u_code

        char_list, raw_list = zip(*(get_info(c) for c in characters))
        embed = discord.Embed(color=thecolor())
        embed.add_field(name="Character info", value="\n".join(char_list))
        if len(characters) > 1:
            # Maximum length possible is 502 out of 1024, so there's no need to truncate.
            embed.add_field(name='Full Raw Text', value=f"`{''.join(raw_list)}`", inline=False)
        
        #await LinePaginator.paginate(char_list, ctx, embed, max_lines=10, max_size=2000, empty=False)
        await ctx.send(embed=embed)
        
    @commands.command(hidden=True)
    async def tt(self, ctx:Context):
        await ctx.send(dir(ctx.message))
    @commands.command(aliases=['calc'])
    async def calculator(self, ctx:Context):

        embed = discord.Embed(description=f"```yaml\n0```", color=self.bot.discordcolor)
        embed.set_author(name="Calculator", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="To interact with your virtual calculator, click the shown buttons.")     

        msg = await ctx.send(embed=embed, components=[k for k in but('comp')])

        
        sci, alg = False, False

        l = len(calc) + 1
        calc[str(l)] = {'d': '', 'i': [], 'au': ctx.author, 'm': msg}
        display = calc[str(l)]['d'] 
        mode = 'Computer'

        def check(inter):
            return inter.author == ctx.author and inter.message.id == msg.id

        try:
            
            inter = await msg.wait_for_button_click(check, timeout=10000000000) 

            while inter.clicked_button != "ejejkdeked":
                display = calc[str(l)]['d'] 
                if inter.clicked_button.custom_id == "Clear":

                    embed.description = f"```yaml\n0```"
                    
                    calc[str(l)]['d'] = ''

                    await inter.reply(type=7, embed=embed)

                elif inter.clicked_button.custom_id == "Exit":

                    embed.description =f"```yaml\nSession ended```"

                    return await inter.reply(type=7, embed=embed, components=[])
                
                elif inter.clicked_button.custom_id == "Sci":
                    if not sci:

                       # m = await ctx.send('\u200b', )
                        m = await ctx.send('\u200b', components=[s for s in but('sci')])
                        
                        calc[str(l)]['i'].append(m.id)
                        calc[str(l)]['s'] = m
                        sci = True

                    else:
                        await m.delete()
                        sci = False
                    await inter.respond(type=6)
                elif inter.clicked_button.custom_id == "Alg":
                    if not alg:


                        #y = await ctx.send('\u200b', components=[s for s in but('alg')])
                        y = await ctx.send('\u200b', components=[but('alg')])
                        calc[str(l)]['i'].append(y.id)
                        calc[str(l)]['a'] = y
                        alg = True
                    else:
                        await y.delete()
                        alg = False
                    await inter.respond(type=6)
                elif inter.clicked_button.custom_id == "Back":
                    
                    calc[str(l)]['d'] = calc[str(l)]['d'][:-1]

                    embed.description = f"```yaml\n{calc[str(l)]['d']}```"

                    await inter.reply(type=7, embed=embed)
                elif inter.clicked_button.custom_id == "=":
                    displayed = calc[str(l)]['d']
                    adv = False
                    for i in ['sin', 'cos', 'tan', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'j.', 'ₓ√ⁿ', 'π', '%', 'log', '!', 'x', 'y', 'z']:
                        if i in displayed:
                            adv = True
                            break
                    if adv:
                        #parser = InfixParser.Evaluator()
                        ndisplay = displayed
                    
                        ndisplay = displayed.replace('⁻¹', 'j.-1')
                        # for l in ('x', 'y', 'z'):
                        #     if l in ndisplay:
                        #         s = ndisplay.split(',')
                        #         for k in s:
                        #             if ' --> ' in k:
                        #                 lis = k.split(' --> ')
                        #                 parser.append_variable(str(lis[0]), int([lis[1]]))
                                        
                        for kk in sub:
                            ndisplay = ndisplay.replace(sub[kk], kk)
                        
                        output: float = parser.eval(ndisplay)
                    else:
                        if '√' in calc[str(l)]['d']:
                            ndisplay = ''
                            nume = 0
                            l = []
                            e = display.split(' ')
                            
                            for t in e:
                                if t == '√':
                                    l.append(nume)

                                nume += 1
                            
                            for k in l:

                                e[k], e[k+1] = e[k+1], e[k]
                            
                            displayed = "".join(e) 
                        
                        if not calc[str(l)]['d']:
                            calc[str(l)]['d'] = '0'
                            output = '0'
                        else:
                            ndisplay = displayed.strip(' ').replace('√', '**0.5').replace('²', '**2')
                            output = simpleeval.simple_eval(ndisplay)

                    embed.description = f"```yaml\nIn ❯❯ {calc[str(l)]['d']} \nOut ❯❯ {output}```"
                    
                    
                    await inter.reply(type=7, embed=embed)
                        
                    calc[str(l)]['d'] = str(output)

                else:
                    if calc[str(l)]['d'][::-1][:1] in ['j.', 
                            '-',
                            '⁰',
                            '¹',
                            '²',
                            '³',
                            '⁴',
                            '⁵',
                            '⁶',
                            '⁷',
                            '⁸',
                            '⁹']:
                            calc[str(l)]['d'] += f"{sub[inter.clicked_button.custom_id]}"
                    elif inter.clicked_button.custom_id in ['*', '/', '-', '+', '√', '²']:
                        calc[str(l)]['d'] += f" {inter.clicked_button.custom_id} "
                    
                        
                    else:
                        calc[str(l)]['d'] += f"{inter.clicked_button.custom_id}"

                    embed.description = f"```yaml\n{calc[str(l)]['d']}```"

                    await inter.reply(type=7, embed=embed)
                
                inter = await msg.wait_for_button_click(check, timeout=10000000000) 


        except Exception as e:
            
            #await thebed(ctx, '', e)
            await thebed(ctx, '', f'**Error. You somehow broke the calculator. Make sure you do:** ```yaml\nnumber operation number!``` **The error was:** ```yaml\n{e}```')

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if calc != {}:
            for k in calc:
                
                for uu in calc[k]['i']:
                
                    if inter.message.id == uu:
                        if inter.author == calc[k]['au']:
                            
                            if inter.clicked_button.custom_id == 'xⁿ':
                                calc[k]['d'] += 'j.'
                            elif inter.clicked_button.custom_id == '=':
                                pass
                            else:
                                calc[k]['d'] += inter.clicked_button.custom_id
                            msg = calc[k]['m']
                            embed = discord.Embed(description=f"```yaml\n{calc[k]['d']}```", color=self.bot.discordcolor)
                            embed.set_author(name="Calculator", icon_url=inter.author.avatar_url)
                            embed.set_footer(text="To interact with your virtual calculator, click the shown buttons.")
                            await msg.edit(embed=embed)
                            await inter.respond(type=6)
                
        

            
    @commands.command()
    async def qr(self, ctx:Context, *, text):
        m = await ctx.send("**Creating...**")
        async with ctx.typing():

            response = requests.get(f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={text}')   
        
        
        await thebed(ctx, f'Qr code for {text}', i=response.url)
        await m.delete()

    @commands.command(hidden=True)
    async def hibernate(self, ctx:Context):
        await ctx.send(':thumbsup:')
        self.bot.hiber = True
    @commands.command(hidden=True)
    async def hiber(self, ctx:Context):
        await ctx.send(':thumbsup:')
        self.bot.hiber = False

    @commands.command(
        
        )
    async def math(self, ctx:Context, *, math=None):
        if not math:
            return await thebed(ctx, '', "**The current list of available eval operations**", i="https://cdn.discordapp.com/attachments/836812307971571762/846334605669826600/unknown.png")
       
        result = simpleeval.simple_eval(math)
        embed = discord.Embed(color=thecolor())
        embed.set_footer(text=str(ctx.author) + " | Evaluation", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Your expression: ", value=f'```yaml\n"{math}"\n```', inline=False)
        embed.add_field(name="Result: ", value=f"```\n{result}\n```")
        await ctx.send(embed=embed)



    @commands.command(
        aliases=['fib'], 
        description="Sends the numbers of the fibinaci upto the number provided"
        )

    async def fibonacci(self, ctx:Context, sequences=10000000000000):
        x = []
        
        if sequences > 1000000000000000:
            sequences = 100000000000000

        a,b = 0, 1
        while a < sequences:
            x.append(str(a))
            
            a, b = b, a+b
    
        embed = discord.Embed(title="Fibinaci", description=f"{', '.join(x)}", colour=thecolor())
        await ctx.send(embed=embed)

    @commands.command(
        aliases=['av', 'avatars'], 
        description="Sends the mentioned users avatar or if none is specified, the usrs avatar"
        )

    async def avatar(self, ctx:Context, user:discord.Member = ""):
        if user == "":
            user = ctx.author.id
            username = self.bot.get_user(user)
            embed = discord.Embed(title=f"Avatar", colour=thecolor())
            embed.set_author(name=username.name, icon_url=username.avatar_url)
            embed.set_image(url=username.avatar_url)
            await ctx.send(embed=embed)
        
        else:

            username = self.bot.get_user(user.id)
            embed = discord.Embed(title=f"Avatar", colour=thecolor())
            embed.set_author(name=username.name, icon_url=username.avatar_url)
            embed.set_image(url=username.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['tz', 'time', 'zone'], description="Sends the current time of the [origin]. To get all of the places recognisable, leave `origin` blank")
    async def timezone(self, ctx:Context, origin=None):
        try:
            if not origin:
                var = ""
                num = 0
                result = pytz.all_timezones
                y = Paginator(ctx)   
                return await y.paginate(content=", ".join(result), name='Timezones')

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
    
    @commands.command(aliases=['bin'])
    async def binary(self, ctx:Context, *, text):
       
        
        response = requests.get(f'https://some-random-api.ml/binary?text={text}')
        fox = response.json()
        embed=discord.Embed(color=thecolor())
        embed.add_field(name="Binary", value=f"{fox['binary']}")
        await ctx.send(embed=embed)
   

    @commands.command(aliases=['unbin'])
    async def unbinary(self, ctx:Context, *, nums:str):
      
        
        response = requests.get(f'https://some-random-api.ml/binary?decode={nums}')
        fox = response.json()
        embed=discord.Embed(color=thecolor())
        embed.add_field(name="Decoded from binary", value=f"{fox['text']}") 
        await ctx.send(embed=embed)
   
    
    @commands.command(description="""ASCII was developed from telegraph code. Work on the ASCII standard began in May 1961. The first edition of the standard was published in 1963. Compared to earlier telegraph codes, the proposed Bell code and ASCII were both ordered for more convenient sorting (i.e., alphabetization) of lists.

The use of ASCII format for Network Interchange was described in 1969. That document was formally elevated to an Internet Standard in 2015.

Originally based on the English alphabet, ASCII encodes 128 specified characters into seven-bit integers as shown by the ASCII chart above. Ninety-five of the encoded characters are printable: these include the digits 0 to 9, lowercase letters a to z, uppercase letters A to Z, and punctuation symbols. 

For example, lowercase i would be represented in the ASCII encoding by binary 1101001 = hexadecimal 69 (i is the ninth letter) = decimal 105.
To get the ascii table type j.ascii

Source: [Website](https://en.wikipedia.org/wiki/ASCII)
    """)
    async def ascii(self, ctx:Context, *, text=None):
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
            embed.set_footer(text="Type j.help ascii to get information about what the ascii table is. | `,` signifies a new character.")
            return await ctx.send(embed=embed)
                        
        
       
        z = text.split(' ')
        for c in z:
            
            for t in c:
                p.append(str(ord(t)))
               
            x.append(f"\n`{c}: {'-'.join(p)}`")
            p = []
        embed = discord.Embed(title="Ascii:", description=", ".join(x), colour=thecolor())
        embed.set_footer(text="Type j.help ascii to get information about what the ascii table is. | '-' signifies a new character.")
        await ctx.send(embed=embed)
        

    @commands.command(aliases=["morse_code", 'mcode'], description="""Encode or decode text/morse code into morse code/plain text, type .morse for help""")
    async def morse(self, ctx:Context, *, string):
        
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
                    
                    y = await Paginator(ctx)
                    await y.paginate(content=converted, name='Morse/Text')
            except KeyError as e:
                return await ctx.reply(f"{CLOSE} The String contains some characters which cannot be converted into Morse!\n> If you think that's a Mistake, please report it to my Developers, they'll Review and fix it :)")

       

    @commands.command(aliases=['eval2', 'e2'], description='run code', hidden=True)
    async def evaldir(self, ctx:Context, *, code):
        x = await run_eval(ctx, code, _eval='dir')

        try:
            await ctx.send(x)
        except:
            pass

    @commands.command(aliases=['eval1', 'e1'], description='run code', hidden=True)
    async def evalreturn(self, ctx:Context, *, code):
        x = await run_eval(ctx, code, _eval='return')

        try:
            await ctx.send(x)
        except:
            pass
    
    @commands.command(description='run code', hidden=True, aliases=['e'])
    async def eval(self, ctx:Context, *, code):
        x = await run_eval(ctx, code)
        try:
            await ctx.send(x)
        except:
            pass
       
    
def setup(bot):
  bot.add_cog(Utils(bot))

import discord, os, requests, json, asyncio
from discord.ext.commands import has_permissions
from discord.ext import commands 
from discord.utils import get
from asyncio import sleep
from random import choice, randint
from core.utils.utils import thecolor, thebed
from core.Context import Context

from dislash import *
import random

def card_check(card1):
    card = ""
    for k in card1:
        if k not in [':', '>', '<']:
            card += k

    visual = ""
    if card.startswith('Y'):
        n = 'Yellow'
        second_part = card[6:8]
        
    elif card.startswith('R'):
        n = 'Red'
        second_part = card[3:5]
    elif card.startswith('B'):
        n = 'Blue'
        second_part = card[4:6]
    else:
        n = 'Green'
        second_part = card[5:7]
    if int(second_part) < 10:
        if int(second_part) == 0:
            visual = str(second_part[1:])
        visual = second_part.strip('0')
    else:
        visual = "- "

    return n, second_part, visual
class Card:
        def __init__(self):
            self.suit = choice(['Hearts ðŸŽ”', 'Diamonds â—†', 'Clubs â™§', 'Spades â™¤'])
            self.num = randint(1, 13)
            self.show = self.num
            if self.num in [1, 11, 12, 13]:
                if self.num == 1:
                    self.show = 'Ace'
                    self.num = 0
                else:
                    self.num = 10
                    self.show = choice(['King', 'Jack', 'Queen'])
            self.card = f"{self.show} of {self.suit}"
async def buno(ctx, title, description='', **kwargs):
    theembed = discord.Embed(title=title, description=description, color=thecolor())
    theembed.set_author(icon_url=ctx.author.avatar.url, name='Uno')
    author = kwargs.get('a')
    icon_url = kwargs.get('i_u')
    footer = kwargs.get('f')
    thumbnail = kwargs.get('t')
    image = kwargs.get('i')
    if footer:
        theembed.set_footer(text=footer)
    if author:
        theembed.set_author(name=author)
        if icon_url:
            theembed.set_author(name=author, icon_url=icon_url)
    if thumbnail:
        theembed.set_thumbnail(url=thumbnail)
    if image:
        theembed.set_image(url=image)
    await ctx.send(embed=theembed)

class Games(commands.Cog):
    def __init__(self, bot):

        self.bot = bot
    
    @commands.command(aliases=['rr'], description="You play russian roulette with yourself - 1 in 6 chance you will die...Be warned!")
    async def russianroulette(self, ctx:Context):
        rand = randint(1, 5)
        if rand == 1:
            embed = discord.Embed(title="🔫 / You died", colour=thecolor())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🌹 / You lived", colour=thecolor())
            await ctx.send(embed=embed)
    @commands.command(aliases=['bj'], description="Emits a game of blackjack with the user")
    async def blackjack(self, ctx:Context):
        one_ace = False
        BotHit = False

        Player_Card_1 = Card()
        Player_Card_2 = Card()

        Oposition_Card_1 = Card()
        Oposition_Card_2 = Card()

        Player_Total = Player_Card_1.num + Player_Card_2.num 
        Oposition_Total = Oposition_Card_1.num + Oposition_Card_2.num 

        embed = discord.Embed(description=f"**Your cards:** \n{Player_Card_1.card} \n {Player_Card_2.card}\n\n**Type h to hit or s to stand**", colour=thecolor())
        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
        embed.set_footer(text="K, Q, J = 10  |  A = 1 or 11")
        await ctx.send(embed=embed)
        #Opponent ace
        if Oposition_Card_1.num == 0:
            Oposition_Total += 1
        if Oposition_Card_2.num == 0:
            Oposition_Total += 1

        if Oposition_Total < 10:
            Oposition_Card_3 = Card()
            BotHit = True
            Oposition_Total += Oposition_Card_3.num
            if Oposition_Card_1.num == 0 and Oposition_Total != 10:
                Oposition_Total += 1
            else:
                Oposition_Total += 11
            if Oposition_Card_2.num == 0 and Oposition_Total != 10:
                Oposition_Total += 1
            else:
                Oposition_Total += 11
    
        #ACE
    
        try:
            received_msg2 = str((await self.bot.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
            while received_msg2 != "s":
                if received_msg2 == "h":
                    Player_Card_3 = Card()
                    if Player_Card_3.num != 0:
                        Player_Total += Player_Card_3.num
                        embed = discord.Embed(description=f"**Your card:** \n {Player_Card_3.card}", colour=thecolor())
                        embed.set_footer(text="Type s to stand or h to hit")
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        if Player_Total > 21:
                            embed = discord.Embed(title="You lose because you went over! Restart the game", colour=thecolor())
                            embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                            return await ctx.send(embed=embed)
                        


                    else:
                        embed = discord.Embed(description="You drew an ace, choose 1 or 11 for its value", colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        try:
                            received_msg1 = str((await self.bot.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                            if received_msg1 == "1":
                                Player_Total += 1
                                embed = discord.Embed(description=f"Type h to hit or s to stand", colour=thecolor())
                                embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                            elif received_msg1 == "11":
                                Player_Total += 11
                                embed = discord.Embed(description=f"Type h to hit or s to stand", colour=thecolor())
                                embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=thecolor())
                            embed = discord.Embed(description=f"Type h to hit or s to stand", colour=thecolor())
                            embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        except asyncio.TimeoutError:
                            embed = discord.Embed(title="I gave up waiting", colour=thecolor())
                            return await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(title="Incorrect answer, restart the game", colour=thecolor())
                    return await ctx.send(embed=embed)
                    
                received_msg2 = str((await self.bot.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
            else:
                if Player_Card_1.num == 0:
                    embed = discord.Embed(description="You have an ace, choose 1 or 11 for its value", colour=thecolor())
                    embed.set_author(name="Blackjack", icon_url = ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                    one_ace = True
                    try:
                        received_msg = str((await self.bot.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                        if Player_Card_2.num != 0:
                            if received_msg == "1":
                                Player_Total += 1
                                
                            
                            elif received_msg == "11":
                                Player_Total += 11
                            
                        
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=thecolor())
                                return await ctx.send(embed=embed)
                        else:
                            if received_msg == "1":
                                Player_Total += 1
                            elif received_msg == "11":
                                Player_Total += 11
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=thecolor())
                                return await ctx.send(embed=embed)

                        await ctx.send(embed=embed)
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title="I gave up waiting", colour=thecolor())
                        await ctx.send(embed=embed)
                        return await ctx.send(embed=embed)

                if Player_Card_2.num == 0:
                    if one_ace:

                        embed = discord.Embed(description="You have an ace, choose 1 or 11 for its value", colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        try:
                            received_msg = str((await self.bot.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                            if received_msg == "1":
                                Player_Total += 1
                        
                            elif received_msg == "11":
                                Player_Total += 11
                            
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=thecolor())
                                return await ctx.send(embed=embed)
                            await ctx.send(embed=embed)
                        except asyncio.TimeoutError:
                            embed = discord.Embed(title="I gave up waiting", colour=thecolor())
                            return await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(description="You have an ace, choose 1 or 11 for its value", colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        try:
                            received_msg = str((await self.bot.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                            if received_msg == "1":
                                Player_Total += 1
                        
                            elif received_msg == "11":
                                Player_Total += 11
                
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=thecolor())
                                return await ctx.send(embed=embed)
                            await ctx.send(embed=embed)

                        except asyncio.TimeoutError:
                            embed = discord.Embed(title="I gave up waiting", colour=thecolor())
                            return await ctx.send(embed=embed)

                if Player_Total > 21:
                    embed = discord.Embed(title="You went over 21!", colour=thecolor())
                    return await ctx.send(embed=embed)
                if BotHit:
                    if Player_Total > Oposition_Total:
                        embed = discord.Embed(title="You won against the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**", colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        return await ctx.send(embed=embed)

                    elif Player_Total < Oposition_Total:
                        embed = discord.Embed(title="You lost to the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**", colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        return await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(titlen="You drew with the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**",  colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        return await ctx.send(embed=embed)

                else:

                    if Player_Total > Oposition_Total:
                        embed = discord.Embed(title="You won against the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**", colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        return await ctx.send(embed=embed)

                    elif Player_Total < Oposition_Total:
                        embed = discord.Embed(title="You lost to the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**", colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        return await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(titlen="You drew with the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**",  colour=thecolor())
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar.url)
                        return await ctx.send(embed=embed)


        except asyncio.TimeoutError:
            embed = discord.Embed(title="I gave up waiting", colour=thecolor())
            return await ctx.send(embed=embed)

    
 
    @commands.command(aliases=['dices', 'die'], description="Rolls a dice and compares the number to `<roll>`, difficulty can be; easiest (1 in 2 chance), easy (1 in 3 chance), normal (1 in 6 chance), hard (1 in 9 chance), impossible (1 in 15 chance)")
    async def dice(self, ctx:Context, num, difficulty = "normal"):
        try:

            num = int(num)
        except Exception as e:
            return await thebed(ctx, 'That is not an integer!')
            
        async def ea():
            
            rollrig = ['1', '2', '3', '4', '5', '6']
            rand = randint(1, 2)
            rollrigy = choice(rollrig)
            print(rand)
            async def displaycorrect():
                nonlocal rollrigy
                
                if num != int(rollrigy):
                    rollrig = [str(num)]
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=thecolor())
                await ctx.send(embed=embed)
                
            
        
            async def displaywrong():
                nonlocal rollrigy, rollrig
            
                if int(rollrigy) == num:
                    rollrig.remove(str(num))
                    
                    rollrigy = choice(rollrig)
                    embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=thecolor())
                    await ctx.send(embed=embed)
                    
        
            if num == 1:
                if rand == 1:
                    await displaycorrect()

                elif rand != 1:
                    await displaywrong()
                
            if num == 2:
                if rand == 1:
                    await displaycorrect()
                elif rand != 1:
                    await displaywrong()
            if num == 3:
                if rand == 1:
                    await displaycorrect()
                elif rand != 1:
                    await displaywrong()

            if num == 4:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()
                
            if num == 5:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()
                
            if num == 6:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()
            
        async def easy():
            rollrig = ['1', '2', '3', '4', '5', '6']
            rand = randint(1, 3)
            rollrigy = choice(rollrig)
            
            async def displaycorrect():
                nonlocal rollrigy
                
                if num != int(rollrigy):
                    rollrig = [str(num)]
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=thecolor())
                await ctx.send(embed=embed)
                
            

            async def displaywrong():
                nonlocal rollrigy
                
                if int(rollrigy) == num:
                    rollrig.remove(str(num))
                    
                    rollrigy = choice(rollrig)
                embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=thecolor())
                await ctx.send(embed=embed)
            if num == 1:
                if rand == 1:
                    await displaycorrect()

                elif rand != 1:
                    await displaywrong()
                
            if num == 2:
                if rand == 1:
                    await displaycorrect()
                elif rand != 1:
                    await displaywrong()
            if num == 3:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()
                
            if num == 4:
                if rand == 2:
                    await displaycorrect()
                elif rand != 2:
                    await displaywrong()
            if num == 5:
                if rand == 3:
                    await displaycorrect()
                elif rand != 3:
                    await displaywrong()
            if num == 6:
                if rand == 3:
                    await displaycorrect()
                    
                elif rand != 3:
                    await displaywrong()
            
        async def normal():
            rand = randint(1, 6)
            rollrig = ['1', '2', '3', '4', '5', '6']
            rollrigy = choice(rollrig)
        
            
            if int(rollrigy) == num:
                rollrig.remove(str(num))
                print(rollrig)
                rollrigy = choice(rollrig)
            if rand == num: 
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=thecolor())
                await ctx.send(embed=embed)
                
            elif rand != num:
                embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=thecolor())
                await ctx.send(embed=embed)
                

            
        async def hard():
            rand = randint(1, 9)
            rollrig = ['1', '2', '3', '4', '5', '6']
            rollrigy = choice(rollrig)
    
            
            if int(rollrigy) == num:
                rollrig.remove(str(num))
                print(rollrig)
            if rand == num: 
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=thecolor())
                await ctx.send(embed=embed)
            
            elif rand != num:
                embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=thecolor())
                await ctx.send(embed=embed)
        

        async def impossible():
            rand = randint(1, 20)
            rollrig = ['1', '2', '3', '4', '5', '6']
            rollrigy = choice(rollrig)
            
            
            if int(rollrigy) == num:
                rollrig.remove(str(num))
                print(rollrig)
            if rand == num: 
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=thecolor())
                await ctx.send(embed=embed)
                
            elif rand != num:
                embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=thecolor())
                await ctx.send(embed=embed)
            


        if difficulty == "normal":
            await normal()

        elif difficulty == "hard":
            await hard()

        elif difficulty == "easy":
            await easy()

        elif difficulty == "impossible":
            await impossible()

        elif difficulty == "easiest":
            await ea()

    

    @commands.command(aliases=['rock', 'rockpaperscissors'], description="Plays rock paper scissors with the bot `<choice>` must be rock, paper, or scissors")
    async def rps(self, ctx:Context, roll):

        random_num = randint(0, 2)
        
        if roll not in ['rock', 'paper', 'scissors']:
            embed = discord.Embed(title="Thats not an option. Choose rock, paper, or scissors...", colour=thecolor())
            await ctx.send(embed=embed)
            
        if random_num == 0:
            cpu_choice = "rock"

        elif random_num == 1:
            cpu_choice = "paper"
        elif random_num == 2:
            cpu_choice = "scissors"
        
        if roll == "rock":
            if cpu_choice == "rock":
                embed = discord.Embed(title="You drew", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you drew", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
                
                await ctx.send(embed=embed)
            elif cpu_choice == "paper":
                embed = discord.Embed(title="You lost", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you lost", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)
            
            elif cpu_choice == "scissors":
                embed = discord.Embed(title="You won", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you won", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)        

        if roll == "paper":
            if cpu_choice == "paper":
                embed = discord.Embed(title="Drew", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you drew", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
                
                await ctx.send(embed=embed)
            
            elif cpu_choice == "scissors":
                embed = discord.Embed(title="You lost", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you lost", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
    
                await ctx.send(embed=embed)
            
            elif cpu_choice == "rock":
                embed = discord.Embed(title="You won", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you won", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)        
            
        if roll == "scissors":
            if cpu_choice == "scissors":
                embed = discord.Embed(title="You drew", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you drew", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)
            elif cpu_choice == "rock":
                embed = discord.Embed(title="You lost", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you lost", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
            
                await ctx.send(embed=embed)
            
            elif cpu_choice == "paper":
                embed = discord.Embed(title="You won", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you won", colour=thecolor())
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)

        
    @commands.command(aliases=['rpsbait', 'rpsbaits', 'RPSB', 'RockPaperScissorsBait'], description="Emits a fake rock paper scissors game with a bot")
    async def rpsfail(self, ctx:Context):
        embed = discord.Embed(title=f"Rock paper scissors!", colour=thecolor())
        msg = await ctx.send(embed=embed)
        
        await msg.add_reaction("\U0001f4bf")
    
        await msg.add_reaction('\U0001f4f0')
        await msg.add_reaction('\U00002702')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '\U0001f4bf'

        reaction, user = await self.self.bot.wait_for('reaction_add', check=check)
        await msg.delete()
        embed = discord.Embed(title=f"Baited", colour=thecolor())
        await ctx.send(embed=embed)

  
   
    @commands.command(aliases=['gussing', 'Guessing', 'Guessing_game','gg'], description="Plays a guessinggame with the bot (bot thinks of a number)")
    async def guessinggame(self, ctx:Context):
        rand = randint(1, 100)
        embed = discord.Embed(title=f"Give me a number between 1-100, the game has started'", colour=thecolor())
        await ctx.send(embed=embed)
        
        
        
        try:
            received_msg = int((await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=10)).content)
            while received_msg != rand:
                
                
                if received_msg > rand:
                    embed = discord.Embed(title="Lower", colour=thecolor())
                    await ctx.send(embed=embed)
                    
                    
                elif received_msg < rand:
                    embed = discord.Embed(title="Higher", colour=thecolor())
                    await ctx.send(embed=embed)
                elif str(received_msg) == "q":
                    embed = discord.Embed(title="Goodbye", colour=thecolor())
                    return await ctx.send(embed=embed)
                received_msg = int((await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=10)).content)
            else:
                embed = discord.Embed(title=f"Correct! The answer was {rand}", colour=thecolor())
                return await ctx.send(embed=embed)
                
                
        except asyncio.TimeoutError:
            embed = discord.Embed(title="I gave up waiting", colour=thecolor())
            await ctx.send(embed=embed)
    








    
    @commands.command(
        aliases=['playuno', 'unos', 'ungogame']

    )
    async def uno(self, ctx:Context):
        cards_played = []  
        emoji_list = []
        url_list = []
        card_list = []
        mentions = []
        msglist = []
        clicked = []
        player_cards = {}
        play = False
        #EMOJIS
        
        
        emojifile = open('./dicts/cards.json')
        data = json.load(emojifile)

        for key in data:
            for key_key in data[key]:
                
                emoji_list.append(f"{data[key][key_key]['emoj']}")
                url_list.append(f"{data[key][key_key]['url']}")

                
                if int(key_key[:2]) < 10:
                    
                    card_list.append(f"{data[key][key_key]['url']}")
        
        
        participants = [ctx.author]
        #MEMBERS

        await thebed(ctx, '', 'Mention who you would like to play against; if you do not want to play against anyone type `bot` to play against the bot. Put a space in between each person you want to ping.', a='Uno', i_u=ctx.author.avatar.url)


        try:
            received_msg = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)

            if received_msg.mentions:

                for k in received_msg.mentions:
                    if k != ctx.author:
                        mentions.append(k)
                        participants.append(k)
                    if not mentions:
                        return await buno(ctx, '', 'You need to choose someone other than yourself!')

                    msg = await ctx.send(embed=discord.Embed(description=f"React with this to play: {', '.join([k.name for k in mentions])}", color=thecolor()))
                    await msg.add_reaction('🎲')
                    await self.bot.wait_until_ready()
                    
                    try:
                        emoji, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=lambda e, u: u in mentions) 
                        msgd = await ctx.channel.fetch_message(msg.id)  
                        
                        while msgd.reactions[0].count - 1 != len(received_msg.mentions):
                            
                            emoji, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=lambda e, u: u in mentions)  
                        
                            
                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        await msg.edit(embed=discord.Embed(description='I received no response!', color=thecolor()))
                
                    
                


            else:


                if not received_msg.content == "bot":
                    
                    return await buno(ctx, 'Restart game', 'You need to ping valid members to play with you.')



        except asyncio.TimeoutError:
            await thebed(ctx, '', 'You did not mention anyone within 2 minutes.')


        #PLAY
        
            
        starting_card1 = choice(emoji_list)

        check = card_check(starting_card1)
        
        starting_card_emoji = data[check[0]][f"{check[1]}.png"]['emoj']
        starting_card_color = check[1]
        cards_played.append(starting_card_color)
        starting_card_url = data[check[0]][f"{check[1]}.png"]['url']
        emoji_list.remove(starting_card_emoji)
        url_list.remove(starting_card_url)

        random.shuffle(participants)
        
        unobed1 = discord.Embed(description=f"""It is {participants[0].mention}'s go! 
        {participants[0].name} press  the button and select a card to play. 
        The order is {', '.join([m.name for m in participants])}""", color=thecolor())
        unobed1.set_author(name="Uno", icon_url=ctx.author.avatar.url)
        unobed1.set_footer(text="Press the button to see your cards")
        unobed1.set_image(url=starting_card_url)


        msg = await ctx.send(embed=unobed1, components=[Button(
                style=ButtonStyle.grey,
                label="See your cards",
                custom_id="cards"
            )])
        msglist.append(msg.id)
        game = True
        
        for t in participants:
            player_cards[t] = {'cards': [], 'num':7}
            clicked.append(t)
            player_cards[t]['opt'] = SelectMenu(
                    custom_id="test",
                    placeholder=f"Your cards",
                    max_values=1,
                    options=[]
                )
            for i in range(0, 7):
                card = choice(emoji_list)
                ncheck = card_check(card)
                player_cards[t]['opt'].add_option(f'{ncheck[2]} of {ncheck[0]}',f'{ncheck[1]} of {ncheck[0]}', emoji=data[ncheck[0]][f"{ncheck[1]}.png"]['emoj'])
                emoji_list.remove(data[ncheck[0]][f"{ncheck[1]}.png"]['emoj'])
                player_cards[t]['cards'].append(card)
        #HANDS OF PLAYERS
        
       

        def check(inter):
            return inter.message.id == msg.id and inter.author in clicked
        

            
        while len(clicked) != 0:
            
            inter = await msg.wait_for_button_click(check)
            clicked.remove(inter.author)
            
            
            await inter.reply("\u200b", type=4, ephemeral=True, components=[player_cards[inter.author]['opt']])

        def check(interd):
            print(interd.author, participants, interd.message.id, msg.id)
            #return interd.message.id == msg.id and interd.author in participants
            return True
        print(participants)
        new_inter = await msg.wait_for_dropdown(check)
        print(new_inter.author)
    
        if new_inter.author != participants[0]:
            await new_inter.reply("It isn't your turn!", type=4, ephemeral=True)
        else:
            chosen_card = new_inter.select_menu.selected_options[0].label.split(' ')
            card_num = chosen_card[0]
            card_color = chosen_card[1]
            if card_color == cards_played -1:
                await new_inter.reply("worked so far", type=4, ephemeral=True)
            else:
                print(card_color, cards_played, card_num, chosen_card)
                

def setup(bot):
  bot.add_cog(Games(bot))

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
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from random import choice, randint
from discord.ext.buttons import Paginator

class Pag(Paginator):
    async def teardown(self):
        try:
            
            await self.page.clear_reactions()
            
        except discord.HTTPException:
            pass
def Json(pref, data1):
    pref.seek(0)  # set point at the beginning of the file
    pref.truncate(0)  # clear previous content
    pref.write(json.dumps(data1, indent=4)) # write to file

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
class TheColor:
    def __init__(self):
        
        with open('./dicts/Color.json', 'r') as k:
            data = json.load(k)
            self.color = data['Color']['color'] 
    
    
xz = int(TheColor().color, 16)
async def embed(ctx, title, description=""):
    embed = discord.Embed(title=title, color=xz)
    if description:

        embed = discord.Embed(title=title, description=description, color=xz)
    await ctx.send(embed=embed)
class Games(commands.Cog):
    def __init__(self, client):

        self.client = client
    
    @commands.command(aliases=['rr'], help="You play russian roulette with yourself - 1 in 6 chance you will die...Be warned!")
    async def russianroulette(self, ctx):
        rand = randint(1, 5)
        if rand == 1:
            embed = discord.Embed(title="🔫 / You died", colour=xz)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🌹 / You lived", colour=xz)
            await ctx.send(embed=embed)
    @commands.command(aliases=['bj'], help="Emits a game of blackjack with the user")
    async def blackjack(self, ctx):
        one_ace = False
        BotHit = False
        # embed = discord.Embed(colour=xz)
        # embed.set_author(name="Blackjack", icon_url = ctx.author.avatar_url)
        class Card:
            def __init__(self):
                self.suit = choice(['Hearts 🎔', 'Diamonds ◆', 'Clubs ♧', 'Spades ♤'])
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

        Player_Card_1 = Card()
        Player_Card_2 = Card()

        Oposition_Card_1 = Card()
        Oposition_Card_2 = Card()

        Player_Total = Player_Card_1.num + Player_Card_2.num 
        Oposition_Total = Oposition_Card_1.num + Oposition_Card_2.num 

        embed = discord.Embed(description=f"**Your cards:** \n{Player_Card_1.card} \n {Player_Card_2.card}\n\n**Type h to hit or s to stand**", colour=xz)
        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
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
            received_msg2 = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
            while received_msg2 != "s":
                if received_msg2 == "h":
                    Player_Card_3 = Card()
                    if Player_Card_3.num != 0:
                        Player_Total += Player_Card_3.num
                        embed = discord.Embed(description=f"**Your card:** \n {Player_Card_3.card}", colour=xz)
                        embed.set_footer(text="Type s to stand or h to hit")
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                        if Player_Total > 21:
                            embed = discord.Embed(title="You lose because you went over! Restart the game", colour=xz)
                            embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                            return await ctx.send(embed=embed)
                        


                    else:
                        embed = discord.Embed(description="You drew an ace, choose 1 or 11 for its value", colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                        try:
                            received_msg1 = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                            if received_msg1 == "1":
                                Player_Total += 1
                                embed = discord.Embed(description=f"Type h to hit or s to stand", colour=xz)
                                embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                            elif received_msg1 == "11":
                                Player_Total += 11
                                embed = discord.Embed(description=f"Type h to hit or s to stand", colour=xz)
                                embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=xz)
                            embed = discord.Embed(description=f"Type h to hit or s to stand", colour=xz)
                            embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        except asyncio.TimeoutError:
                            embed = discord.Embed(title="I gave up waiting", colour=xz)
                            return await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(title="Incorrect answer, restart the game", colour=xz)
                    return await ctx.send(embed=embed)
                    
                received_msg2 = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
            else:
                if Player_Card_1.num == 0:
                    embed = discord.Embed(description="You have an ace, choose 1 or 11 for its value", colour=xz)
                    embed.set_author(name="Blackjack", icon_url = ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    one_ace = True
                    try:
                        received_msg = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                        if Player_Card_2.num != 0:
                            if received_msg == "1":
                                Player_Total += 1
                                
                            
                            elif received_msg == "11":
                                Player_Total += 11
                            
                        
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=xz)
                                return await ctx.send(embed=embed)
                        else:
                            if received_msg == "1":
                                Player_Total += 1
                            elif received_msg == "11":
                                Player_Total += 11
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=xz)
                                return await ctx.send(embed=embed)

                        await ctx.send(embed=embed)
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title="I gave up waiting", colour=xz)
                        await ctx.send(embed=embed)
                        return await ctx.send(embed=embed)

                if Player_Card_2.num == 0:
                    if one_ace:

                        embed = discord.Embed(description="You have an ace, choose 1 or 11 for its value", colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                        try:
                            received_msg = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                            if received_msg == "1":
                                Player_Total += 1
                        
                            elif received_msg == "11":
                                Player_Total += 11
                            
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=xz)
                                return await ctx.send(embed=embed)
                            await ctx.send(embed=embed)
                        except asyncio.TimeoutError:
                            embed = discord.Embed(title="I gave up waiting", colour=xz)
                            return await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(description="You have an ace, choose 1 or 11 for its value", colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                        try:
                            received_msg = str((await self.client.wait_for('message', timeout=90.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel,)).content).lower()
                            if received_msg == "1":
                                Player_Total += 1
                        
                            elif received_msg == "11":
                                Player_Total += 11
                
                            else:
                                embed = discord.Embed(title="Choose 1 or 11, restart the game", colour=xz)
                                return await ctx.send(embed=embed)
                            await ctx.send(embed=embed)

                        except asyncio.TimeoutError:
                            embed = discord.Embed(title="I gave up waiting", colour=xz)
                            return await ctx.send(embed=embed)

                if Player_Total > 21:
                    embed = discord.Embed(title="You went over 21!", colour=xz)
                    return await ctx.send(embed=embed)
                if BotHit:
                    if Player_Total > Oposition_Total:
                        embed = discord.Embed(title="You won against the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**", colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        return await ctx.send(embed=embed)

                    elif Player_Total < Oposition_Total:
                        embed = discord.Embed(title="You lost to the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**", colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        return await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(titlen="You drew with the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n{Oposition_Card_3.card}\n**Opponent scored {Oposition_Total}**",  colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        return await ctx.send(embed=embed)

                else:

                    if Player_Total > Oposition_Total:
                        embed = discord.Embed(title="You won against the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**", colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        return await ctx.send(embed=embed)

                    elif Player_Total < Oposition_Total:
                        embed = discord.Embed(title="You lost to the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**", colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        return await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(titlen="You drew with the opposition!", description=f"**The opponents cards were:** \n{Oposition_Card_1.card}\n{Oposition_Card_2.card}\n**Opponent scored {Oposition_Total}**",  colour=xz)
                        embed.set_author(name=f"Blackjack - Score: {Player_Total}", icon_url = ctx.author.avatar_url)
                        return await ctx.send(embed=embed)


        except asyncio.TimeoutError:
            embed = discord.Embed(title="I gave up waiting", colour=xz)
            return await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def t(self, ctx, d, t=""):
        await embed(ctx, d, t)
 
    @commands.command(aliases=['dices', 'die'], help="Rolls a dice and compares the number to `<roll>`, difficulty can be; easiest (1 in 2 chance), easy (1 in 3 chance), normal (1 in 6 chance), hard (1 in 9 chance), impossible (1 in 15 chance)")
    async def dice(self, ctx, num, difficulty = "normal"):
        try:

            num = int(num)
        except Exception as e:
            return await embed(ctx, 'That is not an integer!')
            
        async def ea():
            
            rollrig = ['1', '2', '3', '4', '5', '6']
            rand = randint(1, 2)
            rollrigy = choice(rollrig)
            print(rand)
            async def displaycorrect():
                nonlocal rollrigy
                
                if num != int(rollrigy):
                    rollrig = [str(num)]
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=xz)
                await ctx.send(embed=embed)
                
            
        
            async def displaywrong():
                nonlocal rollrigy, rollrig
            
                if int(rollrigy) == num:
                    rollrig.remove(str(num))
                    
                    rollrigy = choice(rollrig)
                    embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=xz)
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
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=xz)
                await ctx.send(embed=embed)
                
            

            async def displaywrong():
                nonlocal rollrigy
                
                if int(rollrigy) == num:
                    rollrig.remove(str(num))
                    
                    rollrigy = choice(rollrig)
                embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=xz)
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
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=xz)
                await ctx.send(embed=embed)
                
            elif rand != num:
                embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=xz)
                await ctx.send(embed=embed)
                

            
        async def hard():
            rand = randint(1, 9)
            rollrig = ['1', '2', '3', '4', '5', '6']
            rollrigy = choice(rollrig)
    
            
            if int(rollrigy) == num:
                rollrig.remove(str(num))
                print(rollrig)
            if rand == num: 
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=xz)
                await ctx.send(embed=embed)
            
            elif rand != num:
                embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=xz)
                await ctx.send(embed=embed)
        

        async def impossible():
            rand = randint(1, 20)
            rollrig = ['1', '2', '3', '4', '5', '6']
            rollrigy = choice(rollrig)
            
            
            if int(rollrigy) == num:
                rollrig.remove(str(num))
                print(rollrig)
            if rand == num: 
                embed = discord.Embed(title=f"Good guess! The roll was {rollrig[0]}", colour=xz)
                await ctx.send(embed=embed)
                
            elif rand != num:
                embed = discord.Embed(title=f"Your guess was incorrect, the roll was {rollrigy}", colour=xz)
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

    

    @commands.command(aliases=['rock', 'rockpaperscissors'], help="Plays rock paper scissors with the bot `<choice>` must be rock, paper, or scissors")
    async def rps(self, ctx, roll):

        random_num = randint(0, 2)
        
        if roll not in ['rock', 'paper', 'scissors']:
            embed = discord.Embed(title="Thats not an option. Choose rock, paper, or scissors...", colour=xz)
            await ctx.send(embed=embed)
            
        if random_num == 0:
            cpu_choice = "rock"

        elif random_num == 1:
            cpu_choice = "paper"
        elif random_num == 2:
            cpu_choice = "scissors"
        
        if roll == "rock":
            if cpu_choice == "rock":
                embed = discord.Embed(title="You drew", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you drew", colour=xz)
                embed.set_author(name="Rock paper scissors")
                
                await ctx.send(embed=embed)
            elif cpu_choice == "paper":
                embed = discord.Embed(title="You lost", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you lost", colour=xz)
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)
            
            elif cpu_choice == "scissors":
                embed = discord.Embed(title="You won", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you won", colour=xz)
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)        

        if roll == "paper":
            if cpu_choice == "paper":
                embed = discord.Embed(title="Drew", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you drew", colour=xz)
                embed.set_author(name="Rock paper scissors")
                
                await ctx.send(embed=embed)
            
            elif cpu_choice == "scissors":
                embed = discord.Embed(title="You lost", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you lost", colour=xz)
                embed.set_author(name="Rock paper scissors")
    
                await ctx.send(embed=embed)
            
            elif cpu_choice == "rock":
                embed = discord.Embed(title="You won", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you won", colour=xz)
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)        
            
        if roll == "scissors":
            if cpu_choice == "scissors":
                embed = discord.Embed(title="You drew", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you drew", colour=xz)
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)
            elif cpu_choice == "rock":
                embed = discord.Embed(title="You lost", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you lost", colour=xz)
                embed.set_author(name="Rock paper scissors")
            
                await ctx.send(embed=embed)
            
            elif cpu_choice == "paper":
                embed = discord.Embed(title="You won", description = f"You picked {roll}, bot picked {cpu_choice}, therefore you won", colour=xz)
                embed.set_author(name="Rock paper scissors")
                await ctx.send(embed=embed)

        
    @commands.command(aliases=['rpsbait', 'rpsbaits', 'RPSB', 'RockPaperScissorsBait'], help="Emits a fake rock paper scissors game with a bot")
    async def rpsfail(self, ctx):
        embed = discord.Embed(title=f"Rock paper scissors!", colour=xz)
        msg = await ctx.send(embed=embed)
        
        await msg.add_reaction("\U0001f4bf")
    
        await msg.add_reaction('\U0001f4f0')
        await msg.add_reaction('\U00002702')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '\U0001f4bf'

        reaction, user = await self.self.client.wait_for('reaction_add', check=check)
        await msg.delete()
        embed = discord.Embed(title=f"Baited", colour=xz)
        await ctx.send(embed=embed)

  
   
    @commands.command(aliases=['gussing', 'Guessing', 'Guessing_game','gg'], help="Plays a guessinggame with the bot (bot thinks of a number)")
    async def guessinggame(self, ctx):
        rand = randint(1, 100)
        embed = discord.Embed(title=f"Give me a number between 1-100, the game has started'", colour=xz)
        await ctx.send(embed=embed)
        
        
        
        try:
            received_msg = int((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=10)).content)
            while received_msg != rand:
                
                
                if received_msg > rand:
                    embed = discord.Embed(title="Lower", colour=xz)
                    await ctx.send(embed=embed)
                    
                    
                elif received_msg < rand:
                    embed = discord.Embed(title="Higher", colour=xz)
                    await ctx.send(embed=embed)
                elif str(received_msg) == "q":
                    embed = discord.Embed(title="Goodbye", colour=xz)
                    return await ctx.send(embed=embed)
                received_msg = int((await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=10)).content)
            else:
                embed = discord.Embed(title=f"Correct! The answer was {rand}", colour=xz)
                return await ctx.send(embed=embed)
                
                
        except asyncio.TimeoutError:
            embed = discord.Embed(title="I gave up waiting", colour=xz)
            await ctx.send(embed=embed)
    
def setup(client):
  client.add_cog(Games(client))

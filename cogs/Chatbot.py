import discord
from discord.ext import commands

class Chatbot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    

def setup(bot):
    bot.add_cog(Chatbot(bot))
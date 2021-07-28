import discord, os, requests, json, asyncio
from discord.ext import commands 
from core.utils.utils import thecolor, Json, thebed
from core.Context import Context



class Feedback(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command()
    async def feedback(self, ctx:Context, *, feedback):

        with open('./dicts/Feedback.json', 'r+') as k:
            data = json.load(k)
            data['feedback']['message'].append(feedback)
            data['feedback']['author'].append(ctx.author.name)
            Json(k, data)

            await thebed(ctx, '', 'Sent!')

    @commands.command()
    async def viewfeedback(self, ctx:Context, distance:int=0):
        with open('./dicts/Feedback.json', 'r+') as k:
            data = json.load(k)
            await thebed(ctx, 'Feedback', f'*`{distance}`*: "{data["feedback"]["message"][distance]}", submitted by **{data["feedback"]["author"][distance]}**')

    @commands.command(aliases=['dial', 'call', 'assistance'])
    async def support(self, ctx:Context):
        f = open('./dicts/Dial.json', 'r+')
        data = json.load(f)
        if str(ctx.channel.id) in data:
            return await thebed(ctx, '', 'This is already engaged in a support dial!')
        data[str(ctx.channel.id)] = True
        Json(f, data)
        chan = self.bot.get_channel(866598271991545886)
        await thebed(ctx, '', 'You are now connected to **JesterBot offical Support Dial**. Type `j.closesupport` to end your ticket')
        await thebed(chan, '', f'You are now connected to **{ctx.author}** in **{ctx.guild}** with channel id of **{ctx.channel.id}**')
        await chan.send(f"<@521226389559443461> - <@298043305927639041>")

    @commands.command(aliases=['closedial', 'endsupport', 'enddial', 'dialend', 'hangup'])
    async def closesupport(self, ctx:Context, chan=""):
        c = self.bot.get_channel(866598271991545886)
        f = open('./dicts/Dial.json', 'r+')
        data = json.load(f)
        if chan:
            if ctx.author.id in [521226389559443461, 298043305927639041]:
                
                
                if chan in data:
                    del data[chan]
                    Json(f, data)
                    return await ctx.send('**Ended**')
        if str(ctx.channel.id) not in data:
            return await thebed(ctx, '', 'You are not engaged in a support dial!')
        del data[str(ctx.channel.id)]
        Json(f, data)
        await thebed(ctx, '', 'The ticket has been closed! We hope your problem got solved!')
        await thebed(c, '', f'{ctx.author} ended a call at {ctx.channel.id}')

    @commands.Cog.listener('on_message')
    async def dial(self, message):
        if message.author == self.bot.user:
            return
        f = open('./dicts/Dial.json', 'r+')
        data = json.load(f)
        chan = self.bot.get_channel(866598271991545886)
        if message.channel == chan:
            for k in data:
                newchan = self.bot.get_channel(int(k))
                return await newchan.send(f"**{message.author}:** {message.content}")
        if str(message.channel.id) in data:
            return await chan.send(f"**{message.author}:** {message.content}")

def setup(bot):
  bot.add_cog(Feedback(bot))

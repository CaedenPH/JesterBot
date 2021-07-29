import json, asyncio, traceback
import discord
from discord.ext.commands import *

from core.utils.utils import thecolor, thebed, Json

async def unexpected(bot, ctx, error):
    k = open('./dicts/Errors.json', 'r+')
    data = json.load(k) 
    num = str(len(data))
    
    data[num] = {'author': ctx.author.name, 'id': ctx.author.id, 'error': str(error), 'error_dir': str(dir(error)), 'command': ctx.command.name}
    Json(k, data)
    await thebed(bot.chan, f'{ctx.guild}; {ctx.author}; {ctx.command.name}', error)
    await ctx.error(bot, error=error)
async def error_handler(bot, ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(description="You do not have permissions to do that!", colour=thecolor())
        await ctx.send(embed=embed)
    elif isinstance(error, AttributeError):
        pass
    elif isinstance(error, CheckFailure):
        pass
    
    elif isinstance(error, MissingRequiredArgument):
        com = str(ctx.command.signature)
        x = com.split(f"{error.param.name}")
        y = " "
        z = "  "
        for k in str(ctx.command):
            z += " "
        for e in error.param.name:
            y += "^"
        
        
        for k in range(0, len(x[0])):
            z += " "
        
        embed = discord.Embed(title=f"<{error.param.name}>  is missing:", description=f"```j.{ctx.command} {ctx.command.signature}\n{z}{y}```", colour=thecolor())
        embed.set_footer(text="<> = needed │ [] = not needed")
        await ctx.send(embed=embed)

    elif isinstance(error, CommandNotFound):
        if bot.hiber:
            return
        with open('./dicts/Suggest.json') as l:
            data = json.load(l)
            if str(ctx.channel.id) in data and data[str(ctx.channel.id)]['Yes'] == True:
                return   
        try:
            y = []
            content = ctx.message.content
            content_replace = content.replace(ctx.prefix, '')
        
            for cmd in bot.commands:
        
                if  cmd.name[:1] == content_replace[:1]:
                    
                    if cmd.hidden:
                        pass
                    else:

                        if len(y) == 5:
                            y.append(f"`{cmd.name}`---")
                        else:
                            y.append(f"`{cmd.name}`")
            my_string = ""
            n = 0
            for string in y:
            
                my_string += f" \n - {str(string)}"
        
            
            num = 1
            my_string = my_string.split("---")

        
            embed = discord.Embed(title="Error!", colour=thecolor())
            embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
            
            if my_string[0] not in [""]:

                embed.add_field(name="Did you mean:", value=f"{my_string[0]}")
                
            msg = await ctx.send(embed=embed)
            def check(e, u):
                return u == ctx.author and e.message.id==msg.id

                
            if len(my_string) >= 2:
                if my_string[1] != "":

                    await msg.add_reaction("⬅")
                    await msg.add_reaction("➡")
                    await msg.add_reaction("⛔")
                    try:
                        emoji, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        
                        
                        while emoji.emoji != "⛔":
                            if emoji.emoji == "➡" and num == 1:
                        
                                embed = discord.Embed(title="Error!", colour=thecolor())
                                embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                embed.add_field(name="Did you mean:", value=f"{my_string[1]}")
                                embed.set_footer(text="Page 2")
                                await msg.edit(embed=embed)
                                await msg.remove_reaction(member=ctx.author, emoji="➡")
                                num = 2

                            elif emoji.emoji == "⬅" and num == 2:
                                embed = discord.Embed(title="Error!", colour=thecolor())
                                embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                embed.add_field(name="Did you mean:", value=f"{my_string[0]}")
                                embed.set_footer(text="Page 1")
                                await msg.edit(embed=embed)
                                await msg.remove_reaction(member=ctx.author, emoji="⬅")
                                num = 1
                            else:
                                await msg.remove_reaction(member=ctx.author, emoji="➡")
                                await msg.remove_reaction(member=ctx.author, emoji="⬅")

                            emoji, user = await bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author)
                        else:
                            embed = discord.Embed(title="Error!", description="Goodbye", colour=thecolor())
                            embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                            embed.set_footer(text="Have fun!")
                            return await msg.edit(embed=embed)
                            
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title="Error!", description="Session timed out", colour=thecolor())
                        embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                        embed.set_footer(text="Have fun!")
                        return await msg.edit(embed=embed)
            
        except:
            pass
    elif isinstance(error, MemberNotFound):
        embed = discord.Embed(description=f"They are not a **member!**", colour=thecolor())
        await ctx.send(embed=embed)
    elif isinstance(error, RoleNotFound):
        embed = discord.Embed(description=f"That is not a **role!**", colour=thecolor())
        await ctx.send(embed=embed)
    
    elif isinstance(error, CommandOnCooldown):
        embed = discord.Embed(description=f'This command is on cooldown for **{error.retry_after:.2f}** seconds', colour=thecolor())
        await ctx.send(embed=embed)
    
    elif isinstance(error,CommandInvokeError):
        if error.args[0] == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions':

            await ctx.em('You unfortunately did not invite my bot with enough permissions for me to complete this action!')
        else:
            await unexpected(bot, ctx, error)
        
    else:
        await unexpected(bot, ctx, error)
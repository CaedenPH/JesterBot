import json, asyncio, traceback
import disnake
from disnake.ext.commands import *

from core.utils.utils import thecolor, thebed, Json
from core.utils.emojis import LOCATIONemojis
from core.Paginator import Paginator

async def unexpected(bot, ctx, error):
    k = open('./dicts/Errors.json', 'r+')
    data = json.load(k) 
    num = str(len(data))
    
    data[num] = {'author': ctx.author.name, 'id': ctx.author.id, 'error': str(error), 'error_dir': str(dir(error)), 'command': ctx.command.name}
    Json(k, data)
    await thebed(bot.chan, f'{ctx.guild}; {ctx.author}; {ctx.command.name}', error)
    e = "".join(traceback.format_exception(error, error, error.__traceback__))
    y = Paginator(ctx)
    await y.paginate(content=f"{e}", name='error')
async def error_handler(bot, ctx, error):
    if isinstance(error, MissingPermissions):
        embed = disnake.Embed(description="You do not have permissions to do that!", colour=thecolor())
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
        
        await thebed(ctx, f"<{error.param.name}> is missing:", f"```j.{ctx.command} {ctx.command.signature}\n{z}{y}```", f="<> = needed | [] = not needed")

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

            failed_cmd = ctx.message.content.split(' ')
            failed_cmd = failed_cmd[0]
            embed = disnake.Embed(title="Error!", colour=thecolor())
            embed.set_author(icon_url=ctx.author.avatar.url, name=f"{failed_cmd} is not a command!")
            
            if my_string[0] not in [""]:

                embed.add_field(name="Did you mean:", value=f"{my_string[0]}")
                
            msg = await ctx.send(embed=embed)
            def check(e, u):
                return u == ctx.author and e.message.id==msg.id

            left = LOCATIONemojis['backwards']
            right = LOCATIONemojis['forwards']
            close = LOCATIONemojis['close']
            if len(my_string) >= 2:
                if my_string[1] != "":

                    await msg.add_reaction(left)
                    await msg.add_reaction(close)
                    await msg.add_reaction(right)
                    try:
                        emoji, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        
                        
                        while str(emoji.emoji) != close:
                            if str(emoji.emoji) == right and num == 1:
                        
                                embed = disnake.Embed(title="Error!", colour=thecolor())
                                embed.set_author(icon_url=ctx.author.avatar.url, name=f"{failed_cmd} is not a command!")
                                embed.add_field(name="Did you mean:", value=f"{my_string[1]}")
                                embed.set_footer(text="Page 2")
                                await msg.edit(embed=embed)
                                await msg.remove_reaction(member=ctx.author, emoji=right)
                                num = 2

                            elif str(emoji.emoji) == left and num == 2:
                                embed = disnake.Embed(title="Error!", colour=thecolor())
                                embed.set_author(icon_url=ctx.author.avatar.url, name=f"{failed_cmd} is not a command!")
                                embed.add_field(name="Did you mean:", value=f"{my_string[0]}")
                                embed.set_footer(text="Page 1")
                                await msg.edit(embed=embed)
                                await msg.remove_reaction(member=ctx.author, emoji=left)
                                num = 1
                            else:
                                await msg.remove_reaction(member=ctx.author, emoji=right)
                                await msg.remove_reaction(member=ctx.author, emoji=left)

                            emoji, user = await bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author)
                        else:
                            embed = disnake.Embed(title="Error!", description="Goodbye", colour=thecolor())
                            embed.set_author(icon_url=ctx.author.avatar.url, name=f"{failed_cmd} is not a command!")
                            embed.set_footer(text="Have fun!")
                            return await msg.edit(embed=embed)
                            
                    except asyncio.TimeoutError:
                        embed = disnake.Embed(title="Error!", description="Session timed out", colour=thecolor())
                        embed.set_author(icon_url=ctx.author.avatar.url, name=f"{failed_cmd} is not a command!")
                        embed.set_footer()
                        return await msg.edit(embed=embed)
            
        except Exception as e:
            print(e)
    elif isinstance(error, MemberNotFound):
        embed = disnake.Embed(description=f"They are not a **member!**", colour=thecolor())
        await ctx.send(embed=embed)
    elif isinstance(error, RoleNotFound):
        embed = disnake.Embed(description=f"That is not a **role!**", colour=thecolor())
        await ctx.send(embed=embed)
    
    elif isinstance(error, CommandOnCooldown):
        embed = disnake.Embed(description=f'This command is on cooldown for **{error.retry_after:.2f}** seconds', colour=thecolor())
        await ctx.send(embed=embed)
    
    elif isinstance(error,CommandInvokeError):
        if error.args[0] == 'Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions':

            await ctx.em('You unfortunately did not invite my bot with enough permissions for me to complete this action!')
        else:
            await unexpected(bot, ctx, error)
        
    else:
        await unexpected(bot, ctx, error)

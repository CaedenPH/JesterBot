import discord
import json

from core.utils.utils import thebed, thecolor, Json
from core.utils.comedy import fact, quote, joke, pickup



async def run_check(bot, ctx):

    if bot.hiber and ctx.command.name not in ['hiber', 'close']:
	    return False
    try:
        ra = ctx.guild.id
    except:
        return await ctx.em('Commands dont work in DMs! My prefix is `j.`, or you can ping me in a guild!') 
    
    if ctx.command.cog:
        if ctx.command.cog.qualified_name == "Staff" and ctx.author.id not in [298043305927639041]:
            return False          
    x = False
    with open('./dicts/Check.json') as k:
        data = json.load(k)
       
        if str(ctx.author.id) in data:
            
            if ctx.command.name in data[str(ctx.author.id)]['commands']:
                await ctx.em('you cant run this command for some reason, possibly blacklisted')
                return False
            else:
                x = True
        else:
            x = True

    if x:
        
        with open('./dicts/Suggest.json') as k:
            newdata = json.load(k)
        
            if str(ctx.channel.id) in newdata:
                if newdata[str(ctx.channel.id)]['Yes']:
                    return False
                else:
                    return True

            else:
                return True




async def run_precheck(bot, message):
    with open('./dicts/Suggest.json') as k:
        data = json.load(k)
        
        if str(message.channel.id) in data:
            if data[str(message.channel.id)]['Yes']:
                for item in ('suggest', 'sug'):
                    if item in message.content:

                        try:
                                        
                            embed = discord.Embed(description="Suggestion", colour=thecolor())
                            embed1 = discord.Embed(description=f"What is the title of your suggestion? Type end at any point to stop and type title to remove the description", colour=thecolor())
                            x = await message.author.send(embed=embed1)
                            received_msg = str((await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == message.author and m.channel == message.channel)).content).lower()
                            if received_msg not in ["end", "title"]:
                                msg1 = received_msg
                                embed2 = discord.Embed(description=f"What is the description of your suggestion? Type end at any point to stop", colour=thecolor())
                                y = await message.author.send(embed=embed2)
                                received_msg1 = str((await bot.wait_for('message', timeout=90.0, check=lambda m: m.author == message.author and m.channel == message.channel)).content).lower()
                                if received_msg1 != "end":
                                    msg2 = received_msg1
                                    embed.add_field(name="Title", value=msg1, inline=False)
                                    embed.add_field(name="Description", value=msg2, inline=False)
                                    embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
                                    await thebed(message.author, '', 'Completed!')
                                    
                                    msg = await message.channel.send(embed=embed)
                                    await msg.add_reaction("👍")
                                    await message.delete()
                                    return await msg.add_reaction("👎")
                                    
                                else:
                                    embed3 = discord.Embed(description="Goodbye", colour=thecolor())
                                   
                                    msg = await message.author.send(embed=embed3)
                                
                            elif received_msg == "end":
                                
                                embed3 = discord.Embed(description="Goodbye", colour=thecolor())
                                await message.delete()
                                return await message.author.send(embed=embed3)
                            else:
                                embed2 = discord.Embed(description=f"What is the Title of your suggestion? Type end at any point to stop", colour=thecolor())
                                y = await message.author.send(embed=embed2)
                                received_msg1 = str((await bot.wait_for('message', timeout=90.0, check=lambda m: m.author == message.author and m.channel == message.channel)).content).lower()
                                if received_msg1 != "end":

                                    embed.add_field(name="Title", value=received_msg1, inline=False)
                                    
                                    embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
                                    
                                    
                                    msg = await message.channel.send(embed=embed)
                                    await thebed(message.author, '', 'Completed!')
                                    await msg.add_reaction("👍")
                                    await message.delete()
                                    return await msg.add_reaction("👎")
                        except Exception as e:
                            print(e)
                        
                        
                    else:
                        if message.author.id != 828363172717133874:

                            await bot.wait_until_ready()
                            try:
                                await message.delete()
                            except:
                                pass





async def run_channel_send(bot):
     with open('./dicts/ConfigChannel.json') as k:
        data = json.load(k)
        for k in data:
            if k not in "emojis":
                for e in data[k]:
                    try:
                        await bot.wait_until_ready()
                        t = bot.get_channel(int(data[k][e])) 
                        if e == "factchannel":
                            send = fact()
                        elif e == "jokechannel":
                            send = joke()
                        elif e == "pickuplinechannel":
                            send = await pickup()
                        elif e == "quotechannel":
                            send = quote()
                        await t.send(embed=send)
                    except:
                        continue




async def run_executed(bot, ctx):

    await bot.wait_until_ready()
    user = bot.get_user(298043305927639041)
    if ctx.author.id != 298043305927639041:
        await user.send(f"Name:{ctx.author.name} \nGuild:{ctx.guild}  \nCommand:{ctx.command.name} \nChannel:{ctx.channel.name}")
    
    if ctx.command.name == "color":
        for cog in tuple(bot.extensions):
            
                bot.reload_extension(cog)
   
    with open('./dicts/Selfscore.json', 'r+') as k:
        loaded1 = json.load(k)
        if str(ctx.author.id) in loaded1:
            pass
        else:
            loaded1[str(ctx.author.id)] = {
            "Name":    ctx.author.name,
            "Guild":    ctx.guild.name,
            "selfscore":  0,

        }

            Json(k, loaded1)

    with open('./dicts/Scoreoverall.json', 'r+') as x:
        data = json.load(x)
        data["Score"]["Score1"] += 1
        Json(x, data)

    with open('./dicts/Selfscore.json', 'r+') as f:
        data = json.load(f)
        
        if str(ctx.author.id) in data:
            data[str(ctx.author.id)]['selfscore'] += 1
            Json(f, data)

    with open('./dicts/Commandsused.json') as y:
        data = json.load(y)
        if str(ctx.command) not in data:
            data[str(ctx.command)] = {
                'score': 1
            } 
            
            with open('./dicts/Commandsused.json', 'r+') as y:
                Json(y, data)
        else:
            
            with open('./dicts/Commandsused.json', 'r+') as y:
                data[str(ctx.command)]['score'] += 1
                Json(y, data)
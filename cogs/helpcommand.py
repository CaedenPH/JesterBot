import discord, json, asyncio, random, requests
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from dutils import thecolor, Json, thebed
from dislash import SlashClient, ActionRow, Button


class THEACTUALHelp(commands.Cog):
    def __init__(self, client):

        self.client = client
   
           

    @commands.command(aliases=['h', 'commands', 'cmd', 'command', '?', 'helpme', 'helpcommand', 'cmds'])
    async def help(self, ctx, command=""):
          
        client_av = self.client.get_user(828363172717133874)
        
        command1 = self.client.get_command(command)
        
        with open('./dicts/Emoji.json') as k:
            data = json.load(k)
            if command == "JesterStaff":
                the_list1 = ""
                if ctx.author.id == 298043305927639041:
                
                    num = 0
                    
                    
                    for cog in self.client.cogs:
                        cog = self.client.get_cog(cog)
                        for cmd in cog.walk_commands():
                            if cmd.hidden:
                                if num % 2 == 0:
                                    
                                    the_list1 += f"\n - `{cmd}`  │"
                                else:
                                    the_list1 += f"`{cmd}`"
                                num += 1
                    
                    
                    embed = discord.Embed(title=cog.qualified_name, description=f"I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `^help <command>`. To get a more detailed description of a cog, type `^help <Category>` , but make sure you capitlize the name of the category\n{the_list1}", colour=thecolor())
                    embed.set_author(name="Help", icon_url = client_av.avatar_url)
                    embed.add_field(name="Links:", value= "[Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?self.client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)")
                    return await ctx.send(embed=embed)

            cog = self.client.get_cog(command)
            if cog:
                the_list = ""
                num = 0
                
                for cmd in cog.walk_commands():
                    if not cmd.hidden:  
                        if num % 2 == 0:
                            
                            the_list += f"\n - `{cmd}`  │"
                        else:
                            the_list += f"`{cmd}`"
                        num += 1
                
                embed = discord.Embed(title=cog.qualified_name, description=f"I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `^help <command>`. To get a more detailed description of a cog, type `^help <Category>` , but make sure you capitlize the name of the category\n{the_list}", colour=thecolor())
                embed.set_author(name="Help", icon_url = client_av.avatar_url)
                embed.add_field(name="Links:", value= "[Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?self.client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)")
                return await ctx.send(embed=embed)

            
            else:
                y = []
                if command1 == None and command:
                
                    for cmd in self.client.walk_commands():
                        
                        if cmd.name[:1] == command[:1]:
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

                    
                        n += 1
                    my_string = my_string.split("---")
                    num = 1
                    embed = discord.Embed(title="Error!", colour=thecolor())
                    embed.set_author(icon_url=ctx.author.avatar_url, name=f"{command} is not a command!")
                    
        
                    if my_string[0] not in [""]:

                        embed.add_field(name="Did you mean:", value=f"{my_string[0]}")
            
                    def check(e, u):
                        return u == ctx.author and e.message.id==msg.id
                    
                    msg = await ctx.send(embed=embed)
                
                    if len(my_string) >= 2:
                        if my_string[1] != "":

                            await msg.add_reaction("⬅")
                            await msg.add_reaction("➡")
                            await msg.add_reaction("⛔")
                            try:
                                emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                                
                                
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

                                    emoji, user = await self.client.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author)
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

                    
                elif command1 == None and not command:
                    us = ctx.guild.get_member(828363172717133874)
                    if us.guild_permissions.manage_messages:
                        ddata = {
                            'JesterInfo': 863075610048987166,
                            'Feedback': 863075610851147777,
                            'Music': 863075611320647719,
                            'Snipe': 863075611269791794,
                            'Fun': 863075609781075968,
                            'Mod': 863075610784301068,
                            'Games': 863075611329167380,
                            'Utils': 863075611161788478,
                            'Images': 863075611277656124,
                            'Economy': 863075610913800233,
                            'Misc': 863075610979729409,
                            'Levels': 863075611182628895,
                            'Config': 863075611169259550,
                            'Love': 863075611374125056,
                            'JesterJokes': 863075611278704670

                    



                        }
                        
                        close = "<:Cross:863313854069997578>"
                        home = "<:Arrow:863313854040506379>"
                        
                        row_1 = ActionRow()
                        row_2 = ActionRow()
                        row_3 = ActionRow()
                        row_4 = ActionRow()
                        row_4.add_button(emoji=close, custom_id='close', style=ButtonStyle.green)
                        row_4.add_button(emoji=home, custom_id='home', style=ButtonStyle.green)
                        z = 0
                        y = 0
                        desc1 = ""
                        desc2 = ""
                        desc3 = ""
                        for t in self.client.cogs:
                            if t not in ["Event", "THEACTUALHelp"]:
                                name = self.client.get_emoji(ddata[t]).name
                                emoj = f"<:{name}:{ddata[t]}>"
                                
                                
                                emoj1 = data['emojis'][t]['description']
                                #em.add_field(name=f"{t} │ {emoj}", value=f"React with the {emoj} to view {t} commands")
                                
                                    
                                y += 1
                                if z < 5:
                                    desc1 += f"\n{emoj} │ {t}"
                                    row_1.add_button(emoji=emoj, custom_id=t, style=ButtonStyle.grey)
                                elif z < 10 and z >= 5:
                                    desc2 += f"\n{emoj} │ {t}"
                                    row_2.add_button(emoji=emoj, custom_id=t, style=ButtonStyle.grey)
                                else:
                                    desc3 += f"\n{emoj} │ {t}"
                                    row_3.add_button(emoji=emoj, custom_id=t, style=ButtonStyle.grey)


                                z += 1
                        

                        e = self.client.get_emoji(863313854150606848)
                        j = self.client.get_emoji(863313855286607932)
                        s = self.client.get_emoji(863313855061164062)
                        r = self.client.get_emoji(863313855119360022)
                        t = self.client.get_emoji(863313855399329812)
                        links = "[Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?self.client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)"
                        em = discord.Embed(title=f"{j}{e}{s}{t}{e}{r}", description=f"{links}", colour=thecolor())
                        em.set_thumbnail(url=self.client.user.avatar_url)
                        #\u200b\n
                        # em.add_field(value="\u200b", name=desc1)
                        # em.add_field(value="\u200b", name=desc2)
                        # em.add_field(value="\u200b", name=desc3)
                        em.add_field(name="\u200b", value=f"{desc1}\u200b\n")
                        em.add_field(name="\u200b", value=f"{desc2}\u200b\n")
                        em.add_field(name="\u200b",value =f"{desc3}\u200b\n")
                        
                        
                        #em.add_field(name="\u200b", value=links, inline=False)
                        em.add_field(value="```yaml\nTo get a more detailed description of a command use ^help <command/Category>. Press the button to see the category.``` ```ini\n[To give feedback, use the feedback command]```", name="\u200b")
                        
                        em.set_footer(text="<> - Required Parameters │ [] - Optional Parameters")
                        msg = await ctx.send(embed=em, components=[row_1, row_2, row_3, row_4])
                        
                        def check(inter):
                            return inter.message.id == msg.id and inter.author == ctx.author
                        inter = await ctx.wait_for_button_click(check)
                
                        while inter.clicked_button != "eejekedjedemkemek":
                            the_list1 = ""
                            if inter.clicked_button.custom_id == "close":
                                response = requests.get('https://official-joke-api.appspot.com/random_joke')
                                fox = response.json()
                                foxupdate = (fox["setup"]) 
                                foxupdatey = (fox["punchline"])
                                
                                theembed = discord.Embed(title=f"{j}{e}{s}{t}{e}{r}", description="```yaml\nGoodbye```", color=thecolor())
                                
                                await inter.reply(type=4, embed=theembed)
                            elif inter.clicked_button.custom_id == "home":
                                
                               
                                await inter.reply(type=7, embed=em)
                        
                            else:

                                for cog in self.client.cogs:
                                    if cog not in ["Event", "THEACTUALHelp"]:

                                            
                                        if cog == inter.clicked_button.custom_id:
                                            name = self.client.get_emoji(ddata[cog]).name
                                            emoj = f"<:{name}:{ddata[cog]}>"
                                            the_list3 = ""
                                            the_list4 = ""
                                            if cog == "Mod":
                                                num = 0
                                                the_list3 = "\n-`permmute/unmute`\n-`ban/unban`"
                                                the_list4 = "\n-`mute/reactmute`\n-`permreactmute/unreactmute`"
                                                
                                                dcog1 = self.client.get_cog(cog)
                                                for cmd in dcog1.walk_commands():
                                                    if not cmd.hidden:
                                                        if cmd.name not in ['permmute', 'unmute', 'permreactmute', 'unreactmute', 'mute', 'reactmute', 'ban', 'unban']:

                                                            if num % 2 == 0:
                                                                
                                                                the_list3 += f"\n- `{cmd}`"
                                                            else:
                                                                the_list4 += f"\n- `{cmd}`"
                                                            num += 1
                                                
                                                #, description=f"*{data['emojis'][cog]['description']}*\n{the_list1}"
                                                embed = discord.Embed(title=f"{cog} │ {emoj}", color=thecolor())
                                                embed.add_field(value=the_list3, name="\u200b")
                                                embed.add_field(value=the_list4, name="\u200b")
                                                
                                                await inter.reply(type=7, embed=embed)
                                            
                                            elif cog == "Economy":
                                                the_list1 = ""
                                                
                                                num = 0
                                                
                                                
                                                cog1 = self.client.get_cog(cog)
                                                for cmd in cog1.walk_commands():
                                                    if not cmd.hidden:
                                                        if " " not in cmd.qualified_name:
                                                            if num % 2 == 0:
                                                                
                                                                the_list3 += f"\n- `{cmd}`"
                                                            else:
                                                                the_list4 += f"\n- `{cmd}`"
                                                            num += 1
                                                
                                                        
                                                
                                                #escription=f"*{data['emojis'][cog]['description']}*\n{the_list1}", 
                                                embed = discord.Embed(title=f"{cog} │ {emoj}",color=thecolor())
                                                embed.add_field(value=the_list3, name="\u200b")
                                                embed.add_field(value=the_list4, name="\u200b")
                                                await inter.reply(type=7, embed=embed)

                                            else:
                                                the_list = ""
                                                num = 0
                                                actualcog = self.client.get_cog(cog)
                                                for cmd in actualcog.walk_commands():
                                                    if not cmd.hidden:  
                                                        if num % 2 == 0:
                                                            
                                                            the_list3 += f"\n- `{cmd}`"
                                                        else:
                                                            the_list4 += f"\n- `{cmd}`"
                                                        num += 1
                                                #, description=f"*{data['emojis'][cog]['description']}*\n{the_list}"
                                                embed = discord.Embed(title=f"{cog} │ {emoj}", color=thecolor())
                                                embed.add_field(value=the_list3, name="\u200b")
                                                embed.add_field(value=the_list4, name="\u200b")
                                                await inter.reply(type=7, embed=embed)
                            
                            inter = await ctx.wait_for_button_click(check)
                    else:
                        the_list = []
                        em = discord.Embed(description="**I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `^help <command>`.**\nLinks:  [Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?self.client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)", colour=thecolor())
                        em.set_author(name="Help", icon_url = client_av.avatar_url)
                        for cog in self.client.cogs:
                            
                            if cog not in ['Event',  'THEACTUALHelp']:
                                
                                thecog = self.client.get_cog(cog)
                                for cmd in thecog.walk_commands():
                                    if not cmd.hidden:

                                        the_list.append(f"`{cmd}`")
                            
                                em.add_field(name=cog, value="│".join(the_list), inline=False)
                                the_list = []
                        em.add_field(name="Help command", value="The help command looks bad because the main help command requires the `discord.Permission` `manage_messages`... This is because it uses emojis to control it")
                        await ctx.send(embed=em)

                elif command1 != None and command:
                    alx = []
                    
                    sig = command1.signature   
                    thehelp = command1.help
                    alias = command1.aliases
                    if alias:
                        
                        for al in command1.aliases:

                            alx.append(f"`{al}`")
                    client_av = self.client.get_user(828363172717133874)
                    em = discord.Embed(colour=thecolor())
                    name = f"{command1.name.capitalize()}"
                    
                    em.add_field(name="Name", value=f"`{name}`", inline=False)
                    em.add_field(name="Alias", value=f"{', '.join(alx)} " if alias else f"`none`", inline=False)
                    em.add_field(name="Usage", value=f"`^{command1.name} {sig}`" if sig else f'`^{command1.name}`', inline=False)
                    em.add_field(name="Description", value=thehelp if thehelp else "Currently no help!", inline=False)
                    em.set_author(name="Help", icon_url = client_av.avatar_url)
                    em.set_footer(text="<> = needed │ [] = not needed")
                    await ctx.send(embed=em)

         
def setup(client):
  client.add_cog(THEACTUALHelp(client))

import discord, json, asyncio, random, requests
from discord.ext import commands

from core.utils.utils import thecolor, Json, thebed, Cmds
from core.utils.emojis import j, e, s, t, e, r, COGemojis, CATEGORIES, LINK, HOME
from core.Context import Context

from dislash import SlashClient, ActionRow, Button, SelectMenu, SelectOption, MenuOption


class THEACTUALHelp(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command(
        
        aliases=['h', 'commands', 'cmd', 'command', '?', 'helpme', 'helpcommand', 'cmds']
        
        )

    async def help(self, ctx:Context, command=""):
        
        bot_av = self.bot.get_user(828363172717133874)
        
        command1 = self.bot.get_command(command)
        
        with open('./dicts/Emoji.json') as k:
            data = json.load(k)

            cog = self.bot.get_cog(command)

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
                
                embed = discord.Embed(title=cog.qualified_name, description=f"I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `j.help <command>`. To get a more detailed description of a cog, type `j.help <Category>` , but make sure you capitlize the name of the category\n{the_list}", colour=thecolor())
                embed.set_author(name="Help", icon_url = bot_av.avatar_url)
                embed.add_field(name="Links:", value= "[Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?self.bot_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)")
                return await ctx.send(embed=embed)

            
            else:

                

                if not command1 and command:

                    y = []

                    for cmd in self.bot.walk_commands():
                        
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
                                emoji, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                                
                                
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

                                    emoji, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == ctx.author)
                                else:
                                    return await msg.delete()
                                    
                            except asyncio.TimeoutError:
                                embed = discord.Embed(title="Error!", description="Session timed out", colour=thecolor())
                                embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.message.content} is not a command!")
                                embed.set_footer(text="Have fun!")
                                return await msg.edit(embed=embed)

                    
                elif not command1 and not command:
                    us = ctx.me
                    #if us.guild_permissions.manage_messages:

                    desc1 = ""
                    desc2 = ""
                    desc3 = ""

                    
                    opt = SelectMenu(
                            custom_id="test",
                            placeholder=f"Choose a category",
                            max_values=1,
                            options=[
                                MenuOption("home", "r", "Go back to the main help panel", emoji=HOME),
                            ]
                        )
                    z = 0

                    for cog in self.bot.cogs:
                        
                        if cog not in ["Event", "THEACTUALHelp", "Staff", "Jishaku"]:
                            
                            try:
                                name = self.bot.get_emoji(COGemojis[cog]).name
                            except:
                                print(cog)
                            emoj = f"<:{name}:{COGemojis[cog]}>"
                            
                            
                            emoj1 = data['emojis'][cog]['description']
                            
                            cg = self.bot.get_cog(cog)
                            te = 0
                            for cmd in cg.walk_commands():
                                if not cmd.hidden:

                                    te += 1
                            
                            if z % 2 == 0:
                                desc1 += f"\n> {emoj} \u200b **{cog}**"
                                opt.add_option(f"{cog}", f"{emoj} {cog}", f"{cog} has {te} commands", emoji=emoj)
                            
                            else:
                                desc2 += f"\n> {emoj}  \u200b **{cog}**"
                                opt.add_option(f"{cog}", f"{emoj} {cog}", f"{cog} has {te} commands", emoji=emoj)

                            z += 1
                    
                    
                    links = "> [Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?client_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot) │ [Vote for me!](https://top.gg/bot/828363172717133874/vote)"
                    description = f'''\n
                    
                    ```ml\n[] - Required Argument | <> - Optional Argument``````diff\n+ Use the dropbar to navigate through Categories``````diff\n+ Use {ctx.prefix}help prefix for info about the prefix```
                    
                    
                    
                    '''
                    #description=f"{description}",
                    em = discord.Embed(title=f"{j}{e}{s}{t}{e}{r}", description=description, colour=thecolor())
                    #em.set_thumbnail(url=self.bot.user.avatar_url```yaml\nTo get a more detailed description of a command use j.help <command/Category>. Press the button to see the category.```)
                    #u200b\n
                    em.add_field(name=f"{CATEGORIES} **Categories:**\n\u200b", value=f"{desc1}\n\u200b")
                    em.add_field(name="\u200b\n\u200b", value=f"{desc2}")
                    #em.add_field(name="\u200b",value =f"{desc3}\u200b\n")
                    #diff, fix  
                    em.add_field(name=f"{LINK} **Links:**", value=f"**{links}**", inline=False)
                    
                    #em.add_field(value=f"""```yaml\nTo get a more detailed description of a command use j.help     command/Category>. Press the button to see the category.``` ```ini\n[If you require assistance use the support command. To understand the prefixes type {ctx.prefix}help prefix]```""", name="\u200b", inline=False)
                    em.set_footer(text=f"{str(ctx.message.created_at)[11:16]} • Expires in 5 minutes")
                    
                    msg = await ctx.send(embed=em, components=[opt])

                    the_list1 = ""
                    def check(inter):

                        return inter.message.id == msg.id
                    
                    try:
                        inter = await msg.wait_for_dropdown(check, timeout=360)

                        while inter.select_menu != "eejekedjedemkemek":

                            if inter.select_menu.selected_options[0].label == "home":
                                if inter.author == ctx.author:

                                    await inter.reply(type=7, embed=em)
                                else:
                                    await inter.reply(type=4, embed=em, ephemeral=True)

                            for cog in self.bot.cogs:

                                if cog not in ["Event", "THEACTUALHelp", "Staff", "Jishaku"]:
                                        
                                    if cog == inter.select_menu.selected_options[0].label:
                                        name = self.bot.get_emoji(COGemojis[cog]).name
                                        emoj = f"<:{name}:{COGemojis[cog]}>"
                                        the_list3 = ""
                                        the_list4 = ""
                                        if cog == "Mod":
                                            num = 0
                                            the_list3 = "\n-`permmute/unmute`\n-`ban/unban`"
                                            the_list4 = "\n-`mute/reactmute`\n-`permreactmute/unreactmute`"
                                            
                                            dcog1 = self.bot.get_cog(cog)
                                            for cmd in dcog1.walk_commands():
                                                if not cmd.hidden:
                                                    if cmd.name not in ['permmute', 'unmute', 'permreactmute', 'unreactmute', 'mute', 'reactmute', 'ban', 'unban']:

                                                        if num % 2 == 0:
                                                            
                                                            the_list3 += f"\n- `{cmd}`"
                                                        else:
                                                            the_list4 += f"\n- `{cmd}`"
                                                        num += 1
                                            
                                            
                                            embed = discord.Embed(title=f"{cog} │ {emoj}", description=data['emojis'][cog]['description'], color=thecolor())
                                            embed.add_field(value=the_list3, name="\u200b")
                                            embed.add_field(value=the_list4, name="\u200b")
                                            if inter.author == ctx.author:

                                                await inter.reply(type=7, embed=embed)
                                            else:
                                                await inter.reply(type=4, embed=embed, ephemeral=True)

                                        else:
                                            the_list = ""
                                            the_list5 = ""
                                            num = 1
                                            actualcog = self.bot.get_cog(cog)
                                            for cmd in actualcog.walk_commands():
                                                if not cmd.hidden: 
                                                    if not " " in cmd.qualified_name:

                                                        if num % 2 == 0:
                                                            
                                                            the_list4 += f"\n- `{cmd}`"
                                                        else:
                                                            if num % 3 == 0:
                                                                the_list5 += f"\n - `{cmd}`"
                                                                
                                                            else:

                                                                the_list3 += f"\n- `{cmd}`"
                                                        num += 1
                                                        if num == 4:
                                                            num = 1
                                                        
                                            desc = data['emojis'][cog]['description']
                                            embed = discord.Embed(title=f"{cog} │ {emoj}", description=desc, color=thecolor())
                                            embed.add_field(value=the_list3, name="\u200b")
                                            embed.add_field(value=the_list4, name="\u200b")
                                            if the_list5:

                                                embed.add_field(name="\u200b", value=the_list5)
                                            if inter.author == ctx.author:

                                                await inter.reply(type=7, embed=embed)
                                            else:
                                                await inter.reply(type=4, embed=embed, ephemeral=True)
                                
                            inter = await msg.wait_for_dropdown(check)
                    except asyncio.TimeoutError:
                        em.set_footer(text="Help timed out")
                        await msg.edit(embed=em, components=[])
                    # else:

                    #     the_list = []
                    #     em = discord.Embed(description="**I'm a multi-use bot with new features being created every week! \nTo get a more detailed description of a command use `j.help <command>`.**\nLinks:  [Official server](https://discord.gg/2654CuU3ZU) │ [Bot invite](https://discord.com/oauth2/authorize?self.bot_id=828363172717133874&scope=bot&permissions=8589934591) │ [Website](https://sites.google.com/view/jesterbot)", colour=thecolor())
                    #     em.set_author(name="Help", icon_url = bot_av.avatar_url)
                    #     for cog in self.bot.cogs:
                            
                    #         if cog not in ["Event", "THEACTUALHelp", "Staff", "Jishaku"]:
                                
                    #             thecog = self.bot.get_cog(cog)
                    #             for cmd in thecog.walk_commands():
                    #                 if not cmd.hidden:

                    #                     the_list.append(f"`{cmd}`")
                            
                    #             em.add_field(name=cog, value="│".join(the_list), inline=False)
                    #             the_list = []
                    #     em.add_field(name="Help command", value="The help command looks bad because the main help command requires the `discord.Permission` `manage_messages`... This is because it uses emojis to control it")
                    #     await ctx.send(embed=em)

                elif command1 != None and command:
                    alx = []
                    
                    sig = command1.signature   
                    thehelp = Cmds(command1.name).chelp
                    alias = command1.aliases
                    if alias:
                        
                        for al in command1.aliases:

                            alx.append(f"`{al}`")
                    bot_av = self.bot.get_user(828363172717133874)
                    em = discord.Embed(colour=thecolor())
                    name = f"{command1.name.capitalize()}"
                    
                    em.add_field(name=" ❯❯ Name", value=f"`{name}`", inline=False)
                    em.add_field(name=" ❯❯ Alias", value=f"{', '.join(alx)} " if alias else f"`none`", inline=False)
                    em.add_field(name=" ❯❯ Usage", value=f"`j.{command1.name} {sig}`" if sig else f'`j.{command1.name}`', inline=False)
                    em.add_field(name=" ❯❯ Description", value=thehelp if thehelp else "Currently no help!", inline=False)
                    em.set_author(name="Help", icon_url = bot_av.avatar_url)
                    em.set_footer(text="<> = needed │ [] = not needed")
                    await ctx.send(embed=em)

def setup(bot):
  bot.add_cog(THEACTUALHelp(bot))

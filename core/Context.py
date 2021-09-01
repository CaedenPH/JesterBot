from discord.errors import HTTPException
from core.utils.emojis import CLOSE, HOME, TRASHCAN
import discord, asyncio
from discord.ext import commands
from dislash import *

from core.utils.utils import thecolor, thebed


def Components():
    components = [
            ActionRow(Button(
                style=ButtonStyle.green,
                label="Yes",
                custom_id="Yes"
            ),
            Button(
                style=ButtonStyle.red,
                label="No", 
                custom_id="No"

            ))
            ]
    return components

class Context(commands.Context):

    async def em(self, message):
        return await self.send(
            embed = discord.Embed(
                description=message,
                color=thecolor() 
            )
        )

    async def send(self, content: any = None, **kwargs):
        perms = self.channel.permissions_for(self.me)
        if not perms.send_messages:
            try:
                await self.author.send(
                    "I can't send any messages in that channel. \nPlease give me sufficient permissions to do so."
                )
            except discord.Forbidden:
                pass
            return

        require_embed_perms = kwargs.pop("embed_perms", False)
        if require_embed_perms and not perms.embed_links:
            kwargs = {}
            content = (
                "Oops! I need **Embed Links** permission to work properly. \n"
                "Please tell a server admin to grant me that permission."
            )
        if isinstance(content, discord.Embed):
            kwargs["embed"] = content
            content = None
        if isinstance(content, discord.File):
            kwargs["file"] = content
            content = None
        
        msg = await super().send(content, **kwargs)
        self.bot.data[self.message] = {'bot':msg}
        try:
            async def reaction_task(msg, arg, kwargs):
                def check(r, u):
                    return r.message == msg and u == arg.author
                
                    
                await asyncio.sleep(3)
                try:
                    
                    await msg.add_reaction(TRASHCAN)
                except Exception as a:
                    return

                try:
                    r, u = await arg.bot.wait_for('reaction_add', check=check, timeout=250)
                    if str(r.emoji.id) == TRASHCAN[11:-1]:
                        await msg.delete()
                except Exception as b:
                    try:
                        await msg.clear_reactions()
                    except Exception as c:
                        pass
         

            loop = asyncio.get_running_loop()   
            loop.create_task(reaction_task(msg, self, kwargs))
        except:
            pass
        return msg

    async def confirm(self, content: any = None, **kwargs):
        
        components=Components()
        msg = await super().send(content, **kwargs, components=components)

        def check(inter):
            return inter.author == self.author and inter.message.id == msg.id
        
        inter = await msg.wait_for_button_click(check)
        if inter.clicked_button.custom_id == "Yes":
            await inter.respond(type=6)
            return True
        else:

            await inter.reply('Not sent', type=7)
            return False

    async def error(self, bot, **kwargs):
        async with self.typing():
            error = kwargs.get('error')

            await self.message.add_reaction(CLOSE)

            components=Components()

        msg = await super().send(components=components, embed=discord.Embed(description=f"**Error:**{error}\n\u200b\n**Would you like to submit this error to the developer?**", color=thecolor()).set_author(name="Error", icon_url=self.author.avatar_url).set_footer(text='This error command is slow because it takes a lot of time to process it!'))
        x = False
        inter = await msg.wait_for_button_click(check)
        if inter.clicked_button.custom_id == "Yes":
            await inter.reply('Sent', type=4, ephemeral=True)
            x = True
        else:
            await inter.reply('Not sent!', type=4, ephemeral=True)
            x =  False
        if x:
            await thebed(bot.dev, f"{error} - {self.author} - {self.guild} - {self.channel}")
    async def expected_error(self, **kwargs):
        async with self.typing():
            error = kwargs.get('error')

            await self.message.add_reaction(CLOSE)


        msg = await super().send(embed=discord.Embed(description=f"**Error: **{error}"))
       

        
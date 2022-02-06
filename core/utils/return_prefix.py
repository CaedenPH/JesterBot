from disnake import Embed, Message
from .utils import thecolor
from core.utils.comedy import joke


async def create_embed(message: Message, bot) -> Embed:
    avatar = message.guild.get_member(bot.user.id).avatar.url
    prefix = await bot.get_prefix(message)

    embed = Embed(
        title=f"Hello {message.author.name}",
        description=f"""
    │ My default prefix is: `j.` │
    │ My prefix for you is: {', '.join([f"`{k}`" for k in prefix if not k.startswith('<@')])} │ 
    │ Type `j.prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
    """,
        colour=thecolor(),
    )
    embed.set_author(name="JesterBot", icon_url=avatar)
    embed.add_field(
        name="Also here is a joke for you:", value=f"│ {await joke()} │", inline=False
    )
    embed.set_footer(text="You can get more of these jokes with j.joke!")
    return embed

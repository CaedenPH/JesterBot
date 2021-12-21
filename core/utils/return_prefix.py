import discord
from .utils import thecolor
from core.utils.comedy import joke

async def create_embed(message, bot) -> discord.Embed:
    avatar = message.guild.get_member(bot.user.id).avatar_url

    x = []    
    prefix = await bot.get_prefix(message)
    for pref in [prefix1 for prefix1 in prefix if not prefix1.startswith('<@')]:
        x.append(f"`{pref}`")

    embed = discord.Embed(title=f"Hello {message.author.name}", description=f"""
    │ My default prefix is: `j.` │
    │ My prefix for you is: {', '.join(x)} │ 
    │ Type `j.prefix <prefix> [prefix], [prefix], etc` to change the prefix for you! │
    """, colour=thecolor())
    embed.set_author(name="JesterBot", icon_url=avatar)
    embed.add_field(name="Also here is a joke for you:", value=f"│ {await joke()} │", inline=False)
    embed.set_footer(text="You can get more of these jokes with j.joke!")

    return embed
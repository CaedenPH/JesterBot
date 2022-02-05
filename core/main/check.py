import disnake
import json

from core.utils.utils import thebed, thecolor, Json
from core.utils.comedy import fact, quote, joke, pickup


async def suggest(bot, message):
    message_id = message.id
    data = {}
    embed = (
        disnake.Embed(color=thecolor())
        .set_author(name=message.author.name, icon_url=message.author.avatar.url)
        .set_footer(
            text=str(message.created_at)[11:16]
            + " • This suggestion was created by {}".format(message.author.name)
        )
    )

    def check(m):
        return m.author == message.author and isinstance(
            m.channel, disnake.channel.DMChannel
        )

    for a in [
        "What would you like the title to be? Type q at any point to end",
        "What would you like the description to be? Type q at any point to end",
    ]:
        await thebed(message.author, "", a)

        received_msg = await bot.wait_for("message", check=check)

        if received_msg.content.lower() == "q":
            return await received_msg.add_reaction("\u274c")

        await received_msg.add_reaction("\u2705")

        data[a] = received_msg.content

    for b in data:
        name = b.split(" ")

        embed.add_field(name=f"**{name[5]}**", value=data[b], inline=False)
    msg = await message.channel.send(embed=embed)

    await msg.add_reaction("\U0001f44d")
    await msg.add_reaction("\U0001f44e")

    newmsg = await message.channel.fetch_message(message_id)

    return await newmsg.delete()


async def run_check(bot, ctx):

    if bot.hiber and ctx.command.name not in ["hiber", "close"]:
        return False
    try:
        ra = ctx.guild.id
    except:
        await ctx.em(
            "Commands dont work in DMs! My prefix is `j.`, or you can ping me in a guild!"
        )
        return False

    if ctx.command.hidden:
        y = await bot.is_owner(ctx.author)
        if not y:
            await ctx.em(
                "You cannot run this command, it is a `hidden` command which only bot admins can run."
            )
            return False
        return True
    x = False
    with open("./dicts/Check.json") as k:
        data = json.load(k)

        if str(ctx.author.id) in data:

            if ctx.command.name in data[str(ctx.author.id)]["commands"]:
                await ctx.em(
                    "you cant run this command for some reason, possibly blacklisted"
                )
                return False
            else:
                x = True
        else:
            x = True

    if x:

        with open("./dicts/Suggest.json") as k:
            newdata = json.load(k)

            if str(ctx.channel.id) in newdata:
                if newdata[str(ctx.channel.id)]["Yes"]:
                    return False
                return True
            return True


async def run_precheck(bot, message):
    with open("./dicts/Suggest.json") as k:
        data = json.load(k)

        if str(message.channel.id) in data:
            if data[str(message.channel.id)]["Yes"]:
                for item in ("suggest", "sug"):
                    if item in message.content:
                        return await suggest(bot, message)

                if message.author.id != 828363172717133874:
                    await bot.wait_until_ready()
                    try:
                        await message.delete()
                    except:
                        pass


async def run_channel_send(bot) -> None:
    await bot.wait_until_ready()

    with open("./dicts/ConfigChannel.json") as k:
        data = json.load(k)

    for guild_id in data:
        if guild_id in "emojis":
            continue
        for _type in data[guild_id]:
            try:
                channel_id = data[guild_id][_type]
                channel = bot.get_channel(channel_id)
                if not channel:
                    try:
                        channel = await bot.fetch_channel(channel_id)
                    except disnake.HTTPException:
                        continue

                if _type == "factchannel":
                    embed = fact()
                elif _type == "jokechannel":
                    embed = disnake.Embed(
                        title="Joke", description=await joke(), colour=thecolor()
                    )
                elif _type == "pickuplinechannel":
                    embed = await pickup(bot)
                elif _type == "quotechannel":
                    embed = await quote(bot)
                await channel.send(embed=embed)
            except Exception as e:
                pass


async def run_executed(ctx) -> None:
    bot = ctx.bot

    if ctx.author.id != 298043305927639041:
        user = await bot.fetch_user(298043305927639041)
        await user.send(
            f"Name:{ctx.author.name} \nGuild:{ctx.guild}  \nCommand:{ctx.command.name} \nChannel:{ctx.channel.name}"
        )

    if ctx.command.name == "color":
        for cog in tuple(bot.extensions):
            bot.reload_extension(cog)

    with open("./dicts/Selfscore.json", "r+") as k:
        loaded1 = json.load(k)
        if str(ctx.author.id) not in loaded1:
            loaded1[str(ctx.author.id)] = {
                "Name": ctx.author.name,
                "Guild": ctx.guild.name,
                "selfscore": 0,
            }
            Json(k, loaded1)

    with open("./dicts/Scoreoverall.json", "r+") as x:
        data = json.load(x)
        data["Score"]["Score1"] += 1
        Json(x, data)

    with open("./dicts/Selfscore.json", "r+") as f:
        data = json.load(f)

        if str(ctx.author.id) in data:
            data[str(ctx.author.id)]["selfscore"] += 1
            Json(f, data)

    with open("./dicts/Commandsused.json") as y:
        data = json.load(y)
        if str(ctx.command) not in data:
            data[str(ctx.command)] = {"score": 1}
            with open("./dicts/Commandsused.json", "r+") as y:
                Json(y, data)
        else:

            with open("./dicts/Commandsused.json", "r+") as y:
                data[str(ctx.command)]["score"] += 1
                Json(y, data)

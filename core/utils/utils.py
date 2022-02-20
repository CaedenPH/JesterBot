import disnake
import json


def update_json(_file, _data: str) -> None:
    """Update file to match data"""

    _file.truncate(0)
    _file.seek(0)
    _file.write(json.dumps(_data, indent=4))


def get_colour() -> int:
    with open("./dicts/Color.json") as fp:
        data = json.load(fp)

    colour = data["colour"]
    return int(colour, 16)


async def send_embed(
    channel: disnake.abc.Messageable, title: str, description: str = disnake.Embed.Empty, **kwargs
) -> disnake.Message:
    from core.context import Context

    author = kwargs.get("a")
    icon_url = kwargs.get("i_u")
    footer = kwargs.get("f")
    thumbnail = kwargs.get("t")
    image = kwargs.get("i")

    embed = disnake.Embed(title=title, description=description, colour=get_colour())
    if footer:
        embed.set_footer(text=footer)
    if author:
        embed.set_author(name=author)
        if icon_url:
            embed.set_author(name=author, icon_url=icon_url)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)

    if isinstance(channel, Context):
        embed.timestamp = channel.message.created_at
        msg = await channel.reply(embed=embed)
    else:
        msg = await channel.send(embed=embed)
    return msg

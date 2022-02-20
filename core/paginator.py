import disnake

from core.utils import get_colour
from core.constants import LOCATION_EMOJIS as l


async def message_edit(embed, **kwargs):
    content = kwargs.get("content")
    message = kwargs.get("message")
    current = kwargs.get("current")
    top = kwargs.get("top")
    embed.description = content
    embed.set_footer(text=f"{str(message.created_at)[11:16]} • Page: {current} / {top}")
    await message.edit(embed=embed)


class Paginator:
    def __init__(self, context) -> None:
        self._pages = {}
        self._current = 0
        self.ctx = context
        self._top = 0

    @property
    async def pages(self):
        return self._pages

    async def paginate(self, **kwargs):
        content = kwargs.get("content")
        name = kwargs.get("name")
        icon_url = kwargs.get("icon_url")
        result = []
        for i in range(0, len(content), 2000):
            result.append(content[i : i + 2000])
        self._pages["0"] = {"content": result[0]}
        self._top = len(result) - 1

        embed = (
            disnake.Embed(colour=get_colour())
            .set_author(name=name, icon_url=icon_url if icon_url else self.ctx.author.avatar.url)
            .set_footer(text=f"{str(self.ctx.message.created_at)[11:16]} • Page: {self._current} / {self._top}")
        )
        embed.description = "```yaml\n{}```".format(self._pages[str(self._current)]["content"])
        msg = await self.ctx.reply(embed=embed)
        if len(result) == 1:
            return

        for pagenum, page in enumerate(result[1:], start=1):
            self._pages[str(pagenum)] = {"content": page}

        for k in l:
            await msg.add_reaction(l[k])

        def check(e, u):
            return u == self.ctx.author and e.message == msg

        e, u = await self.ctx.bot.wait_for("reaction_add", check=check)

        while str(e.emoji) != l["close"]:
            name = str(e.emoji)

            if name == l["fastbackwards"]:
                self._current = 0
            elif name == l["backwards"]:
                if self._current > 0:
                    self._current -= 1
            elif name == l["forwards"]:
                if self._current < self._top:
                    self._current += 1
            elif name == l["fastforwards"]:
                self._current = self._top

            await msg.remove_reaction(member=self.ctx.author, emoji=e.emoji)
            await message_edit(
                embed,
                message=msg,
                content="```yaml\n{}```".format(self._pages[str(self._current)]["content"]),
                current=self._current,
                top=self._top,
            )

            e, u = await self.ctx.bot.wait_for("reaction_add", check=check)

        else:
            return await msg.clear_reactions()

    async def edit(self, **kwargs):
        pass

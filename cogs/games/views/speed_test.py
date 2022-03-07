import asyncio
import typing as t

from essential_generators import DocumentGenerator

from disnake import Member, SelectOption, Message, MessageInteraction, HTTPException, Embed, ButtonStyle
from disnake.ui import View, Button, Select, Item, select, button

from core.constants import CHECKERED_FLAG, PLAY_BUTTON, SPEEDTEST_MESSAGE, STOPWATCH, THUMBS_UP, VIDEO_GAME
from core.context import Context


DIFFICULTY_CONVERTER = {
    "easy": 30,
    "medium": 60,
    "hard": 120,
    "insane": 180
} # difficulty to sentance length

class _SpeedTestView(View):
    """
    represent the speedtest view

    attributes
    ----------
    bot_message: Message
        the bot's original message that is 
        passed in ``after`` the instance is 
        initiated. Added to avoid having to
        use disnake's dodgy get_original_message
        method.
    """
    bot_message: Message

    def __init__(self, ctx: Context):
        super().__init__(timeout=720)

        self.ctx = ctx
        self.test_time = 30
        self.difficulty = "medium"
        self.clicked = False
        self._difficulty_converter = DIFFICULTY_CONVERTER

    async def exit(self) -> None:
        for child in self.children:
            if isinstance(child, (Button, Select)):
                child.disabled = True
        await self.edit_embed()

    async def on_timeout(self) -> None:
        await self.exit()

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        self.embed: Embed = self.bot_message.embeds[0] # cant assign anywhere else because bot_message is passed ** after ** the instance is created.

        return interaction.author == self.ctx.author and interaction.channel == self.ctx.channel

    async def edit_embed(self, desc: t.Optional[str] = None) -> None:
        """
        edit the bot message by
        changing description and
        view.

        params
        ------
        `desc: t.Optional[str]`
            the description to set to
            the embed, if None just change
            the message view.
        """

        if desc:
            self.embed.description = desc
        try:
            await self.bot_message.edit(embed=self.embed, view=self)
        except HTTPException:
            return

    def _get_sentence(self) -> str:
        temp_gen = DocumentGenerator()
        sentence = temp_gen.gen_sentence()

        return sentence

    @select(
        placeholder=f"Change difficulty {VIDEO_GAME}",
        options=[
            SelectOption(label="easy"),
            SelectOption(label="medium"),
            SelectOption(label="hard"),
            SelectOption(label="insane"),
        ],
    )
    async def change_difficulty(self, select: Select, interaction: MessageInteraction) -> None:
        """
        user changes the difficulty 
        to either easy, hard, medium 
        or insane which is then parsed
        by the bot.

        params
        ------
        select: Select
            the select option that was
            chosen by the user.
        interaction: MessageInteraction
            the interaction instance that
            was returned by the discord api.
        """

        self.difficulty = select.values[0]
        await interaction.response.defer()
        await self.edit_embed(
            "```yaml\n" + SPEEDTEST_MESSAGE.format(difficulty=self.difficulty, test_time=self.test_time) + "```"
        )


    @select(
        placeholder=f"Change test time {STOPWATCH}",
        options=[SelectOption(label="15"), SelectOption(label="30"), SelectOption(label="60"), SelectOption(label="120")],
    )
    async def change_test_time(self, select: Select, interaction: MessageInteraction) -> None:
        """
        user changes the test length
        to either 15s, 30s, 60s, or 120s.

        params
        ------
        select: Select
            the select option that was
            chosen by the user.
        interaction: MessageInteraction
            the interaction instance that
            was returned by the discord api.
        """

        self.test_time = int(select.values[0])
        await interaction.response.defer()
        await self.edit_embed(
            "```yaml\n" + SPEEDTEST_MESSAGE.format(difficulty=self.difficulty, test_time=self.test_time) + "```"
        )



class SpeedTest(_SpeedTestView):
    """
    represents the speedtest game.
    avoiding claustrophobia by packing
    a lengthy play func with useless
    select menus.
    """

    async def start_game(self, players: t.List[Member]) -> None:
        """
        starts the game which entails
        generating a sentence, showing 
        the sentence, waiting for users 
        to react (within the time frame)
        and then display statistics.
        """

        sentence = self._get_sentence()

        await self.edit_embed(sentence)
        await self.bot_message.reply("") 

    @button(label="Play", style=ButtonStyle.green, emoji=PLAY_BUTTON)
    async def play(self, button: Button, interaction: MessageInteraction) -> None:
        """
        user presses the play button
        to initiate the game stage and
        remove configuration buttons
        from the board.

        params
        ------
        button: Button
            the button that was pressed
            by the user.
        interaction: MessageInteraction
            the interaction instance that
            was returned by the discord api.
        """

        if self.clicked:
            return
        self.clicked = True

        def disable(c: Item) -> Item:
            c.disabled = True
            return c

        self.children = [disable(c) for c in self.children]

        _m = await self.bot_message.reply(f"{CHECKERED_FLAG} ** REACT TO PLAY ** {CHECKERED_FLAG}\nGame starting 30 seconds.")
        await _m.add_reaction(CHECKERED_FLAG)

        await interaction.response.defer()
        await self.edit_embed()
        await asyncio.sleep(30)

        m = self.ctx.bot.get_message(_m.id)
        players = [p for p in await [m for m in m.reactions if m.emoji == CHECKERED_FLAG][0].users().flatten() if not p.bot]
        if not players:
            return await self.bot_message.reply("**NO ONE REACTED**")

        await self.instigate_game(players)
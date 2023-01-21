import random
from typing import List, Union

from disnake import ButtonStyle, Embed, Message, MessageInteraction
from disnake.ui import Button, View, button

from core import Context
from core.constants import (
    BLACKJACK_HOW_TO, BOOM, CARD_SUITS, CLOSED_LOCK, CONFETTI, HANDSHAKE
)
from core.utils import get_colour

special_cards = {1: "Ace", 10: "Jack", 11: "Queen", 12: "King"}
blackjack_visual = """\
[ {player} hand: ]
{bar}------
{cards}
Hand value: {value}
"""


class Card:
    def __init__(self, *, suit: str, value: int):
        self._suit = suit + " " + CARD_SUITS[suit]
        self._name = (
            f"{special_cards[value] if value in special_cards else value} of {self._suit}"
        )
        self._value = value if value <= 10 else 10
        self._value = self._value if self._value != 1 else 1

    @property
    def name(self) -> str:
        return self._name

    @property
    def suit(self) -> str:
        return self._suit

    @property
    def value(self) -> int:
        return self._value

    def change_to(self, value: Union[str, int,]) -> None:
        self._value = int(value)


class BlackJack(View):
    bot_message: Message

    def __init__(self, ctx: Context) -> None:
        super().__init__()
        self.ctx = ctx

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        return (
            interaction.author == self.ctx.author
            and interaction.channel == self.ctx.channel
        )

    def lock_embed(self) -> None:
        for child in self.children:
            if not isinstance(child, Button):
                continue

            if child.style == ButtonStyle.green:
                child.disabled = True

    def get_aces(self, cards: List[Card]) -> List[Card]:
        return [card for card in cards if card.value == 1 or card.value == 11]

    def visual_hand(self, cards: List[Card] = None, hide_card: bool = False) -> str:
        visual_cards = "\n".join(
            [card.name for card in (cards if cards else self.user_cards)]
        )
        if hide_card:
            visual_cards = cards[0].name + f"\n? of {cards[1].suit}"

        player = "Bots" if cards else "Your"
        return blackjack_visual.format(
            player=player,
            bar="".join("-" for _ in range(len(player))),
            cards=visual_cards,
            value=self.generate_card_values(
                self.user_cards if not cards else self.bot_cards
            )
            if not hide_card
            else f"{cards[0].value} + ?",
        )

    def generate_card_values(self, cards: List[Card]) -> int:
        return sum([c.value for c in cards])

    def generate_card(self, bot: bool = False) -> Card:
        card = Card(
            suit=random.choice(list(CARD_SUITS.keys())), value=random.randint(1, 12)
        )
        if not bot:
            self.user_cards.append(card)
        elif bot:
            self.bot_cards.append(card)
        return card

    def generate_hand(self, bot: bool = False) -> List[Card]:
        if bot:
            self.bot_cards: List[Card] = []
        else:
            self.user_cards: List[Card] = []
        return [self.generate_card(bot) for _ in range(2)]

    def display_cards_embed(self, hide_card=True) -> Embed:
        return self.create_embed(
            description=self.visual_hand()
            + "\n"
            + self.visual_hand(self.bot_cards, hide_card=hide_card)
        )

    def create_embed(self, description: str, cards: List[Card] = None) -> Embed:
        return (
            Embed(
                title="Blackjack",
                description=f"```yaml\n{self.ctx.author.name}'s Blackjack Game\n================={''.join('=' for _ in range(len(self.ctx.author.name)))}\ngame status: {self.status}\n\n{description}```",
                timestamp=self.ctx.message.created_at,
                colour=get_colour(),
            )
            .set_author(name=self.ctx.author, icon_url=self.ctx.author.display_avatar)
            .set_footer(
                text=f"{'Hand value: ' + str(self.generate_card_values(cards or self.user_cards)) + ' • ' if getattr(self, 'status', None) == 'in progress' else ''} K, Q, J = 10  |  A = 1 or 11"
            )
        )

    @button(label="Stand", style=ButtonStyle.green, disabled=True)
    async def stand_button(self, button: Button, interaction: MessageInteraction):
        bot_aces = self.get_aces(self.bot_cards)
        user_worth = self.generate_card_values(self.user_cards)

        while (bot_worth := self.generate_card_values(self.bot_cards)) <= 12:
            if bot_aces:
                bot_aces[0].change_to(11)
            self.generate_card(bot=True)

        if bot_worth == user_worth:
            self.status = "You drew!"
        if bot_worth > user_worth:
            self.status = "You lost!"
        if bot_worth < user_worth:
            self.status = "You won!"
        embed = self.display_cards_embed(hide_card=False)
        self.lock_embed()

        conditions = {
            "You drew!": [
                HANDSHAKE,
                "https://tenor.com/view/predator-arnold-schwarzenegger-hand-shake-arms-gif-3468629",
            ],
            "You lost!": [
                BOOM,
                "https://tenor.com/view/diary-of-a-wimpy-kid-loser-bleh-tongue-out-gif-8481263",
            ],
            "You won!": [
                CONFETTI,
                "https://tenor.com/view/win-confetti-celebration-gif-7374480",
            ],
        }

        await interaction.response.send_message(
            self.status + f"\n{conditions[self.status][1]}"
        )
        await self.bot_message.add_reaction(conditions[self.status][0])
        await self.bot_message.edit(content=self.status, embed=embed, view=self)

    @button(label="Hit", style=ButtonStyle.green, disabled=True)
    async def hit_button(self, button: Button, interaction: MessageInteraction):
        await interaction.response.defer()
        card = self.generate_card()

        if self.generate_card_values(self.user_cards) > 21:
            self.status = "You lost"
            self.lock_embed()

            embed = self.display_cards_embed(hide_card=False)

            await self.bot_message.add_reaction(BOOM)
            return await self.bot_message.edit(
                content="You went over 21!", embed=embed, view=self
            )

        await self.bot_message.edit(
            content=f"You drew `{card.name}`", embed=self.display_cards_embed()
        )

    @button(label="Change ace value", style=ButtonStyle.green, disabled=True)
    async def change_ace_button(self, button: Button, interaction: MessageInteraction):
        aces = self.get_aces(self.user_cards)
        if not aces:
            await interaction.response.send_message(
                "You don't have any aces in Your hand", ephemeral=True
            )
        message = await interaction.response.send_message(
            "Would You like to change Your ace to a `1` or an `11`?"
        )

        num = 0
        msg: Message
        while (
            msg := await self.ctx.bot.wait_for(
                "message",
                check=lambda m: m.author == self.ctx.author
                and m.channel == self.ctx.channel,
            )
        ).content not in ["1", "11"]:
            if num == 3:
                return
            await message.edit(content="Send either `1` or  `11`.")
            num += 1

        if (
            msg.content == "11"
            and self.generate_card_values(self.user_cards) >= 11
            and aces[0].value != 11
        ):
            return await msg.reply(
                "You cannot change the value of this ace to `11` because You would go over 21."
            )

        original_value = aces[0].value
        aces[0].change_to(msg.content)

        await self.bot_message.edit(
            content=f"Changed ace from `{original_value}` to `{msg.content}`",
            embed=self.display_cards_embed(),
        )

    @button(label="How to play", style=ButtonStyle.blurple)
    async def how_to_play(self, button: Button, interaction: MessageInteraction):
        await interaction.response.defer()

        embed = Embed(
            title="Blackjack",
            description=BLACKJACK_HOW_TO,
            timestamp=self.ctx.message.created_at,
            colour=get_colour(),
        ).set_author(
            name=self.ctx.author.name, icon_url=self.ctx.author.display_avatar.url
        )

        await self.bot_message.edit(embed=embed)

    @button(label="Play", style=ButtonStyle.green, row=1)
    async def play_button(self, button: Button, interaction: MessageInteraction):
        await interaction.response.defer()
        await self.bot_message.clear_reactions()

        self.status = "in progress"
        for child in self.children:
            if not isinstance(child, Button):
                continue

            if child.disabled:
                child.disabled = False

            if child.label == "Play":
                child.style = ButtonStyle.danger
                child.label = "New game"

        self.generate_hand(bot=False)
        self.generate_hand(bot=True)

        await self.bot_message.edit(embed=self.display_cards_embed(), view=self)

    @button(label="Exit", style=ButtonStyle.danger, row=1)
    async def exit_button(self, button: Button, interaction: MessageInteraction):
        self.status = "game over"
        embed = self.display_cards_embed(hide_card=False)

        await self.bot_message.clear_reactions()
        await self.bot_message.add_reaction(CLOSED_LOCK)

        return await self.bot_message.edit(content="Game over", embed=embed, view=None)

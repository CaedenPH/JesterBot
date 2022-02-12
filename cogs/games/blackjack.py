import random

from typing import List
from disnake import MessageInteraction, Message, Embed, ButtonStyle
from disnake.ui import View, Button, button

from core import Context
from core.constants import CARD_SUITS

class Card:
    name: str
    suit: str
    value: int

    def __init__(
        self,
        *,
        suit: str,
        value: int
    ):
        self.name = f"{value} of {suit} {CARD_SUITS[suit]}"
        self.suit = suit
        self.face_value = value

class BlackJack(View):
    bot_message: Message

    def __init__(self, ctx: Context) -> None:
        super().__init__()

        self.ctx = ctx
        self.cards: List[Card]

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        return (
            interaction.author == self.ctx.author 
            and interaction.channel == self.ctx.channel
        )

    def generate_visual_cards(self) -> str:
        return """
        """
    def generate_card_values(self) -> int:
        return sum([c.value for c in self.cards])

    def generate_card(self, bot: bool = False) -> Card:
        card = Card(
            suit=random.choice(list(CARD_SUITS.keys())),
            value=random.randint(1, 11)
        )
        if not bot:
            self.cards.append(card)
        return card

    def generate_hand(self, bot: bool = False) -> List[Card]:
        return [
            self.generate_card() for _ in range(2)
        ]

    def create_embed(self, description: str) -> Embed:
        return Embed(
            title="Blackjack",
            description=f"```yaml\n{description}```",
            timestamp=self.ctx.message.created_at
        ).set_author(
            name=self.ctx.author,
            icon_url=self.ctx.author.display_avatar
        ).set_footer(
            text=f"Current card worth: {self.generate_card_values()}"
        )

    @button(label="Play", style=ButtonStyle.green)
    async def play_button(
        self, button: Button, interaction: MessageInteraction
    ):
        embed = self.create_embed(self.generate_visual_cards())
        self.children.index(button).hidden = True
        await self.bot_message.edit(
            embed=embed,
            view=self
        )

    @button(label="Hit", style=ButtonStyle.grey)
    async def hit_button(
        self, button: Button, interaction: MessageInteraction
    ):
        ...
    
    @button(label="Stand", style=ButtonStyle.grey)
    async def stand_button(
        self, button: Button, interaction: MessageInteraction
    ):  
        ...

    @button(label="Change ace value", style=ButtonStyle.grey)
    async def change_ace_button(
        self, button: Button, interaction: MessageInteraction
    ):  
        ...

    @button(label="Exit", style=ButtonStyle.danger)
    async def exit_button(
        self, button: Button, interaction: MessageInteraction
    ):
        ...
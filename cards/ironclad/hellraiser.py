"""
Ironclad Rare Power card - Hellraiser
"""

from typing import List

from actions.combat import ApplyPowerAction
from cards.base import Card
from entities.creature import Creature
from engine.runtime_api import add_actions
from utils.registry import register
from utils.types import CardType, RarityType


@register("card")
class Hellraiser(Card):
    """Whenever you draw a card containing Strike it is played against a random enemy."""

    card_type = CardType.POWER
    rarity = RarityType.RARE

    base_cost = 1

    def on_play(self, targets: List[Creature] = []):
        target = targets[0] if targets else None

        super().on_play(targets)

        add_actions(
            [
                ApplyPowerAction(
                    power="HellraiserPower",
                    target=target,
                    amount=0,
                    duration=-1,
                )
            ]
        )

        return

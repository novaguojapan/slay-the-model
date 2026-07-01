"""
Hellraiser power for Ironclad.
Whenever you draw a card containing "Strike", play it against a random enemy.
"""

from actions.combat import PlayCardAction
from engine.runtime_api import add_action
from powers.base import Power, StackType
from utils.registry import register


@register("power")
class HellraiserPower(Power):
    """Auto-play drawn cards whose name contains Strike."""

    name = "Hellraiser"
    description = (
        'Whenever you draw a card containing "Strike" it is played against a random enemy.'
    )
    stack_type = StackType.PRESENCE
    is_buff = True

    def __init__(self, amount: int = 0, duration: int = -1, owner=None):
        super().__init__(amount=amount, duration=duration, owner=owner)

    def on_card_draw(self, card):
        """Play drawn Strike-name cards for free against a random enemy."""
        if card is None:
            return

        card_names = [card.__class__.__name__]
        if hasattr(card, "display_name"):
            card_names.append(card.display_name.resolve())
        else:
            card_names.append(str(card))
        if not any("strike" in name.lower() for name in card_names):
            return

        add_action(PlayCardAction(card=card, is_auto=True, ignore_energy=True))
        return

"""
Hellraiser power for Ironclad.
Whenever you draw a card containing "Strike", it is played against a random enemy.
"""
from engine.runtime_api import add_action, add_actions
from typing import Any
from powers.base import Power, StackType
from actions.combat import PlayCardAction
from utils.registry import register


@register("power")
class HellraiserPower(Power):
    """Whenever you draw a card containing "Strike", it is played against a random enemy."""

    name = "Hellraiser"
    description = "Whenever you draw a card containing \"Strike\" it is played against a random enemy."
    stack_type = StackType.PRESENCE
    is_buff = True

    def __init__(self, amount: int = 1, duration: int = -1, owner=None):
        """
        Args:
            amount: Not used
            duration: -1 for permanent
        """
        super().__init__(amount=amount, duration=duration, owner=owner)

    def on_card_draw(self, card: Any):
        """Play the drawn card automatically if it contains "Strike" in its name."""
        # Check if the card name contains "Strike" case-insensitive
        card_name = ""
        
        # Try to get the name from display_name
        if hasattr(card, 'display_name'):
            try:
                card_name = card.display_name.resolve()
            except:
                pass
        
        # Fallback to class name
        if not card_name and hasattr(card, '__class__'):
            card_name = card.__class__.__name__
        
        if card_name and "strike" in card_name.lower():
            # Play the card automatically against a random enemy without expending energy
            add_actions([PlayCardAction(card=card, is_auto=True, ignore_energy=True)])
        
        return

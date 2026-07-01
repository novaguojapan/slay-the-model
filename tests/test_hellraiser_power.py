from actions.card import DrawCardsAction
from actions.combat import PlayCardAction
from cards.ironclad.hellraiser import Hellraiser
from cards.ironclad.pommel_strike import PommelStrike
from cards.ironclad.strike import Strike
from powers.definitions.hellraiser import HellraiserPower
from tests.test_combat_utils import create_test_helper
from utils.types import PilePosType


def test_hellraiser_card_applies_power():
    card = Hellraiser()

    assert card.cost == 1
    assert card.rarity.value == "Rare"
    assert card.card_type.value == "Power"

    card.upgrade()

    assert card.cost == 1
    assert card.display_name.resolve() == "Hellraiser+"
    assert card.description.resolve() == (
        "Whenever you draw a card containing “Strike” it is played against a random enemy."
    )


def test_hellraiser_power_queues_drawn_strike_for_free_auto_play():
    helper = create_test_helper()
    player = helper.create_player(energy=0)
    helper.start_combat([])

    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    drawn_strike = Strike()
    card_manager.add_to_pile(drawn_strike, "draw_pile", pos=PilePosType.TOP)

    player.add_power(HellraiserPower(owner=player))
    helper.game_state.action_queue.clear()

    DrawCardsAction(count=1).execute()

    queued = list(helper.game_state.action_queue.queue)
    assert len(queued) == 1
    play_action = queued[0]
    assert isinstance(play_action, PlayCardAction)
    assert play_action.card is drawn_strike
    assert play_action.is_auto is True
    assert play_action.ignore_energy is True


def test_hellraiser_matches_strike_case_insensitively_in_card_name():
    helper = create_test_helper()
    player = helper.create_player()
    power = HellraiserPower(owner=player)
    pommel_strike = PommelStrike()
    pommel_strike.display_name = pommel_strike.display_name.resolve().upper()

    helper.game_state.action_queue.clear()
    power.on_card_draw(pommel_strike)

    queued = list(helper.game_state.action_queue.queue)
    assert len(queued) == 1
    assert isinstance(queued[0], PlayCardAction)
    assert queued[0].card is pommel_strike
    assert queued[0].ignore_energy is True


def test_hellraiser_played_drawn_strike_does_not_spend_energy():
    from enemies.base import Enemy

    helper = create_test_helper()
    player = helper.create_player(energy=0)
    enemy = Enemy(max_hp=30, name="Cultist")
    helper.start_combat([enemy])

    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    drawn_strike = Strike()
    card_manager.add_to_pile(drawn_strike, "draw_pile", pos=PilePosType.TOP)
    player.add_power(HellraiserPower(owner=player))

    helper.game_state.action_queue.clear()
    DrawCardsAction(count=1).execute()
    helper.game_state.drive_actions()

    assert player.energy == 0
    assert enemy.hp == 24
    assert drawn_strike not in card_manager.get_pile("hand")
    assert drawn_strike in card_manager.get_pile("discard_pile")

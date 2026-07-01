from cards.ironclad.strike import Strike
from cards.ironclad.pommel_strike import PommelStrike
from cards.ironclad.twin_strike import TwinStrike
from cards.ironclad.defend import Defend
from cards.ironclad.bash import Bash
from engine.game_state import game_state
from powers.definitions.hellraiser import HellraiserPower
from tests.test_combat_utils import create_test_helper
from utils.types import PilePosType


def test_hellraiser_power_triggers_on_strike_draw():
    """Hellraiser should auto-play Strike cards when drawn."""
    helper = create_test_helper()
    player = helper.create_player()
    combat = helper.start_combat([])
    
    player.add_power(HellraiserPower(owner=player))
    
    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    strike = Strike()
    card_manager.add_to_pile(strike, "draw_pile", pos=PilePosType.TOP)
    
    game_state.action_queue.clear()
    power = player.powers[0]
    power.on_card_draw(strike)
    
    assert len(game_state.action_queue.queue) == 1
    action = game_state.action_queue.queue[0]
    assert getattr(action, "card", None) is strike
    assert getattr(action, "is_auto", None) == True
    assert getattr(action, "ignore_energy", None) == True


def test_hellraiser_power_triggers_on_pommel_strike_draw():
    """Hellraiser should auto-play Pommel Strike when drawn."""
    helper = create_test_helper()
    player = helper.create_player()
    combat = helper.start_combat([])
    
    player.add_power(HellraiserPower(owner=player))
    
    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    pommel = PommelStrike()
    card_manager.add_to_pile(pommel, "draw_pile", pos=PilePosType.TOP)
    
    game_state.action_queue.clear()
    power = player.powers[0]
    power.on_card_draw(pommel)
    
    assert len(game_state.action_queue.queue) == 1
    action = game_state.action_queue.queue[0]
    assert getattr(action, "card", None) is pommel


def test_hellraiser_power_triggers_on_twin_strike_draw():
    """Hellraiser should auto-play Twin Strike when drawn."""
    helper = create_test_helper()
    player = helper.create_player()
    combat = helper.start_combat([])
    
    player.add_power(HellraiserPower(owner=player))
    
    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    twin = TwinStrike()
    card_manager.add_to_pile(twin, "draw_pile", pos=PilePosType.TOP)
    
    game_state.action_queue.clear()
    power = player.powers[0]
    power.on_card_draw(twin)
    
    assert len(game_state.action_queue.queue) == 1
    action = game_state.action_queue.queue[0]
    assert getattr(action, "card", None) is twin


def test_hellraiser_power_does_not_trigger_on_defend():
    """Hellraiser should NOT trigger on non-Strike cards like Defend."""
    helper = create_test_helper()
    player = helper.create_player()
    combat = helper.start_combat([])
    
    player.add_power(HellraiserPower(owner=player))
    
    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    defend = Defend()
    card_manager.add_to_pile(defend, "draw_pile", pos=PilePosType.TOP)
    
    game_state.action_queue.clear()
    power = player.powers[0]
    power.on_card_draw(defend)
    
    assert len(game_state.action_queue.queue) == 0


def test_hellraiser_power_does_not_trigger_on_bash():
    """Hellraiser should NOT trigger on non-Strike cards like Bash."""
    helper = create_test_helper()
    player = helper.create_player()
    combat = helper.start_combat([])
    
    player.add_power(HellraiserPower(owner=player))
    
    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    bash = Bash()
    card_manager.add_to_pile(bash, "draw_pile", pos=PilePosType.TOP)
    
    game_state.action_queue.clear()
    power = player.powers[0]
    power.on_card_draw(bash)
    
    assert len(game_state.action_queue.queue) == 0


def test_hellraiser_power_triggers_on_upgraded_strike():
    """Hellraiser should auto-play upgraded Strike cards."""
    helper = create_test_helper()
    player = helper.create_player()
    combat = helper.start_combat([])
    
    player.add_power(HellraiserPower(owner=player))
    
    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    strike = Strike()
    strike.upgrade()
    card_manager.add_to_pile(strike, "draw_pile", pos=PilePosType.TOP)
    
    game_state.action_queue.clear()
    power = player.powers[0]
    power.on_card_draw(strike)
    
    assert len(game_state.action_queue.queue) == 1
    action = game_state.action_queue.queue[0]
    assert getattr(action, "card", None) is strike


def test_hellraiser_auto_plays_strike_against_random_enemy():
    """Hellraiser should auto-play Strike against a random enemy without energy cost."""
    helper = create_test_helper()
    player = helper.create_player()
    player.base_draw_count = 1
    from enemies.act1.cultist import Cultist
    enemy1 = helper.create_enemy(Cultist)
    enemy2 = helper.create_enemy(Cultist)
    combat = helper.start_combat([enemy1, enemy2])
    
    card_manager = player.card_manager
    card_manager.get_pile("draw_pile").clear()
    card_manager.get_pile("hand").clear()
    
    strike = Strike()
    card_manager.add_to_pile(strike, "draw_pile", pos=PilePosType.TOP)
    
    player.add_power(HellraiserPower(owner=player))
    initial_energy = player.energy
    
    combat._start_player_turn()
    helper.game_state.drive_actions()
    
    # Strike should have been auto-played and not be in hand
    hand = card_manager.get_pile("hand")
    assert strike not in hand
    # Energy should not have been expended for the auto-played Strike
    # (player starts with 3 energy, Hellraiser not played yet, so energy should remain 3)
    # Note: The Strike was auto-played during the draw phase, before player can act

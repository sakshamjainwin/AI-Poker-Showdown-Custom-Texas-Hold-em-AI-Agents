from pypokerengine.api.game import setup_config, start_poker
from examples.players.fish_player import FishPlayer
from examples.players.random_player import RandomPlayer
from examples.players.honest_player import HonestPlayer
from examples.players.CustomPlayerSaksham_1 import CustomPokerPlayer
from examples.players.CustomPlayerSaksham_2 import CustomPokerPlayer
from examples.players.CustomPlayerSaksham_3 import CustomPokerPlayer
from examples.players.CustomPlayerSaksham_4 import CustomPokerPlayer
from examples.players.CustomPlayerSaksham_5 import CustomPokerPlayer
from examples.players.CustomPlayerSaksham_6 import CustomPokerPlayer




config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=10)
config.register_player(name="CustomPlayerSaksham_1", algorithm=CustomPokerPlayer())
config.register_player(name="CustomPlayerSaksham_2", algorithm=CustomPokerPlayer())
config.register_player(name="CustomPlayerSaksham_3", algorithm=CustomPokerPlayer())
#config.register_player(name="CustomPlayerSaksham_4", algorithm=CustomPokerPlayer())
#config.register_player(name="CustomPlayerSaksham_5", algorithm=CustomPokerPlayer())
#config.register_player(name="CustomPlayerSaksham_6", algorithm=CustomPokerPlayer())

config.register_player(name="random_player", algorithm=RandomPlayer())
config.register_player(name="honest_player", algorithm=HonestPlayer())
game_result = start_poker(config, verbose=1)

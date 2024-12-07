from math import floor
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate , gen_cards

from pypokerengine.engine.hand_evaluator import HandEvaluator

class CustomPokerPlayer(BasePokerPlayer):

  def __init__(self):
    # put player name here before running game.py
    self.my_name = 'p4'
    self.initial_stack = None
    self.is_buff_last_round = None
    self.total_winnings = 0

  def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        commc = round_state["community_card"]
        self.get_stack = round_state['seats'][3]['stack']

        player_name = round_state['seats'][3]['name']

        for idx, player in enumerate(round_state["seats"]):
          if player["name"] == player_name:
            self.player_num = idx + 1  # Index starts from 0, so add 1 for player number
            break

        win_rate = estimate_hole_card_win_rate(
            nb_simulation=10000,
            nb_player=self.player_num,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(commc)
        )

        self.pos = win_rate * self.player_num

        rounds_left = 5-len(commc)
        hc_num = []
        hd = {
            'T': 10,
            'K': 13,
            'Q': 12,
            'J': 11
        }

        ssc = 0

        if (len(commc) == 0):
            for card in hole_card:
                if card[-1] == 'A':
                    hc_num.append(1)
                    hc_num.append(14)
                    continue
                elif card[-1] in hd:
                    hc_num.append(hd.get(card[-1].strip(), -1))
                else:
                    hc_num.append(int(card[-1]))

            if hole_card[0][1] == hole_card[1][1] or hole_card[0][0] == hole_card[1][0]:
              # needs changing
                if valid_actions[2]['amount']['min'] > self.get_stack * 0.6 and self.pos > 0.8:
                    self.fold_count = 0
                    return valid_actions[2]['action'], valid_actions[2]['amount']['min']

        else:
            nums = []
            for c in commc:
                if c[-1] == 'A':
                    nums.append(1)
                    nums.append(14)
                    continue

                if (hole_card[0][0] == hole_card[1][0]) and c[0] == hole_card[0][0]:
                    ssc += 1

                if c[-1] in hd:
                    nums.append(hd.get(c[-1], -1))
                else:
                    nums.append(int(c[-1]))

            nums.extend(hc_num)
            nums = sorted(nums)

            count = 1
            for i in range(len(nums) - 1):
                if nums[i + 1] == nums[i] + 1:
                    count += 1
                    # Needs Changing
                    if (count + rounds_left > 5 or ssc + rounds_left >= 5) and valid_actions[2]['amount']['min'] > self.get_stack * 0.6 and self.pos > 0.5:
                        self.fold_count = 0
                        return valid_actions[2]['action'], valid_actions[2]['amount']['min']
                else:
                    count = 1

        if valid_actions[1]['amount'] > 76:
            self.fold_count += 1
            if self.fold_count > 3 and self.pos > 1.25:
                self.fold_count = 0
                return valid_actions[1]['action'], valid_actions[1]['amount']
            return 'fold', 0

        self.fold_count = 0
        return valid_actions[1]['action'], valid_actions[1]['amount']

  def receive_game_start_message(self, game_info):
    #player_num = game_info["player_num"]

    # Placeholder Code
    initial_stack = game_info.get('initial_stack')

    # Use when p4 not defined in game.py
    #initial_stack = game_info['initial_stack']

    # err_msg = self.__build_err_msg("receive_game_start_message")
    # raise NotImplementedError(err_msg)

  def receive_round_start_message(self, round_count, hole_card, seats):
    round_count = round_count
    hole_card = hole_card

    # Placeholder code
    #for player in seats:
    #  if player.get('name') == 'p4':
    #    self.my_name == 'p4'
    #    break

    # Use when p4 not defined in game.py   
    #for player in seats:
    #  if player['name'] == self.name:
    #    self.my_name == player['name']
    #    break
        
    (f"New round {round_count}! My cards are {hole_card}")

    # err_msg = self.__build_err_msg("receive_round_start_message")
    # raise NotImplementedError(err_msg)

  def receive_street_start_message(self, street, round_state):
    street = round_state['street']
    (f"Street started: {street}")

    # err_msg = self.__build_err_msg("receive_street_start_message")
    # raise NotImplementedError(err_msg)

  def receive_game_update_message(self, new_action, round_state):
    #acting_player = new_action['player_uuid']
    #action_type = new_action['action']
    #action_amount = new_action.get('amount', 0)

    # err_msg = self.__build_err_msg("receive_game_update_message")
    # raise NotImplementedError(err_msg)
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    # winner_name = winners['name']
    winner_name = [winner["name"] for winner in winners]

    if self.my_name in winner_name:
      self.total_winnings += round_state["pot"]["main"]["amount"]

    # err_msg = self.__build_err_msg("receive_round_result_message")
    # raise NotImplementedError(err_msg)

  def set_uuid(self, uuid):
    self.uuid = uuid

  def respond_to_ask(self, message):
    """Called from Dealer when ask message received from RoundManager"""
    valid_actions, hole_card, round_state = self.__parse_ask_message(message)
    return self.declare_action(valid_actions, hole_card, round_state)

  def receive_notification(self, message):
    """Called from Dealer when notification received from RoundManager"""
    msg_type = message["message_type"]

    if msg_type == "game_start_message":
      info = self.__parse_game_start_message(message)
      self.receive_game_start_message(info)

    elif msg_type == "round_start_message":
      round_count, hole, seats = self.__parse_round_start_message(message)
      self.receive_round_start_message(round_count, hole, seats)

    elif msg_type == "street_start_message":
      street, state = self.__parse_street_start_message(message)
      self.receive_street_start_message(street, state)

    elif msg_type == "game_update_message":
      new_action, round_state = self.__parse_game_update_message(message)
      self.receive_game_update_message(new_action, round_state)

    elif msg_type == "round_result_message":
      winners, hand_info, state = self.__parse_round_result_message(message)
      self.receive_round_result_message(winners, hand_info, state)


  def __build_err_msg(self, msg):
    return "Your client does not implement [ {0} ] method".format(msg)

  def __parse_ask_message(self, message):
    hole_card = message["hole_card"]
    valid_actions = message["valid_actions"]
    round_state = message["round_state"]
    return valid_actions, hole_card, round_state

  def __parse_game_start_message(self, message):
    game_info = message["game_information"]
    return game_info

  def __parse_round_start_message(self, message):
    round_count = message["round_count"]
    seats = message["seats"]
    hole_card = message["hole_card"]
    return round_count, hole_card, seats

  def __parse_street_start_message(self, message):
    street = message["street"]
    round_state = message["round_state"]
    return street, round_state

  def __parse_game_update_message(self, message):
    new_action = message["action"]
    round_state = message["round_state"]
    return new_action, round_state

  def __parse_round_result_message(self, message):
    winners = message["winners"]
    hand_info = message["hand_info"]
    round_state = message["round_state"]
    return winners, hand_info, round_state

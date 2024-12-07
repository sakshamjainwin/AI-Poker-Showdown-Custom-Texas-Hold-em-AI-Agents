from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION = 1000

class CustomPokerPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        commc = round_state["community_card"]

        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
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


        for card in hole_card:
            if card[-1] == 'A':
                hc_num.append(1)
                hc_num.append(14)
                continue
            elif card[-1] in hd:
                hc_num.append(hd.get(card[-1].strip(), -1))
            else:
                hc_num.append(int(card[-1]))

        if len(commc) == 0 and hole_card[0][1] == hole_card[1][1] or hole_card[0][0] == hole_card[1][0]:
              # needs changing
            if valid_actions[1]['amount'] < 50 and self.pos > 0.8:
                self.fold_count = 0
                return valid_actions[2]['action'], valid_actions[2]['amount']['min']

        if len(commc) > 0:
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
                    if (count + rounds_left > 5 or ssc + rounds_left >= 5) and valid_actions[1]['amount'] <80 and self.pos > 0.5:
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
        self.player_num = game_info['player_num']
        self.init_stack = game_info['seats'][0]['stack']
        self.fold_count = 0

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


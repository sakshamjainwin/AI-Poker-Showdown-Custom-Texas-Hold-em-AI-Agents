from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import random



NB_SIMULATION = 1000

class CustomPokerPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
         #valid_actions format =>   {'action': 'fold', 'amount': 0},   {'action': 'call', 'amount': 0},  {'action': 'raise', 'amount': {'max': 95, 'min': 20}}
        print(hole_card)
        play_random = random.randint(0, 100)
        if play_random in (69, 76, 66, 16, 32, 18, 99, 7, 62, 19, 44, 11, 45):
            r = random.random()
            print("hum randi hai")
            if r < 0.3:
                return "call", valid_actions[1]["amount"]
            return "raise", random.randint(valid_actions[2]["amount"]["min"], valid_actions[2]["amount"]["min"]*4)
        
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
            if card[1] == 'A':
                hc_num.append(1)
                hc_num.append(14)
                continue
            elif card[1] in hd:
                hc_num.append(hd.get(card[1].strip()))   

            else:
                hc_num.append(int(card[1]))
        
                

        if hole_card[0][1] == hole_card[1][1] and len(commc) == 0: 
            if hole_card[0][1] in ["T", "K", "Q", "J","A"]:
                if valid_actions[1]['amount'] < 150:
                    return valid_actions[2]['action'], valid_actions[2]['amount']['min']*3
            else:
                if valid_actions[1]['amount'] < 250:
                    return valid_actions[2]['action'], valid_actions[2]['amount']['min']*2

        if hole_card[0][0] == hole_card[1][0]:
            ssc += 2
            
        

        if len(commc) > 0:
            nums = []

            for c in commc:
                if c[1] == 'A':
                    nums.append(1)
                    nums.append(14)
                    continue
                elif c[1] in hd:
                    nums.append(hd.get(c[1].strip()))   
                else:
                    nums.append(int(c[1]))

            for i in commc:
                if (hole_card[0][0] == hole_card[1][0]) and i[0] == hole_card[0][0]:
                    ssc += 1
                    if ssc == 5:
                        return "raise", valid_actions[2]["amount"]["min"]*6

                    if (ssc + rounds_left >= 5):
                        if valid_actions[1]['amount'] < 150:
                            return "raise", valid_actions[2]["amount"]["min"]*ssc

            nums.extend(hc_num)
            nums = sorted(nums)

            straight_pos = 1
            for i in range(1, len(nums)):
        # If the current element is not exactly one more than the previous one, return False
                if nums[i] - nums[i-1] != 1:
                    straight_pos = 1
                else:
                    straight_pos += 1

                if straight_pos == 5:
                    return "raise", valid_actions[2]["amount"]["max"]

                if (straight_pos + rounds_left >= 5):
                    if valid_actions[1]['amount'] < 250:
                        return "raise", valid_actions[2]["amount"]["min"]*straight_pos            

        
                    

        if valid_actions[1]['amount'] > 150:
            self.fold_count += 1
            if (self.fold_count > 3 and self.pos > 1):  
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

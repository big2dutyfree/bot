"""
BIG 2 DUTY FREE
Copyright (c) TNemz and Plastic Tortoise

Strategy:
    - Split our cards into possible hands
    - Calculate percentile for each hand type, taking into consideration the hands that have already been played
    - Play our best cards except leave a pair and a single for the end
    - Ultimately, this strategy aims to minimise passing  
"""

from classes import *
import itertools

class Algorithm:
    def high_suit(self, suit1, suit2):
        if suit1 == suit2:
            return suit1
        
        if "S" in [suit1, suit2]:
            return "S"
        
        if "H" in [suit1, suit2]:
            return "H"
        
        return "C"
    
    def tuple_cards(self, hand: list):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']

        tuple_hand = []

        for i in hand:
            value = ranks.index(i[0]) + 3
            tuple_hand.append((value, i[1]))

        return tuple_hand
    
    def untuple_cards(self, hand: list):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']

        untuple_hand = []

        for i in hand:
            untuple_hand.append(f"{ranks[i[0] - 3]}{i[1]}")

        return untuple_hand

    def move_type(self, move):
        move.sort()

        if move[0][0] % 13 == move[1][0] % 13 - 1 == move[2][0] % 13 - 2 == move[3][0] % 13 - 3 and (move[0][0] % 13 == move[4][0] % 13 - 4 or move[0][0] % 13 == move[4][0] - 4) and move[0][1] == move[1][1] == move[2][1] == move[3][1] == move[4][1]:
            return ("Straight flush", move[0][0] % 13, move[1][0])
        
        # Straight
        if move[0][0] % 13 == move[1][0] % 13 - 1 == move[2][0] % 13 - 2 == move[3][0] % 13 - 3 and move[0][0] == move[4][0] % 13 - 4 or move[0][0] == move[4][0] - 4:
            return ("Straight", move[0][0] % 13)
        
        # Flush
        if move[0][1] == move[1][1] == move[2][1] == move[3][1] == move[4][1]:
            return ("Flush", move[4][0], move[3][0], move[2][0], move[1][0], move[0][0], move[0][1])
        
        # Full house
        if move[0][0] == move[1][0] and move[2][0] == move[3][0] == move[4][0]:
            return ("Full house", move[4][0])
        
        if move[0][0] == move[1][0] == move[2][0] and move[3][0] == move[4][0]:
            return ("Full house", move[0][0])
        
        # Four of a kind
        if move[0][0] == move[1][0] == move[2][0] == move[3][0]:
            return ("Four of a kind", move[0][0])

        if move[1][0] == move[2][0] == move[3][0] == move[4][0]:
            return ("Four of a kind", move[4][0])
    
    def valid(self, move):
        move.sort()

        # High card
        if len(move) == 1:
            return True
        
        # Two of a kind
        if len(move) == 2 and move[0][0] == move[1][0]:
            return True
        
        # Trips
        if len(move) == 3 and move[0][0] == move[1][0] == move[2][0]:
            return True
         
        if len(move) == 5:
            # Straight flush
            if move[0][0] % 13 == move[1][0] % 13 - 1 == move[2][0] % 13 - 2 == move[3][0] % 13 - 3 and (move[0][0] % 13 == move[4][0] % 13 - 4 or move[0][0] % 13 == move[4][0] - 4) and move[0][1] == move[1][1] == move[2][1] == move[3][1] == move[4][1]:
                return True
            
            # Straight
            if move[0][0] % 13 == move[1][0] % 13 - 1 == move[2][0] % 13 - 2 == move[3][0] % 13 - 3 and (move[0][0] == move[4][0] % 13 - 4 or move[0][0] == move[4][0] - 4):
                return True
            
            # Flush
            if move[0][1] == move[1][1] == move[2][1] == move[3][1] == move[4][1]:
                return True
            
            # Full house
            if move[0][0] == move[1][0] and move[2][0] == move[3][0] == move[4][0]:
                return True
            
            if move[0][0] == move[1][0] == move[2][0] and move[3][0] == move[4][0]:
                return True
            
            # Four of a kind
            if move[0][0] == move[1][0] == move[2][0] == move[3][0]:
                return True

            if move[1][0] == move[2][0] == move[3][0] == move[4][0]:
                return True

        return False

    def percentile(self, trick: list, hand: list, played: list):
        deck = [(x, y) for x in range(3, 16) for y in ["H", "S", "C", "D"]]
        deck = list(set(deck) - set(hand) - set(played) - set(trick))

        if len(trick) == 1:
            higher = 0
            
            for card in deck:
                if card[0] > trick[0][0] or (card[0] == trick[0][0] and self.high_suit(card[1], trick[0][1]) == card[1]):
                    higher += 1

            return 1 - (higher / len(deck))
        elif len(trick) == 2 and self.valid(trick):
            higher = 0
            n = 0

            for card in deck:
                for card2 in deck:
                    if card[0] == card2[0] and card != card2:
                        n += 0.5

                        if card[0] > trick[0][0] or (card[0] == trick[0][0] and (card[1] == "S" or card2[1] == "S")):
                            higher += 0.5
            
            return 1 - (higher / n)
        elif len(trick) == 3 and self.valid(trick):
            higher = 0
            n = 0

            for card in deck:
                for card2 in deck:
                    for card3 in deck:
                        if card[0] == card2[0] == card3[0] and card not in [card2, card3] and card2 != card3:
                            n += 0.5

                            if card[0] > trick[0][0]:
                                higher += 0.5
            
            return 1 - (higher / n)
        elif len(trick) == 5:
            n = 0
            higher = 0

            trick_type = self.move_type(trick)

            if len(deck) <= 36:
                for cards in itertools.combinations(deck, 5):
                    if self.valid(list(cards)):
                        n += 1

                        card_type = self.move_type(list(cards))

                        if card_type[0] == "Straight flush":
                            if trick_type[0] in ["Four of a kind", "Full house", "Flush", "Straight"]:
                                higher += 1
                            
                            if card_type[0] == trick_type[0]:
                                if card_type[1] > trick_type[1]:
                                    higher += 1
                                
                                if card_type[1] == trick_type[1] and self.high_suit(card_type[2], trick_type[2]) == card_type[2]:
                                    higher += 1
                        
                        if card_type[0] == "Four of a kind":
                            if trick_type[0] in ["Full house", "Flush", "Straight"]:
                                higher += 1
                            
                            if card_type[0] == trick_type[0] and card_type[1] > trick_type[1]:
                                higher += 1
                                
                        if card_type[0] == "Full house":
                            if trick_type[0] in ["Flush", "Straight"]:
                                higher += 1
                            
                            if card_type[0] == trick_type[0] and card_type[1] > trick_type[1]:
                                higher += 1
                            
                        if card_type[0] == "Flush":
                            if trick_type[0] == "Straight":
                                higher += 1
                            
                            if card_type[0] == trick_type[0]:
                                if card_type[1] > trick_type[1]:
                                    higher += 1

                                if card_type[1] == trick_type[1] and card_type[2] > trick_type[2]:
                                    higher += 1

                                if card_type[1] == trick_type[1] and card_type[2] == trick_type[2] and card_type[3] > trick_type[3]:
                                    higher += 1

                                if card_type[1] == trick_type[1] and card_type[2] == trick_type[2] and card_type[3] == trick_type[3] and card_type[4] > trick_type[4]:
                                    higher += 1

                                if card_type[1] == trick_type[1] and card_type[2] == trick_type[2] and card_type[3] == trick_type[3] and card_type[4] == trick_type[4] and card_type[5] > trick_type[5]:
                                    higher += 1
                                
                                if card_type[1] == trick_type[1] and card_type[2] == trick_type[2] and card_type[3] == trick_type[3] and card_type[4] == trick_type[4] and card_type[5] == trick_type[5] and self.high_suit(card_type[6], trick_type[6]) == card_type[6]:
                                    higher += 1
                                
                        if card_type[0] == trick_type[0] == "Straight" and card_type[1] > trick_type[1]:
                            higher += 1

                return 1 - (higher / n)
            else:
                n = 2598960
                higher = 0

                if trick_type == "Straight flush":
                    return 1 - (36 / n)
                if trick_type == "Four of a kind":
                    return 1 - (624 / n)
                if trick_type == "Full house":
                    return 1 - (3744 / n)
                if trick_type == "Flush":
                    return 1 - (5108 / n)
                if trick_type == "Straight":
                    return 1 - (10200 / n)


    def split(self, hand: list, played: list):
        changed_hand = hand
        split_hand = []
        valid = 5

        while len(changed_hand) != 0:
            strong_hand = []
            strong_percentile = 0
            
            if valid > 1:
                for subset in itertools.combinations(changed_hand, valid):
                    if self.valid(list(subset)):
                        hand_percentile = self.percentile(list(subset), hand, played)
                        strong_percentile = hand_percentile
                        strong_hand = list(subset)

                if strong_percentile == 0:
                    valid -= 1

                if strong_hand != []:
                    split_hand.append(strong_hand)
                    changed_hand = list(set(changed_hand) - set(strong_hand))
            else:
                for i in changed_hand:
                    split_hand.append([i])
                changed_hand = []

        return split_hand

    
    def getAction(self, state: MatchState):
        hand = self.tuple_cards(state.myHand)

        played = []
        
        for round in state.matchHistory[-1].gameHistory:
            for cards_played in round:
                played.extend(cards_played.cards)

        split_hand = self.split(hand, played)

        for trick in split_hand:
            if len(state.toBeat) == 0:
                return self.untuple_cards(trick), ""

            if len(state.toBeat) == len(trick):
                if self.percentile(self.tuple_cards(state.toBeat), [], played) < self.percentile(trick, hand, played):
                    return self.untuple_cards(trick), ""
                
        return [], ""


# print(Algorithm().untuple_cards([(7, 'S'), (8, 'S'), (10, 'S'), (11, 'S'), (14, 'S')]))
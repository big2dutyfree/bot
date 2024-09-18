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

        for i in hand:

        for i in hand:
            value = ranks.index(i[0]) + 3
            tuple_hand.append((value, i[1]))

        return tuple_hand
    
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
            if move[0][0] % 13 == move[1][0] % 13 - 1 == move[2][0] % 13 - 2 == move[3][0] % 13 - 3 and move[0][0] == move[4][0] % 13 - 4 or move[0][0] == move[4][0] - 4:
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
                if card[0] > trick[0][0] or (card[0] == trick[0][0] and self.high_suit(card[1], card[0][1]) == card[1]):
                    higher += 1

            return 1 - (higher / len(deck))
        elif len(trick) == 2:
            pass


    def split(self, hand: list, played: list):
        changed_hand = hand
        split_hand = []

        while len(hand) != 0:
            strong_hand = []
            strong_percentile = 0

            valid = 5
            
            if valid > 1:
                for subset in itertools.combinations(changed_hand, valid):
                    hand_percentile = self.percentile(list(subset), hand, played)
                    
                    if self.valid(list(subset)) and hand_percentile > strong_percentile:
                        strong_percentile = hand_percentile
                        strong_hand = list(subset)     
            else:
                pass
    
    def getAction(self, state: MatchState):
        hand = self.tuple_cards(state.myHand)

        played = []
        
        for round in state.matchHistory[-1].gameHistory:
            for cards_played in round:
                played.extend(cards_played)

        split_hand = self.split(hand, played)

        for trick in split_hand:
            if len(state.toBeat.cards) == 0:
                return self.untuple_cards(trick), ""

            if len(state.toBeat.cards) == len(trick):
                if self.percentile(self.tuple_cards(state.toBeat.cards), [], played) < self.percentile(trick, hand, played):
                    return self.untuple_cards(trick), ""
                
        return [], ""



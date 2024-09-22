"""
BIG 2 DUTY FREE 2.0
Copyright (c) TNemz and Plastic Tortoise

Strategy: Extension of Sugiyanto's (2020) proposed algorithm to accomodate triples.

https://doi.org/10.3390/app11094206
"""

from classes import *
import itertools

class Algorithm:
    def oset(self, olist: list) -> list:
        olist = list(dict.fromkeys(olist).keys())

        olist.sort()

        return olist
    
    def high_suit(self, suit1: str, suit2: str) -> str:
        if suit1 == suit2:
            return suit1
        
        if "S" in [suit1, suit2]:
            return "S"
        
        if "H" in [suit1, suit2]:
            return "H"
        
        return "C"
    
    def tuple_cards(self, hand: list) -> list:
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']

        tuple_hand = []

        for i in hand:
            value = ranks.index(i[0]) + 3
            tuple_hand.append((value, i[1]))

        return tuple_hand
    
    def untuple_cards(self, hand: list) -> list:
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']

        untuple_hand = []

        for i in hand:
            untuple_hand.append(f"{ranks[i[0] - 3]}{i[1]}")

        return untuple_hand
    
    def opponents(self, hand: list, played: list) -> dict[list]:
        deck = [(x, y) for x in range(3, 16) for y in ["H", "S", "C", "D"]]
        deck = list(set(deck) - set(hand) - set(played))

        ranks = [card[0] for card in deck]
        suits = [card[1] for card in deck]

        hands = {
            "single": [],
            "pairs": [],
            "triple": [],
            "fours": [],
            "fiver": []
        }

        # Singles

        for card in deck:
            hands["single"].append([card])

        # Pairs

        for card in deck:
            for suit in ["S", "D", "H", "C"]:
                if (card[0], suit) in deck and card[1] != suit and [(card[0], suit), card] not in hands["pairs"]:
                    hands["pairs"].append(self.oset([card, (card[0], suit)]))

        # Trips

        for card in deck:
            for pair in hands["pairs"]:
                if card[0] == pair[0][0] and card not in pair and self.oset([card, pair[0], pair[1]]) not in hands["triple"]:
                    hands["triple"].append(self.oset([card, pair[0], pair[1]]))

        # Fours

        for card in deck:
            if (card[0], "D") in deck and (card[0], "C") in deck and (card[0], "H") in deck and (card[0], "S") in deck and self.oset([(card[0], "D"), (card[0], "C"), (card[0], "S"), (card[0], "H")]) not in hands["fours"]:
                hands["fours"].append(self.oset([(card[0], "D"), (card[0], "C"), (card[0], "S"), (card[0], "H")]))
        
        # Fivers

        # Straight flush

        for card in deck:
            if card[0] <= 10 and (card[0] + 1, card[1]) in deck and (card[0] + 2, card[1]) in deck and (card[0] + 3, card[1]) in deck and (card[0] + 4, card[1]) in deck:
                hands["fiver"].append(("Straight flush", card))
        
        # Straight

        for (index, rank) in enumerate(ranks):
            if rank <= 10:
                card2 = [i for (i, x) in enumerate(ranks) if x == rank + 1]
                card3 = [i for (i, x) in enumerate(ranks) if x == rank + 2]
                card4 = [i for (i, x) in enumerate(ranks) if x == rank + 3]
                card5 = [i for (i, x) in enumerate(ranks) if x == rank + 4]

                if len(card2) >= 1 and len(card3) >= 1 and len(card4) >= 1 and len(card5) >= 1:
                    for c2 in card2:
                        for c3 in card3:
                            for c4 in card4:
                                for c5 in card5:
                                    if ("Straight", self.oset([deck[index], deck[c2], deck[c3], deck[c4], deck[c5]])[0]) not in hands["fiver"]:
                                        hands["fiver"].append(("Straight", self.oset([deck[index], deck[c2], deck[c3], deck[c4], deck[c5]])[0]))

        # Flush
        
        spades = []
        hearts = []
        clubs = []
        diamonds = []

        for (i, x) in enumerate(suits):
            match x:
                case "S":
                    spades.append(deck[i])
                case "D":
                    diamonds.append(deck[i])
                case "H":
                    hearts.append(deck[i])
                case "C":
                    clubs.append(deck[i])
        
        for subset in itertools.combinations(spades, 5):
            if ("Flush", self.oset(list(subset) + [deck[index]]), "S") not in hands["fiver"]:
                hands["fiver"].append(("Flush", self.oset(list(subset) + [deck[index]]), "S"))

        for subset in itertools.combinations(hearts, 5):
            if ("Flush", self.oset(list(subset) + [deck[index]]), "H") not in hands["fiver"]:
                hands["fiver"].append(("Flush", self.oset(list(subset) + [deck[index]]), "H"))

        for subset in itertools.combinations(clubs, 5):
            if ("Flush", self.oset(list(subset) + [deck[index]]), "C") not in hands["fiver"]:
                hands["fiver"].append(("Flush", self.oset(list(subset) + [deck[index]]), "C"))

        for subset in itertools.combinations(diamonds, 5):
            if ("Flush", self.oset(list(subset) + [deck[index]]), "D") not in hands["fiver"]:
                hands["fiver"].append(("Flush", self.oset(list(subset) + [deck[index]]), "D"))

        
        # Full house
        
        for triple in hands["triple"]:
            for double in hands["pairs"]:
                if triple[0][0] != double[0][0]:
                    hands["fiver"].append(("Full house", triple[0][0]))

        return hands
    
    def compare(self, hand: list, to_beat: list | tuple) -> bool:
        if hand[0] == "Straight flush":
            if to_beat[0] in ["Flush", "Full house", "Straight"] or len(to_beat) == 4:
                return True
            
            if to_beat[0] == "Straight flush" and hand[1][0] > to_beat[1][0] or (hand[1][0] == to_beat[1][0] and self.high_suit(hand[1][1], to_beat[1][1]) == hand[1][1]):
                return True

            return False
        if hand[0] == "Full house":
            if to_beat[0] in ["Flush", "Straight"]:
                return True
            
            if to_beat[0] == "Full house" and hand[1] > to_beat[1]:
                return True
            
            return False
        if hand[0] == "Flush":
            if to_beat[0] == "Straight":
                return True
            
            if to_beat[0] == "Flush":
                if hand[1][4] > to_beat[1][4]:
                    return True
                
                if hand[1][4] == to_beat[1][4] and hand[1][3] > to_beat[1][3]:
                    return True
                
                if hand[1][4] == to_beat[1][4] and hand[1][3] == to_beat[1][3] and hand[1][2] > to_beat[1][2]:
                    return True
                
                if hand[1][4] == to_beat[1][4] and hand[1][3] == to_beat[1][3] and hand[1][2] == to_beat[1][2] and hand[1][1] > to_beat[1][1]:
                    return True
                
                if hand[1][4] == to_beat[1][4] and hand[1][3] == to_beat[1][3] and hand[1][2] == to_beat[1][2] and hand[1][1] == to_beat[1][1] and hand[1][0] > to_beat[1][0]:
                    return True
                
                if hand[1][4] == to_beat[1][4] and hand[1][3] == to_beat[1][3] and hand[1][2] == to_beat[1][2] and hand[1][1] == to_beat[1][1] and hand[1][0] == to_beat[1][0] and self.high_suit(hand[1][1], to_beat[1][1]) == hand[1][1]:
                    return True
            
            return False
        if hand[0] == "Straight":
            if to_beat[0] == "Straight" and hand[1][0] > to_beat[1][0]:
                return True
            
            return False
        if len(hand) == 1:
            if hand[0][0] > to_beat[0][0] or (hand[0][0] == to_beat[0][0] and self.high_suit(hand[0][1], to_beat[0][1]) == hand[0][1]):
                return True
            
            return False
        if len(hand) == 2:
            if hand[0][0] > to_beat[0][0] or (hand[0][0] == to_beat[0][0] and (hand[0][1] == "S" or hand[1][1] == "S")):
                return True
            
            return False
        if len(hand) == 3:
            if hand[0][0] > to_beat[0][0]:
                return True
            
            return False
        if len(hand) == 4:
            if hand[0][0] > to_beat[0][0] or to_beat[0] in ["Flush", "Full house", "Straight"]:
                return True


    def classify(self, hand: list, played: list):
        classes = {
            "A": [],
            "B": [],
            "C": [],
            "D": []
        }

        op = self.opponents(hand, played)

        for i in hand:
            beats = sum(1 for x in op["single"] if self.compare([i], x))

            if beats == len(op["single"]):
                classes["A"].append([i])
            elif beats > 0.8 * len(op["single"]):
                classes["B"].append([i])
            elif beats == 0:
                classes["D"].append([i])
            else:
                classes["C"].append([i])

            for j in ["D", "H", "C", "S"]:
                if (i[0], j) in hand and i != (i[0], j):
                    beats = sum(1 for x in op["pairs"] if self.compare([i, (i[0], j)], x))

                    if beats == len(op["pairs"]) and self.oset([(i[0], j), i]) not in classes["A"] and self.oset([(i[0], j), i]) not in classes["B"]:
                        classes["A"].append(self.oset([(i[0], j), i]))
                    elif beats > 0.8 * len(op["pairs"]) and self.oset([(i[0], j), i]) not in classes["B"] and self.oset([(i[0], j), i]) not in classes["A"]:
                        classes["B"].append(self.oset([(i[0], j), i]))
                    elif beats == 0 and [(i[0], j), i] not in classes["D"]:
                        classes["D"].append(self.oset([(i[0], j), i]))
                    elif [(i[0], j), i] not in classes["C"]:
                        classes["C"].append(self.oset([(i[0], j), i]))


        for i in itertools.combinations(hand, 3):
            beats = sum(1 for x in op["triple"] if self.compare(i, x))
            
            if i[0][0] == i[1][0] == i[2][0]:
                if beats == len(op["triple"]):
                    classes["A"].append(self.oset(i))
                elif beats > 0.8 * len(op["triple"]):
                    classes["B"].append(self.oset(i))
                elif beats == 0:
                    classes["D"].append(self.oset(i))
                else:
                    classes["C"].append(self.oset(i))

        for i in itertools.combinations(hand, 4):
            beats = sum(1 for x in op["fours"] if self.compare(i, x))
            
            if i[0][0] == i[1][0] == i[2][0] == i[3][0]:
                if beats == len(op["fours"]):
                    classes["A"].append(self.oset(i))
                elif beats > 0.8 * len(op["fours"]):
                    classes["B"].append(self.oset(i))
                elif beats == 0:
                    classes["D"].append(self.oset(i))
                else:
                    classes["C"].append(self.oset(i))

        for i in itertools.combinations(hand, 5):
            hand = ()

            i = self.oset(i)
            
            if i[0][0] <= 10 and i[0][0] == i[1][0] - 1 == i[2][0] - 2 == i[3][0] - 3 == i[4][0] - 4:
                if i[0][1] == i[1][1] == i[2][1] == i[3][1] == i[4][1]:
                    hand = ("Straight flush", i[0])
                else:
                    hand = ("Straight", i[0])
            elif i[0][1] == i[1][1] == i[2][1] == i[3][1] == i[4][1]:
                hand = ("Flush", i)
            elif i[0][0] == i[1][0] == i[2][0] and i[3][0] == i[4][0]:
                hand = ("Full house", i[0][0])
            elif i[0][0] == i[1][0] and i[2][0] == i[3][0] == i[4][0]:
                hand = ("Full house", i[2][0])


            if hand != ():
                beats = sum(1 for x in op["fiver"] if self.compare(hand, x))
                
                if beats == len(op["fiver"]):
                    classes["A"].append(i)
                elif beats > 0.8 * len(op["fiver"]):
                    classes["B"].append(i)
                elif beats == 0:
                    classes["D"].append(i)
                else:
                    classes["C"].append(i)

        return classes



    def getAction(self, state: MatchState | None):
        hand =  ["3H", "5D", "6D", "6S", "7H", "8D", "TC", "QD", "QH", "KS", "AD", "2C", "2S"]
        hand = self.tuple_cards(hand)
        # hand = self.tuple_cards(state.myHand)

        played = []
        
        """
        for round in state.matchHistory[-1].gameHistory:
            for cards_played in round:
                played.extend(cards_played.cards)

        """
        classified = self.classify(hand, played)

        # One combination left
        
        if self.oset(hand) in classified["A"] or self.oset(hand) in classified["B"] or self.oset(hand) in classified["C"] or self.oset(hand) in classified["D"]:
            return self.untuple_cards(hand), ""

        return classified


print(Algorithm().getAction(None))
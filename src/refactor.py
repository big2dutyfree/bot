"""
BIG 2 DUTY FREE 2.0
Copyright (c) The Plastic Tortoise & TNemz
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
            if ("Flush", self.oset(list(subset)), "S") not in hands["fiver"]:
                hands["fiver"].append(("Flush", self.oset(list(subset)), "S"))

        for subset in itertools.combinations(hearts, 5):
            if ("Flush", self.oset(list(subset)), "H") not in hands["fiver"]:
                hands["fiver"].append(("Flush", self.oset(list(subset)), "H"))

        for subset in itertools.combinations(clubs, 5):
            if ("Flush", self.oset(list(subset)), "C") not in hands["fiver"]:
                hands["fiver"].append(("Flush", self.oset(list(subset)), "C"))

        for subset in itertools.combinations(diamonds, 5):
            if ("Flush", self.oset(list(subset)), "D") not in hands["fiver"]:
                hands["fiver"].append(("Flush", self.oset(list(subset)), "D"))

        
        # Full house
        
        for triple in hands["triple"]:
            for double in hands["pairs"]:
                if triple[0][0] != double[0][0]:
                    hands["fiver"].append(("Full house", triple[0][0]))

        return hands
    
    def compare(self, hand: list, to_beat: list) -> bool:
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
                hand[1].sort()
                to_beat[1].sort()

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
            if to_beat[0] in ["Flush", "Full house", "Straight"]:
                return True

            if type(to_beat[0]):
                return False
            
            if hand[0][0] > to_beat[0][0]:
                return True
            
            return False


    def classify(self, hand: list, played: list):
        classes = {
            "A": [],
            "B": [],
            "C": [],
            "D": [],
            "all": []
        }

        op = self.opponents(hand, played)

        for i in hand:
            beats = sum(1 for x in op["single"] if self.compare([i], x))

            classes["all"].append([i])

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

                    if beats == len(op["pairs"]) and self.oset([(i[0], j), i]) not in classes["all"]:
                        classes["A"].append(self.oset([(i[0], j), i]))
                    elif beats > 0.8 * len(op["pairs"]) and self.oset([(i[0], j), i]) not in classes["all"]:
                        classes["B"].append(self.oset([(i[0], j), i]))
                    elif beats == 0 and self.oset([(i[0], j), i]) not in classes["all"]:
                        classes["D"].append(self.oset([(i[0], j), i]))
                    elif self.oset([(i[0], j), i]) not in classes["all"]:
                        classes["C"].append(self.oset([(i[0], j), i]))

                    if self.oset([(i[0], j), i]) not in classes["all"]:
                        classes["all"].append(self.oset([(i[0], j), i]))

        for i in itertools.combinations(hand, 3):
            beats = sum(1 for x in op["triple"] if self.compare(i, x))
            
            if i[0][0] == i[1][0] == i[2][0]:
                classes["all"].append(self.oset(i))

                if beats == len(op["triple"]):
                    classes["A"].append(self.oset(i))
                elif beats > 0.8 * len(op["triple"]):
                    classes["B"].append(self.oset(i))
                elif beats == 0:
                    classes["D"].append(self.oset(i))
                else:
                    classes["C"].append(self.oset(i))

        for i in itertools.combinations(hand, 4):
            beats1 = sum(1 for x in op["fours"] if self.compare(i, x))
            beats2 = sum(1 for x in op["fiver"] if self.compare(i, x))
            beats = beats1 + beats2
            
            if i[0][0] == i[1][0] == i[2][0] == i[3][0]:
                classes["all"].append(self.oset(i))
                 
                if beats == len(op["fours"]) + len(op["fiver"]):
                    classes["A"].append(self.oset(i))
                elif beats > 0.8 * (len(op["fours"]) + len(op["fiver"])):
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
                fivers = op["fiver"]
                fivers.extend(op["fours"])
                beats = sum(1 for x in fivers if self.compare(hand, x))

                classes["all"].append(i)
                
                if beats == len(fivers):
                    classes["A"].append(i)
                elif beats > 0.8 * len(fivers):
                    classes["B"].append(i)
                elif beats == 0:
                    classes["D"].append(i)
                else:
                    classes["C"].append(i)

        return classes

    
    def two_cards(self, hand: list, classified: dict, ohands: list) -> list:
        hand.sort()

        if 1 in ohands or hand[1] in classified["A"]:
            return [hand[1]]
        
        return [hand[0]]
    
    def three_cards(self, hand: list, classified: dict, ohands: list) -> list:
        for i in classified["all"]:
            if len(i) == 2:
                if i in classified["A"]:
                    return i
                
                if list(set(hand) - set(i)) in classified["A"]:
                    return list(set(hand) - set(i))
                
                if 1 in ohands:
                    return i
                
                if 2 in ohands:
                    return list(set(hand) - set(i))
                
                return i

        hand.sort()

        if hand[2] in classified["A"]:
            return [hand[1]]
        
        if 1 in ohands:
            return [hand[2]]
        
        return [hand[0]]
    
    def four_cards(self, hand: list, classified: dict, ohands: list) -> list:
        triples = [i for i in classified["all"] if len(i) == 3]

        if len(triples) > 0:
            if triples[0] in classified["A"]:
                return triples[0]
            if list(set(hand) - set(triples[0])) in classified["A"]:
                return list(set(hand) - set(triples[0]))
            
            return triples[0]
            
        pairs = [i for i in classified["all"] if len(i) == 2]

        if len(pairs) == 2:
            pairs.sort()

            if pairs[1] in classified["A"]:
                return pairs[0]
            if 2 in ohands:
                return pairs[1]
            
            return pairs[0]
        
        if len(pairs) == 1:
            singles = [i for i in classified["all"] if len(i) == 1]

            singles.sort()

            if singles[1] in classified["A"]:
                return singles[0]
            
            if 1 in ohands:
                return pairs[0]
            
            return singles[0]
        
        hand.sort()

        if hand[3] in classified["A"]:
            return [hand[1]]
        
        if 1 in ohands:
            return [hand[3]]
        
        return [hand[0]]

    def win_in_three(self, hand: list, classified: dict, ohands: list) -> list | None:
        wm = []
        changed = hand

        for rank in ["A", "B", "C", "D"]:
            classified[rank].sort(key=len, reverse=True)
            for i in classified[rank]:
                i.sort()
                if len(i) == 5:
                    if i[0] in changed and i[1] in changed and i[2] in changed and i[3] in changed and i[4] in changed:
                        if i[0][0] == i[1][0] - 1 == i[2][0] - 2 == i[3][0] - 3 == i[4][0] - 4 and i[0][1] == i[1][1] == i[2][1] == i[3][1] == i[4][1]:
                            wm.append(i)
                            changed = list(set(changed) - set(i))
                        elif (i[0][0] == i[1][0] == i[2][0] == i[3][0]) or (i[1][0] == i[2][0] == i[3][0] == i[4][0]):
                            wm.append(i)
                            changed = list(set(changed) - set(i))
                        elif (i[0][0] == i[1][0] == i[2][0] and i[3][0] == i[4][0]) or (i[0][0] == i[1][0] and i[2][0] == i[3][0] == i[4][0]):
                            wm.append(i)
                            changed = list(set(changed) - set(i))
                        elif i[0][1] == i[1][1] == i[2][1] == i[3][1] == i[4][1]:
                            wm.append(i)
                            changed = list(set(changed) - set(i))
                        else:
                            wm.append(i)
                            changed = list(set(changed) - set(i))
                elif len(i) == 3:
                    if i[0] in changed and i[1] in changed and i[2] in changed:
                        wm.append(i)
                        changed = list(set(changed) - set(i))
                elif len(i) == 2:
                    if i[0] in changed and i[1] in changed:
                        wm.append(i)
                        changed = list(set(changed) - set(i))
                else:
                    if i[0] in changed:
                        wm.append(i)
                        changed = list(set(changed) - set(i))

                if len(changed) == 0:
                    break

            if len(changed) == 0:
                    break

        if len(wm) == 2:
            if wm[0] in classified["A"]:
                return wm[0]
            
            if wm[1] in classified["A"]:
                return wm[1]
            
            if len(wm[0]) == 5:
                return wm[0]
            
            if len(wm[1]) == 5:
                return wm[1]
            
            if len(wm[0]) == 2 or len(wm[1]) == 2:
                wm.sort()

                if 2 in ohands:
                    return wm[1]
                
                return wm[0]
        if len(wm) == 3:
            if wm[0] in classified["A"] and wm[1] in classified["A"] or wm[0] in classified["A"] and wm[2] in classified["A"]:
                return wm[0]
            
            if wm[1] in classified["A"] and wm[2] in classified["A"]:
                return wm[1]
            
            if len(wm[0]) == 5:
                return wm[0]
            
            if len(wm[1]) == 5:
                return wm[1]
            
            if len(wm[0]) == 2 or len(wm[1]) == 2:
                wm.sort()

                if 2 in ohands:
                    return wm[1]
                
                return wm[0]
            
    def hold_back(self, hand: list, trick: list, tobeat: list, classified: dict, reclassified: dict, rnd: int, ohands: list, passes: int) -> bool:
        if len(tobeat) == 1:
            if len(hand) <= 5:
                return False
            if 1 in ohands or 2 in ohands or 3 in ohands or 4 in ohands:
                return False
            if len(classified["A"]) < (len(classified["B"]) + len(classified["C"]) + len(classified["D"])) or min(len(classified["A"]), ohands[0], ohands[1], ohands[2]) > 6:
                if len(classified["A"]) > 0:
                    if trick == classified["A"][-1]:
                        return True
                
            return False
        
        if len(tobeat) == 2:
            if len(hand) <= 3:
                return False
            
            if min(ohands) > 2:
                if trick[0][0] == 15:
                    return True
                
            return False
        
        if len(tobeat) == 3:
            if len(hand) <= 4:
                return False
            
            if min(ohands) > 3:
                if trick[0][0] == 15:
                    return True
                
            return False
        
        if len(tobeat) == 5:
            if len(hand) == 5:
                return False
            
            if min(len(classified["A"]), ohands[0], ohands[1], ohands[2]) > 6 and rnd <= 2:
                if passes > 0:
                    fives = [i for i in reclassified["all"] if len(i) == 5]
                    if fives >= 2 and (trick in reclassified["A"] or trick in reclassified["B"]):
                        return True
                
            return False

    
    def split_card(self, tobeat: list, reclassified: dict):
        if len(tobeat) == 3:
            for i in reclassified["all"]:
                if len(i) == 5:
                    if i[0][0] == i[1][0] == i[2][0] and [i[0], i[1], i[3]] in reclassified["all"]:
                        return [i[0], i[1], i[3]]
                    
                    if i[2][0] == i[3][0] == i[4][0] and [i[2], i[3], i[4]] in reclassified["all"]:
                        return [i[2], i[3], i[4]]
        if len(tobeat) == 2:
            for i in reclassified["all"]:
                if len(i) == 5:
                    if i[0][0] == i[1][0] and [i[0], i[1]] in reclassified["all"]:
                        return [i[0], i[1]]
                    
                    if i[3][0] == i[4][0] and [i[3], i[4]] in reclassified["all"]:
                        return [i[3], i[4]]
        if len(tobeat) == 1:
            for i in reclassified["all"]:
                if len(i) == 2:
                    if i[0] in reclassified["all"]:
                        return [i[0]]
                    
                    if i[1] in reclassified["all"]:
                        return [i[1]]
                    
        return []
    

    def getAction(self, state: MatchState | None):
        hand = self.tuple_cards(state.myHand)

        print(state.myHand)

        played = []
        
        for round in state.matchHistory[-1].gameHistory:
            for cards_played in round:
                played.extend(cards_played.cards)

        classified = self.classify(hand, played)

        ohands = []

        for (index, player) in enumerate(state.players):
            if index != state.myPlayerNum:
                ohands.append(player.handSize)


        # Control
        if state.toBeat == None:
            print("Control")
            # One combination left
        
            if self.oset(hand) in classified["A"] or self.oset(hand) in classified["B"] or self.oset(hand) in classified["C"] or self.oset(hand) in classified["D"]:
                return self.untuple_cards(hand), ""
            
            if (3, "D") in hand:
                for i in classified["all"]:
                    if len(i) == 3 and (3, "D") in i:
                        return self.untuple_cards(i), ""
                    
                for i in classified["all"]:
                    if len(i) == 2 and (3, "D") in i:
                        return self.untuple_cards(i), ""
                    
                for i in classified["all"]:
                    if len(i) == 5 and (3, "D") in i:
                        return self.untuple_cards(i), ""
                 
                return ["3D"], ""

            # Two card rule
            if len(hand) == 2:
                return self.untuple_cards(self.two_cards(hand, classified, ohands)), ""
            
            # Three card rule
            if len(hand) == 3:
                return self.untuple_cards(self.three_cards(hand, classified, ohands)), ""

            # Four card rule
            if len(hand) == 4:
                return self.untuple_cards(self.four_cards(hand, classified, ohands)), ""

            # Win in three rule
            wit = self.win_in_three(hand, classified, ohands)

            if wit != None:
                return self.untuple_cards(wit), ""

            # Normal play

            fives = []
            fours = []
            trips = []
            pairs = []
            singles = []
            worst_single = ()

            # Find worst single

            for i in classified["D"]:
                if len(i) == 1:
                    worst_single = i
            
            if len(worst_single) == 0:
                for i in classified["C"]:
                    if len(i) == 1:
                        worst_single = i
            
            if len(worst_single) == 0:
                for i in classified["B"]:
                    if len(i) == 1:
                        worst_single = i

            if len(worst_single) == 0:
                for i in classified["A"]:
                    if len(i) == 1:
                        worst_single = i

            # Find fives, trips and pairs

            for i in classified["A"]:
                if len(i) == 4:
                    i.append(worst_single)

            for i in classified["B"]:
                if len(i) == 4:
                    i.append(worst_single)

            for i in classified["C"]:
                if len(i) == 4:
                    i.append(worst_single)

            for i in classified["D"]:
                if len(i) == 4:
                    i.append(worst_single)

            for i in classified["all"]:
                if len(i) == 5:
                    fives.append(i)
                if len(i) == 4:
                    i.append(worst_single)
                    fives.append(i)
                if len(i) == 3:
                    trips.append(i)
                if len(i) == 2:
                    pairs.append(i)
                if len(i) == 1:
                    singles.append(i)

            trips.sort()
            pairs.sort()
            singles.sort()

            classified["A"].sort()
            classified["B"].sort()
            classified["C"].sort()
            classified["D"].sort()
            
            classified["A"].sort(key=len, reverse=True)
            classified["B"].sort(key=len, reverse=True)
            classified["C"].sort(key=len, reverse=True)
            classified["D"].sort(key=len, reverse=True)


            if 1 in ohands:
                if len(fives) != 0:
                    return self.untuple_cards(fives[0]), ""
                
                if len(trips) != 0:
                    return self.untuple_cards(trips[0]), ""

                if len(pairs) != 0:
                    return self.untuple_cards(pairs[0]), ""
                
                if len(classified["A"]) != 0:
                    return self.untuple_cards(classified["A"][-1]), ""
                if len(classified["B"]) != 0:
                    return self.untuple_cards(classified["B"][-1]), ""
                if len(classified["C"]) != 0:
                    return self.untuple_cards(classified["C"][-1]), ""
                if len(classified["D"]) != 0:
                    return self.untuple_cards(classified["D"][-1]), ""
                
                
            else:
                if len(trips) > len(pairs) and len(fives) == 0 and len(fours) == 0:
                    return self.untuple_cards(trips[0]), ""
                if len(pairs) > len(singles) and len(fives) == 0 and len(fours) == 0:
                    return self.untuple_cards(pairs[0]), ""
                
            if len(classified["D"]) != 0:
                return self.untuple_cards(classified["D"][0]), ""
            if len(classified["C"]) != 0:
                return self.untuple_cards(classified["C"][0]), ""
            if len(classified["B"]) != 0:
                return self.untuple_cards(classified["B"][0]), ""
            
            return self.untuple_cards(classified["A"][0]), ""
        else:
            # Not in control
            beat = self.tuple_cards(state.toBeat.cards)
            reclassified = {"A": [], "B": [], "C": [], "D": [], "all": []}

            print("No control", beat)

            to_beat = beat

            beat.sort()

            if len(beat) == 5:
                if beat[0][0] <= 10 and beat[0][0] == beat[1][0] - 1 == beat[2][0] - 2 == beat[3][0] - 3 == beat[4][0] - 4:
                    if beat[0][1] == beat[1][1] == beat[2][1] == beat[3][1] == beat[4][1]:
                        to_beat = ("Straight flush", beat[0])
                    else:
                        to_beat = ("Straight", beat[0])
                elif beat[0][1] == beat[1][1] == beat[2][1] == beat[3][1] == beat[4][1]:
                    to_beat = ("Flush", beat)
                elif beat[0][0] == beat[1][0] == beat[2][0] and beat[3][0] == beat[4][0]:
                    to_beat = ("Full house", beat[0][0])
                elif beat[0][0] == beat[1][0] and beat[2][0] == beat[3][0] == beat[4][0]:
                    to_beat = ("Full house", beat[2][0])
                elif beat[0][0] == beat[1][0] == beat[2][0] == beat[3][0]:
                    to_beat = [beat[0], beat[1], beat[2], beat[3]]
                elif beat[1][0] == beat[2][0] == beat[3][0] == beat[4][0]:
                    to_beat = [beat[0], beat[1], beat[2], beat[3]]

            for rank in ["A", "B", "C", "D"]:
                for i in classified[rank]:
                    trick = i

                    i.sort()

                    if len(i) == 5:
                        if i[0][0] <= 10 and i[0][0] == i[1][0] - 1 == i[2][0] - 2 == i[3][0] - 3 == i[4][0] - 4:
                            if i[0][1] == i[1][1] == i[2][1] == i[3][1] == i[4][1]:
                                trick = ("Straight flush", i[0])
                            else:
                                trick = ("Straight", i[0])
                        elif i[0][1] == i[1][1] == i[2][1] == i[3][1] == i[4][1]:
                            trick = ("Flush", i)
                        elif i[0][0] == i[1][0] == i[2][0] and i[3][0] == i[4][0]:
                            trick = ("Full house", i[0][0])
                        elif i[0][0] == i[1][0] and i[2][0] == i[3][0] == i[4][0]:
                            trick = ("Full house", i[2][0])
                        elif i[0][0] == i[1][0] == i[2][0] == i[3][0]:
                            trick = [i[0], i[1], i[2], i[3], i[4]]
                        elif i[1][0] == i[2][0] == i[3][0] == i[4][0]:
                            trick = [i[0], i[1], i[2], i[3], i[4]]

                    if len(i) == len(beat):
                        if self.compare(trick, to_beat):
                            reclassified[rank].append(i)
                            reclassified["all"].append(i)

            reclassified["D"].sort()
            reclassified["C"].sort()
            reclassified["B"].sort()
            reclassified["A"].sort()

            print(reclassified["all"])

            if self.oset(hand) in reclassified["A"] or self.oset(hand) in reclassified["B"] or self.oset(hand) in reclassified["C"] or self.oset(hand) in reclassified["D"]:
                return self.untuple_cards(hand), ""

            passes = 0
            met = False

            if 1 in ohands:
                if len(reclassified["A"]) != 0:
                    return self.untuple_cards(reclassified["A"][-1]), ""
                if len(reclassified["B"]) != 0:
                    return self.untuple_cards(reclassified["B"][-1]), ""
                if len(reclassified["C"]) != 0:
                    return self.untuple_cards(reclassified["C"][-1]), ""
                if len(reclassified["D"]) != 0:
                    return self.untuple_cards(reclassified["D"][-1]), ""

            round_history = state.matchHistory[-1].gameHistory[-1]
            round_history.reverse()

            for i in round_history:
                if met == False and i == []:
                    passes += 1

                if i != []:
                    met = True

            if len(reclassified["D"]) > 0:
                for trick in reclassified["D"]:
                    if not self.hold_back(hand, trick, beat, classified, reclassified, len(state.matchHistory[-1].gameHistory), ohands, passes):
                        return self.untuple_cards(trick), ""
            if len(reclassified["C"]) > 0:
                for trick in reclassified["C"]:
                    if not self.hold_back(hand, trick, beat, classified, reclassified, len(state.matchHistory[-1].gameHistory), ohands,  passes):
                        return self.untuple_cards(trick), ""
            if len(reclassified["B"]) > 0:
                for trick in reclassified["B"]:
                    if not self.hold_back(hand, trick, beat, classified, reclassified, len(state.matchHistory[-1].gameHistory), ohands,  passes):
                        return self.untuple_cards(trick), ""
            if len(reclassified["A"]) > 0:
                for trick in reclassified["A"]:
                    if not self.hold_back(hand, trick, beat, classified, reclassified, len(state.matchHistory[-1].gameHistory), ohands,  passes):
                        return self.untuple_cards(trick), ""
            if 1 in ohands:
                return self.untuple_cards(self.split_card(beat, reclassified)), ""
            
            return [], ""


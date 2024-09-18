"""
BIG 2 DUTY FREE
Copyright (c) TNemz and Plastic Tortoise

game.py: Defines a a playable instance of Big 2 for testing purposes
"""

import sys, random

class Game:
    def __init__(self):
        self.points = [0, 0, 0, 0]
        self.tabled = ()
        self.passed = 0
        self.turn = 0
        self.round = 0
        self.deal()

    # cards(self) -> list[tuple]
    # Generates a deck of cards and randomises the order

    def cards(self):
        deck = [(x, y) for x in range(3, 16) for y in ["hearts", "spades", "clubs", "diamonds"]]
        random.shuffle(deck)

        return deck
    
    # deal(self)
    # Ditributes the randomly ordered cards among all the players

    def deal(self):
        deck = self.cards()

        self.players = [[],[],[],[]]

        for index in range(len(deck)):
            self.players[index % 4].append(deck[index])

    # deal(self, suit1: Literal, suit2: Literal) -> Literal['spades', 'hearts', 'clubs', 'diamonds']
    # Retuns the highest suit of two provided

    def high_suit(self, suit1, suit2):
        if suit1 == suit2:
            return suit1
        
        if "S" in [suit1, suit2]:
            return "S"
        
        if "H" in [suit1, suit2]:
            return "H"
        
        return "C"

    # move_type(self, move : list) -> tuple
    # If a move is valid in big 2, returns the type of move as a tuple. If not, returns an invalid tuple.
    
    def move_type(self, move):
        move.sort()

        # High card
        if len(move) == 1:
            return ("High card", move[0][0], move[0][1])
        
        # Two of a kind
        if len(move) == 2 and move[0][0] == move[1][0]:
            return ("Two of a kind", move[0][0], self.high_suit(move[0][1], move[1][1]))
        
        # Trips
        if len(move) == 3 and move[0][0] == move[1][0] == move[2][0]:
            return ("Trips", move[0][0])
         
        if len(move) == 5:
            # Straight flush
            if move[0][0] % 13 == move[1][0] % 13 - 1 == move[2][0] % 13 - 2 == move[3][0] % 13 - 3 and (move[0][0] % 13 == move[4][0] % 13 - 4 or move[0][0] % 13 == move[4][0] - 4) and move[0][1] == move[1][1] == move[2][1] == move[3][1] == move[4][1]:
                return ("Straight flush", move[0][0] % 13, move[1][0])
            
            # Straight
            if move[0][0] % 13 == move[1][0] % 13 - 1 == move[2][0] % 13 - 2 == move[3][0] % 13 - 3 and move[0][0] == move[4][0] % 13 - 4 or move[0][0] == move[4][0] - 4:
                return ("Straight", move[0][0] % 13)
            
            # Flush
            if move[0][1] == move[1][1] == move[2][1] == move[3][1] == move[4][1]:
                return ("Flush", move[4][0], move[0][1])
            
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

        return ("Invalid")
    

    def valid(self, move):
        if len(self.tabled) == 0:
            return True
        
        move = self.move_type(move)
        
        if move == ("Invalid"):
            return False
        
        if move[0] == self.tabled[0] == "High card":
            if move[1] > self.tabled[1] or move[1] == self.tabled[1] and self.high_suit(self.tabled[2], move[2]) == move[2]:
                return True
        
        if move[0] == self.tabled[0] == "Trips" and move[1] > self.tabled[1]:
            return True

        if move[0] == self.tabled[0] == "Two of a kind":
            if move[1] > self.tabled[1]:
                return True
            
            if move[1] == self.tabled[1] and self.high_suit(move[2], self.tabled[2]) == move[2]:
                return True
            
        if move[0] == "Straight flush":
            if self.tabled[0] in ["Four of a kind", "Full house", "Flush", "Straight"]:
                return True
            
            if move[0] == self.tabled[0]:
                if move[1] > self.tabled[1]:
                    return True
                
                if move[1] == self.tabled[1] and self.high_suit(move[2], self.tabled[2]) == move[2]:
                    return True
        
        if move[0] == "Four of a kind":
            if self.tabled[0] in ["Full house", "Flush", "Straight"]:
                return True
            
            if move[0] == self.tabled[0] and move[1] > self.tabled[1]:
                return True
                
        if move[0] == "Full house":
            if self.tabled[0] in ["Flush", "Straight"]:
                return True
            
            if move[0] == self.tabled[0] and move[1] > self.tabled[1]:
                return True
            
        if move[0] == "Flush":
            if self.tabled[0] == "Straight":
                return True
            
            if move[0] == self.tabled[0]:
                if move[1] > self.tabled[1]:
                    return True
                
                if move[1] == self.tabled[1] and self.high_suit(move[2], self.tabled[2]) == move[2]:
                    return True
                
        if move[0] == self.tabled[0] == "Straight" and move[1] > self.tabled[1]:
            return True
        
        return False
    
    # calculate_points(self)
    # Calculates the points for each player at the end of the round

    def calculate_points(self):
        cumulative = 0

        for (index, player) in enumerate(self.players):
            multiplier = 1

            if self.tabled[0] in ["Straight flush", "Four of a kind"] or self.tabled[0:2] == ("High card", 2):
                multiplier *= 2
            
            if len(player) >= 10:
                multiplier *= 2

            for card in player:
                if card[0] % 13 == 2:
                    multiplier *= 2

                if card[0] <= 10 and (card[0] + 1, card[1]) in player and (card[0] + 2, card[1]) in player and (card[0] + 3, card[1]) in player and (card[0] + 4, card[1]) in player:
                    multipier *= 2

                if (card[0], "hearts") in player and (card[0], "diamonds") in player and (card[0], "spades") in player and (card[0], "clubs") in player:
                    multiplier *= 2
            
            self.points[index] -= len(player) * multiplier
            cumulative += len(player) * multiplier

        self.points[self.turn % 4] += cumulative

    # play(self)
    # Verifies whether a proposed move is valid and applies it if it is
        
    def play(self, move):
        hand = self.players[self.turn % 4]

        if move == "pass":
            self.passed += 1

            if self.passed == 3:
                self.tabled = ()
                self.passed = 0

            self.turn += 1
        else:
            contained = True

            for i in move:
                contained = i in hand and contained

            if contained and len(move) == len(set(move)):
                if self.valid(move):
                    for i in move:
                        self.players[self.turn % 4].remove(i)

                    self.tabled = self.move_type(move)
                    self.passed = 0

                    if len(self.players[self.turn % 4]) == 0:
                        if self.round >= 8:
                            sys.exit()
                        else:
                            self.calculate_points()
                            print(self.points)

                            self.turn = 0
                            self.tabled = ()
                            self.round += 1
                            self.deal()
                    else:
                        self.turn += 1


game = Game()

while True:
    print("Tabled:", game.tabled)
    print("Your Hand:", game.players[game.turn % 4])

    try:
        y = input()

        if y == "pass":
            game.play(y)
        else:
            move = y.split(";")

            for (index, card) in enumerate(move):
                x = card.strip().split(" of ")
                x[0] = int(x[0])
                move[index] = tuple(x,)

            print(move)

            game.play(move)
    except KeyboardInterrupt:
        sys.exit()
    except ValueError:
        pass

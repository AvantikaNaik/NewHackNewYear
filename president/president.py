import sys
from cards import Card
from cards import Player
from cards import Deck


class President():
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.deal(self.players)
        self.currentBoard = []
    
    def playSingleTurn(self, player):
        print("Here is your hand: ")
        player.displayHand()

        print("\n Which card do you want to play?")
        val = input("Card value: ")
        suite = input("Card suite: ")
        card = Card(val, suite)
        if card in player.hand:
            if card.value >= currentBoard[len(currentBoard) - 1]:
                currentBoard.append(card)
            else:
                print("You can't play this card")
                return 1
        else:
            print("This card isn't in your hand")
            return 1
        return 0

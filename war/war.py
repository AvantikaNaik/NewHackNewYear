import sys
from cards import Deck
from cards import Card
from cards import Player


class War:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.deal(self.players)




currentBoard = []
for player in players:
    currentBoard.append(player.drawFromHand())

maxValue = 0
for card in currentBoard:
    if card.value > maxValue:
        maxValue = card.value




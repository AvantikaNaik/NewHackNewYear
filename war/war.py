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
        

    def playRound(self):
        currentBoard = []
        for player in self.players:
            currentBoard.append((player, player.drawFromHand()))
        maxValue = currentBoard[0]
        for player, card in currentBoard:
            if card.value > int(maxValue[1].value):
                maxValue = (player, card)

        counter = 0
        for player, card in currentBoard:
            if card.value == maxValue[1].value:
                counter += 1
        if counter > 1:
            self.playRound()
        return maxValue[0]

            










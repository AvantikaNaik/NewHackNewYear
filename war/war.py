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

        print("Current board: ")
        for player, card in currentBoard:
            print(str(player.name) + " played a " + str(card.value) + " of " + str(card.suite))

        maxValue = currentBoard[0]
        for player, card in currentBoard:
            if card.value > int(maxValue[1].value):
                maxValue = (player, card)
        
        for card in currentBoard:
            maxValue[0].addToPile(card)
        print("Winner: " + maxValue[0].name + " with a " + str(maxValue[1].value) + " of " + str(maxValue[1].suite))

    def winners(self):
        winners = []
        maxPileLength = 0
        for player in self.players:
            if len(player.pile) > maxPileLength:
                maxPileLength = len(player.pile)
        for player in self.players:
            if maxPileLength == len(player.pile):
                winners.append(player)
        return winners
        

            










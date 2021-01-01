import sys
from cards import Deck
from cards import Card
from cards import Player

players = []
for i in range(1, len(sys.argv)):
    players.append(Player(str(sys.argv[i])))

deck = Deck()
deck.shuffle()
deck.deal(players)



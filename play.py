import sys
from war import War
from cards import Player
from cards import Deck
from cards import Card


players = []
for i in range(1, len(sys.argv)):
    players.append(Player(str(sys.argv[i])))
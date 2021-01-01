import sys
from cards import Player
from cards import Deck
from cards import Card
sys.path.append('war')
from war import War


players = []
for i in range(1, len(sys.argv)):
    players.append(Player(str(sys.argv[i])))

game = War(players)
for player in players:
    print(player.name, len(player.hand))




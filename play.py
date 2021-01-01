import sys
from cards import Player
from cards import Deck
from cards import Card
sys.path.append('war')
from war import War

print("Games to play: War")
game = input("What game do you want to play?\n")
if game == "War":
    players = []

    print("LET'S PLAY WAR! ENTER 1 TO EXIT! ENTER PLAYERS:")
    name = ""
    while not name == "1":
        name = input()
        if not name == "1":
            players.append(Player(name))
    print("HERE ARE YOUR PLAYERS:")
    for player in players:
        print(player.name)


    game = War(players)
    while len(players[0].hand) > 0:
        nextMove = input("Enter 'move' to make the next move, enter 'hands' to check how many cards are in each player's hands,\n or enter 'piles' to see how many cards are in each player's piles.\n")
        if nextMove == "move":
            game.playRound()
        elif nextMove == "hands":
            for player in players:
                print(player.name + " has " + str(len(player.hand)) + " cards left.")
        elif nextMove == "piles":
            for player in players:
                print(player.name + " has " + str(len(player.pile)) + " cards in their discard pile.")
        else:
            print("Not a valid move")
        print("\n\n\n")
    print("Here are the winners: ")
    for player in game.winners():
        print(player.name + " with " + str(len(player.pile)) + " cards in their pile.")







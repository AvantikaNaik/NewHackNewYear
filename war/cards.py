import random

#Card object
class Card:

    #Initialize value and suit
    def __init__(self, value, suite):
        self.value = value
        self.suite = suite
    
    #Display a card
    def displayCard(self):
        print(str(self.value) + " of " + str(self.suite))


#Deck object
class Deck:

    #Initalize with array of cards in deck
    def __init__(self):
        self.cards = []
        self.create()

    #Create a new deck of cards
    def create(self):
        suites = ["Spades", "Clubs", "Diamonds", "Hearts"]
        for suite in suites:
            for value in range(1, 14):
                self.cards.append(Card(value, suite))

    #Display all cards in deck
    def displayCards(self):
        for card in self.cards:
            card.displayCard()

    #Shuffle card deck
    def shuffle(self):
        tempDeck = []
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            tempDeck.append(self.cards[r])
            self.cards.pop(r)

        self.cards = tempDeck
    
    #Draw a card from the deck
    def drawCard(self):
        return self.cards.pop()

    def deal(self, players):
        counter = 1
        while len(self.cards) > 0:
            players[(counter % len(players))].drawFromDeck(self)
            counter += 1


#Player object
class Player:

    #Initialize with name, hand, and pile
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.pile = []
    
    #Draw from deck and add to hand of player
    def drawFromDeck(self, deck):
        self.hand.append(deck.drawCard())
        return self
    
    #Display hand of player
    def displayHand(self):
        for card in self.hand:
            card.displayCard()
    
    #Draw from player's hand
    def drawFromHand(self):
        return self.hand.pop()

    #Add to player's discard pile
    def addToPile(self, card):
        self.pile.append(card)
    
    #Display player's discard pile
    def displayPile(self):
        for card in self.pile:
            card.displayCard()
    
    
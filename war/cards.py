import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def displayCard(self):
        print(str(self.value) + " of " + str(self.suit))

class Deck:
    def __init__(self):
        self.cards = []
        self.create()

    def create(self):
        suites = ["Spades", "Clubs", "Diamonds", "Hearts"]
        for suite in suites:
            for value in range(1, 14):
                self.cards.append(Card(suite, value))

    def displayCards(self):
        for card in self.cards:
            card.displayCard()

    def shuffle(self):
        tempDeck = []
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            tempDeck.append(self.cards[r])
            self.cards.pop(r)

        self.cards = tempDeck
    
    def drawCard(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.pile = []
    
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self
    
    def displayHand(self):
        for card in self.hand:
            card.displayCard()

    def addToPile(self, card):
        self.pile.append(card)
    




deck = Deck()
deck.shuffle()

nithya = Player("Nithya")

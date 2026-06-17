import card
import random as rnd
class Deck:
    def __init__(self,DeckAmount):
        self.DeckAmount = DeckAmount
        self.DeckSize=52
        self.fill()
    def shuffle(self):
        self.fill()
        rnd.shuffle(self.cards)
    def fill(self):
        self.cards=[]
        for j in range(self.DeckAmount):
            for i in range(1, self.DeckSize + 1):
                self.cards.append(card.Card(i))
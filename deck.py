"""plik przechowujący klasę Deck"""
import card
import random as rnd
class Deck:
    """klasa przechowująca listę kart(Card), do inicjalizacji pobiera ilość talii kart jaką rozgrywana jest gra"""
    def __init__(self,DeckAmount):
        self.DeckAmount = DeckAmount
        self.DeckSize=52
        self.cards=[]
        self.fill()
    def shuffle(self):
        """uzupełnia i tasuje listę kart"""
        self.fill()
        rnd.shuffle(self.cards)
    def fill(self):
        """wypełnia listę kart uporządkowanymi kartami"""
        self.cards=[]
        for j in range(self.DeckAmount):
            for i in range(1, self.DeckSize + 1):
                self.cards.append(card.Card(i))
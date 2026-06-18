"""plik przechowujący klasę player. obiektem tej klasy jest zarówno gracz jak i krupier"""
import hand
class Player:
    def __init__(self,name,balance=0):
        self.hands=[]
        self.name = name
        self.balance=balance
        self.hands.append(hand.Hand())
        self.activeHandIndex=0
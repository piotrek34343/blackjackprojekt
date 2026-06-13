import hand
class Player:
    def __init__(self,name,balance=0):
        self.hands=[]
        self.name = name
        self.balance=balance
    def addHand(self,hand):
        self.hands.append(hand)
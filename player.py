import hand
class Player:
    def __init__(self,name,balance=0):
        self.hands=[]
        self.name = name
        self.balance=balance
        self.addHand(hand.Hand())
        self.activeHandIndex=0
    def addHand(self,hand):
        self.hands.append(hand)
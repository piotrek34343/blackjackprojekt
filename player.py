import hand
class Player:
    def __init__(self,name):
        self.hands=[]
        self.name = name
    def addHand(self,hand):
        self.hands.append(hand)
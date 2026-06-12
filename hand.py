import card
import deck
class Hand():
    def __init__(self):
        self.cards=[]
        self.isBusted=0
    def updateValue(self):
        self.value=0
        for i in self.cards:
            self.value+=i.value
    def drawFrom(self,Deck=[]):
        if len(Deck.cards)==0:
            Deck.shuffle()
        self.cards.append(Deck.cards.pop())
        self.updateValue()
        if (self.value>21):
            self.isBusted=1
    def setWager(self,wager):
        self.wager=wager
    def show(self,type="full"):
        if type=="full":
            handSummary=""
            for i in self.cards:
                handSummary=handSummary + i.name+","
            handSummary=handSummary+"total value:"+str(self.value)
            return handSummary
        else:
            handSummary=str(self.cards[0].name)+",hidden card,"
            return handSummary
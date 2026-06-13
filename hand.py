import card
import deck
class Hand():
    def __init__(self):
        self.cards=[]
        self.isBusted=0
        self.wager=0
        self.aces=0
        self.acesUsed=0
        self.value=0
    def updateValue(self):
        self.value=0
        for i in self.cards:
            self.value+=i.value
        self.value+=(self.aces*10)
    def drawFrom(self,Deck=[]):
        if len(Deck.cards)==0:
            Deck.shuffle()
        self.cards.append(Deck.cards.pop())
        if self.cards[-1].value==1:
            self.aces+=1
        self.updateValue()
        if (self.value>21):
            if self.aces!=0:
                self.aces-=1
                self.updateValue()
            else:
                self.isBusted=1
    def setWager(self,wager):
        self.wager=wager
    def show(self,type="full"):
        if type=="full":
            soft=""
            if self.aces!=0 and self.value!=21:
                soft="soft"
            handSummary=""
            for i in self.cards:
                if self.wager:
                    handSummary=handSummary + i.name+","
                else:
                    handSummary = handSummary + i.name + ","
            handSummary=handSummary+"total value: "+soft+" "+str(self.value)
            return handSummary
        else:
            handSummary=str(self.cards[0].name)+",hidden card,"
            return handSummary
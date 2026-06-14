import card
import deck
import player
class Hand():
    def __init__(self):
        self.cards=[]
        self.isBusted=False
        self.result=0
        self.wager=0
        self.aces=0
        self.value=0
        self.insurance=False
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
                self.isBusted=True
    def setWager(self,wager):
        self.wager=wager
    def show(self,type="full"):
        if type=="full":
            note=""
            if self.aces!=0 and self.value!=21:
                note=" soft"
            elif self.value==21 and len(self.cards)==2:
                note=" BLACKJACK!!!"
            elif self.isBusted==True:
                note=" BUSTED!!!"
            handSummary=""
            for i in self.cards:
                if self.wager:
                    handSummary=handSummary + i.name+","
                else:
                    handSummary = handSummary + i.name + ","
            handSummary=handSummary+"total value: "+str(self.value)+note
        else:
            handSummary=str(self.cards[0].name)+",hidden card"
        return handSummary
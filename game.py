from unittest import case
import card
import deck
import hand
import player
import config as cfg
class Game:
    def __init__(self):
            self.Deck = deck.Deck(cfg.numberOfDecks)
            self.Deck.shuffle()
            self.participants = []
            self.participants.append(player.Player("dealer"))
            if cfg.numberOfPlayers == 1:
                self.participants.append(player.Player("player", 1000))
            else:
                for i in range(cfg.numberOfPlayers):
                    self.participants.append(player.Player("player" + str(i + 1)))
            self.Deck.cards.append(card.Card(1))
            self.Deck.cards.append(card.Card(14))
            self.Deck.cards.append(card.Card(26))
            self.Deck.cards.append(card.Card(40))
    def roundStart(self):
        for j in self.participants:
            j.addHand(hand.Hand())
            for i in j.hands:
                i.drawFrom(self.Deck)
                i.drawFrom(self.Deck)
                if j.name != "dealer":
                    stawka = int(input(j.name+" stawka:"))
                    while stawka > j.balance:
                        print("za malo srodkow")
                        stawka = int(input("stawka:"))
                    i.wager=stawka
                    j.balance-=stawka
        self.showAll("player")
    def showAll(self,turn="player"):
        print("===============================================================")
        if turn=="player":
            for j in self.participants:
                for i in j.hands:
                    handIterator = ""
                    if len(j.hands) > 1:
                        handIterator = "Hand" + str(j.hands.index(i)+1)
                    print("\n" + j.name+" "+handIterator)
                    if j.name == "dealer":
                        print(i.show("half"))
                    else:
                        print("stan konta:"+str(j.balance))
                        print("stawka:"+str(i.wager))
                        print(i.show("full"))
        else:
            for j in self.participants:
                for i in j.hands:
                    print("\n" + j.name)
                    if j.name != "dealer":
                        print("stawka:"+str(i.wager))
                    print(i.show("full"))
    def printBalances(self):
        if len(self.participants) == 2:
            print("stan konta:" + str(self.participants[1].balance))
        #w razie dopuszczenia trybu wielu graczy tutaj else i pokazanie listy
    def showResults(self):
        for j in self.participants:
            if j.name != "dealer":
                for i in j.hands:
                    wygrana = i.result * i.wager
                    if i.insurance and self.participants[0].hands[0].cards[1].value == 10:
                        wygrana += (i.wager * 1.5)
                    j.balance += wygrana
                    print(j.name + " wygrana= " + str(wygrana))
    def playerTurn(self,Hand,Player):
        #1-pass, 2-dobierz, 3-double,4-split,5-insurance
        Index = Player.hands.index(Hand) + 1
        if Hand.value==21:
            choice ="pass"
        else:
            possibilities=["pass","hit"]
            if len(Hand.cards)==2:
                if Player.balance>=Hand.wager:
                    possibilities.append("double")
                    if len(Player.hands)<(cfg.allowedSplits+1):
                        if cfg.splitSameValue==1:
                            if Hand.cards[1].value==Hand.cards[0].value:
                                possibilities.append("split")
                        else:
                            if Hand.cards[1].rank==Hand.cards[0].rank:
                                possibilities.append("split")
            if self.participants[0].hands[0].cards[0].value==1 and Player.balance>=(Hand.wager*0.5) and len(Player.hands)==1:
                possibilities.append("insurance")
            print(possibilities)
            if len(Player.hands)>1:
                prompt="(Hand"+str(Index)+")wybór:"
            else:
                prompt="wybór:"
            choice=str(input(prompt))
        match choice:
            case "pass":
                return 1
            case "hit":
                Hand.drawFrom(self.Deck)
                Hand.updateValue()
                self.showAll("player")
                if Hand.isBusted==False:
                    return self.playerTurn(Hand,Player)
                else:
                    return 1
            case "double":
                Player.balance -= Hand.wager
                Hand.wager+=Hand.wager
                Hand.drawFrom(self.Deck)
                Hand.updateValue()
                self.showAll("player")
                return 1
            case "split":
                newHand=hand.Hand()
                newHand.wager=Hand.wager
                Player.balance-=Hand.wager
                Player.hands.insert(Index,newHand)
                Player.hands[Index].drawFrom(Hand)
                Hand.drawFrom(self.Deck)
                Player.hands[Index].drawFrom(self.Deck)
                Hand.updateValue()
                Player.hands[Index].updateValue()
                self.showAll( "player")
                return self.playerTurn(Hand,Player)
            case "insurance":
                return self.insuranceCheck(Player)
    def insuranceCheck(self,Player):
        if self.participants[0].hands[0].cards[1].value==10:
            print("dealer ma blackjacka")
            Player.balance +=Player.hands[0].wager
            return 1
        else:
            print("dealer nie ma blackjacka")
            Player.balance -= 0.5 * Player.hands[0].wager
            return self.playerTurn(Player.hands[0].wager,Player)




    def dealerTurn(self):
        Hand=self.participants[0].hands[0]
        self.showAll("dealer")
        if Hand.value<=16:
            choice ="hit"
        elif Hand.aces!=0 and Hand.value==17:
            choice ="hit"
        else:
            choice ="pass"
        match choice:
            case "pass":
                return 1
            case "hit":
                Hand.drawFrom(self.Deck)
                Hand.updateValue()
                self.showAll("dealer")
                if Hand.isBusted == False:
                    return self.dealerTurn()
    def checkResult(self):
        players=self.participants[1:]
        dealer=self.participants[0].hands[0]
        if dealer.isBusted==False:
            for j in players:
                for i in j.hands:
                    if i.isBusted==True:
                        i.result=0
                    elif i.value==dealer.value:
                        i.result=1
                    elif i.value==21 and len(i.cards)==2:
                        i.result=5/2
                    elif i.value>dealer.value:
                        i.result=2
                    else:
                        i.result=0
        else:
            for j in players:
                for i in j.hands:
                    if i.value == 21 and len(i.cards) == 2:
                        i.result = 5 / 2
                    if i.isBusted==True:
                        i.result=0
                    else:
                        i.result=2


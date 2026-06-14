from unittest import case
import deck
import hand
import player
class Game:
    def __init__(self,Deck):
            self.Deck = Deck
    def roundStart(self,participants,Deck):
        for j in participants:
            j.addHand(hand.Hand())
            for i in j.hands:
                i.drawFrom(Deck)
                i.drawFrom(Deck)
                if j.name != "dealer":
                    stawka = int(input(j.name+" stawka:"))
                    while stawka > j.balance:
                        print("za malo srodkow")
                        stawka = int(input("stawka:"))
                    i.wager=stawka
                    j.balance-=stawka
        self.showAll(participants,"player")
    def showAll(self,participants,turn="player"):
        print("===============================================================")
        if turn=="player":
            for j in participants:
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
            for j in participants:
                for i in j.hands:
                    print("\n" + j.name)
                    if j.name != "dealer":
                        print("stawka:"+str(i.wager))
                    print(i.show("full"))
    def playerTurn(self,Deck,Hand,Player,participants):
        #1-pass, 2-dobierz, 3-double,4-split,5-insurance
        Index = Player.hands.index(Hand) + 1
        if Hand.value==21:
            choice ="pass"
        else:
            possibilities=["pass","hit"]
            if len(Hand.cards)==2:
                if Player.balance>=Hand.wager:
                    possibilities.append("double")
                    if Hand.cards[1].rank==Hand.cards[0].rank:#zmienic rank na value jesli zdecydujemy sie na to zeby pozwolic splitowac np jopek-król
                        possibilities.append("split")
            if participants[0].hands[0].cards[0]==1:
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
                Hand.drawFrom(Deck)
                Hand.updateValue()
                self.showAll(participants,"player")
                if Hand.isBusted==False:
                    return self.playerTurn(Deck,Hand,Player,participants)
                else:
                    return 1
            case "double":
                Player.balance -= Hand.wager
                Hand.wager+=Hand.wager
                Hand.drawFrom(Deck)
                Hand.updateValue()
                self.showAll(participants, "player")
                return 1
            case "split":
                newHand=hand.Hand()
                newHand.wager=Hand.wager
                Player.balance-=Hand.wager
                Player.hands.insert(Index,newHand)
                Player.hands[Index].drawFrom(Hand)
                Hand.drawFrom(Deck)
                Player.hands[Index].drawFrom(Deck)
                Hand.updateValue()
                Player.hands[Index].updateValue()
                self.showAll(participants, "player")
                return self.playerTurn(Deck,Hand,Player,participants)
            case "insurance":
                Player.balance-=0.5*Hand.wager
                Hand.insurance=True
                self.showAll(participants, "player")
                return self.playerTurn(Deck,Hand,Player,participants)




    def dealerTurn(self,Deck,participants):
        Hand=participants[0].hands[0]
        self.showAll(participants, "dealer")
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
                Hand.drawFrom(Deck)
                Hand.updateValue()
                self.showAll(participants, "dealer")
                if Hand.isBusted == False:
                    return self.dealerTurn(Deck,participants)
    def checkResult(self,Deck,participants):
        players=participants[1:]
        dealer=participants[0].hands[0]
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


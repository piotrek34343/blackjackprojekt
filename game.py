"""plik zawierający logikę gry"""
import card
import deck
import hand
import player
import config as cfg
class Game:
    def __init__(self):
            self.Deck = deck.Deck(cfg.numberOfDecks)
            self.Deck.shuffle()
            self.Deck.cards.append(card.Card(6))
            self.Deck.cards.append(card.Card(1))
            self.Deck.cards.append(card.Card(6))
            self.Deck.cards.append(card.Card(1))
            self.Deck.cards.append(card.Card(0))
            self.participants = []
            self.participants.append(player.Player("dealer"))
            self.message=''
            if cfg.numberOfPlayers == 1:
                self.participants.append(player.Player("player", 1000))
            else:
                for i in range(cfg.numberOfPlayers):
                    self.participants.append(player.Player("player" + str(i + 1)))
    def roundStart(self,selectedbet):
        """rozdaje po dwie karty kazdemu obiektowi player w game,
        ustawia zakład gracza i odejmuje kwotę od salda"""
        self.message="rozpoczęto rundę"
        for j in self.participants:
            for i in j.hands:
                i.drawFrom(self.Deck)
                i.drawFrom(self.Deck)
                if j.name.lower() != "dealer":
                    i.wager= selectedbet
                    j.balance-= selectedbet
    def showResults(self):
        """przekazuje wyniki gry do self.message"""
        wygrana =0
        self.message=""
        for j in self.participants:
            if j.name != "dealer":
                for i in j.hands:
                    wygrana += i.result * i.wager
                    if i.result==5/2:
                        self.message="BLACKJACK!!!!!!!!!! "
                j.balance += wygrana
                self.message+="całkowita wygrana= " + str(wygrana)
    def updatePossibilites(self,Hand,Player):
        """odświeża możliwości zapisane w Hand należacym do Player"""
        Hand.possibilities = ["pass", "hit"]
        if len(Hand.cards) == 2:
            if Player.balance >= Hand.wager:
                Hand.possibilities.append("double")
                if len(Player.hands) < (cfg.allowedSplits + 1):
                    if cfg.splitSameValue == 1:
                        if Hand.cards[1].value == Hand.cards[0].value:
                            Hand.possibilities.append("split")
                    else:
                        if Hand.cards[1].rank == Hand.cards[0].rank:
                            Hand.possibilities.append("split")
        if self.participants[0].hands[0].cards!=[]:
            if self.participants[0].hands[0].cards[1].value == 1 and Player.balance >= (Hand.wager * 0.5) and len(Player.hands) == 1 and not Hand.isFinished and len(Hand.cards)==2:
                Hand.possibilities.append("insurance")
    def playerTurn(self,Hand,Player,choice):
        """wykonuje choice(hit/pass/double/split/insurance) na obiekcie Hand gracza Player"""
        Index = Player.hands.index(Hand) + 1
        if Hand.value==21:
            choice ="pass"
        match choice:
            case "pass":
                Hand.isFinished=True
            case "hit":
                Hand.drawFrom(self.Deck)
                Hand.updateValue()
                if Hand.isBusted==True:
                    Hand.isFinished=True
            case "double":
                Player.balance -= Hand.wager
                Hand.wager+=Hand.wager
                Hand.drawFrom(self.Deck)
                Hand.updateValue()
                Hand.isFinished=True
            case "split":
                newHand=hand.Hand()
                newHand.insurancePossible=Hand.insurancePossible
                newHand.wager=Hand.wager
                Player.balance-=Hand.wager
                Player.hands.insert(Index,newHand)
                Player.hands[Index].drawFrom(Hand)
                Hand.drawFrom(self.Deck)
                Player.hands[Index].drawFrom(self.Deck)
                Hand.updateValue()
                Player.hands[Index].updateValue()
            case "insurance":
                return self.insuranceCheck(Player)
    def insuranceCheck(self,Player):
        """rozstrzyga ubezpieczenie. przekazuje wynik do self.message i zmienia saldo Player zaleznie od wyniku"""
        Player.hands[0].insurancePossible=False
        if self.participants[0].hands[0].cards[0].value==10:
            self.message="dealer ma blackjacka, gracz wygrywa "+ str(Player.hands[0].wager)
            Player.balance +=Player.hands[0].wager
            Player.hands[0].isFinished=True
        else:
            self.message="dealer nie ma blackjacka, gra toczy sie dalej"
            Player.balance -= 0.5 * Player.hands[0].wager
            return self.playerTurn(Player.hands[0],Player,False)
    def dealerTurn(self):
        """wykonuje CAŁĄ turę krupiera(w przeciwieństwie do playerTurn które wykonuje jeden ruch)"""
        Hand=self.participants[0].hands[0]
        if Hand.value<=16:
            choice ="hit"
        elif Hand.aces!=0 and Hand.value==17 and cfg.dealerHitOnSoft17:
            choice ="hit"
        else:
            choice ="pass"
        match choice:
            case "pass":
                return 1
            case "hit":
                Hand.drawFrom(self.Deck)
                Hand.updateValue()
                if Hand.isBusted == False:
                    return self.dealerTurn()
    def checkResult(self):
        """zapisuje wynik(w postaci proporcji stawki do wygranej) do każdego obiektu hand należącego do gracza"""
        players=self.participants[1:]
        dealer=self.participants[0].hands[0]
        if dealer.isBusted==False:
            for j in players:
                for i in j.hands:
                    if i.isBusted==True:
                        i.result=0
                    elif i.value==dealer.value:
                        i.result=1
                    elif i.value==21 and len(i.cards)==2 and(len(j.hands)==1 or cfg.bjAfterSplit):
                        i.result=5/2
                    elif i.value>dealer.value:
                        i.result=2
                    else:
                        i.result=0
        else:
            for j in players:
                for i in j.hands:
                    if i.value == 21 and len(i.cards) == 2 and(len(j.hands)==1 or cfg.bjAfterSplit):
                        i.result = 5 / 2
                    elif i.isBusted:
                        i.result=0
                    else:
                        i.result=2
    def roundEnd(self):
        """resetuje ręce wszystkich uczestników"""
        for j in self.participants:
            j.hands=[hand.Hand()]

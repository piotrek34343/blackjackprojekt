import card
import deck
import hand
import player
import game as g
numberOfPlayers=1
Deck=deck.Deck(1)
Deck.shuffle()
Deck.cards.append(card.Card(1))
Deck.cards.append(card.Card(14))
Deck.cards.append(card.Card(26))
Deck.cards.append(card.Card(40))
participants = []
participants.append(player.Player("dealer"))
if numberOfPlayers == 1:
    participants.append(player.Player("player",1000))
else:
    for i in range(numberOfPlayers):
        participants.append(player.Player("player"+str(i+1)))
game=input("zaczac gre?")
while(game=="tak"):
    #zaczela sie runda
    g.roundStart(participants,Deck)
    for j in participants:
        if j.name != "dealer":
            for i in j.hands:
                g.playerTurn(Deck,i,j,participants)
    g.dealerTurn(Deck,participants)
    g.checkResult(Deck,participants)
    for j in participants:
        if j.name != "dealer":
            for i in j.hands:
                wygrana=i.result*i.wager
                if i.insurance and participants[0].hands[0].cards[1].value==10:
                    wygrana+=(i.wager*1.5)
                j.balance+=wygrana
                print(j.name+" wygrana= "+str(wygrana))
    if numberOfPlayers == 1:
        print("stan konta:"+str(participants[1].balance))
    game = input("zaczac kolejna runde?")
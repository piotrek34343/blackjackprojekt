import card
import deck
import hand
import player
import functions as f
numberOfPlayers=1
participants=[]
wagers=[]
participants.append(player.Player("dealer"))
if numberOfPlayers == 1:
    participants.append(player.Player("player"))
    wagers.append(25)
else:
    for i in range(numberOfPlayers):
        participants.append(player.Player("player"+str(i+1)))
        wagers.append(25)
wagers.reverse()
Deck=deck.Deck(1)
Deck.shuffle()
Deck.cards.append(card.Card(6))
Deck.cards.append(card.Card(5))
Deck.cards.append(card.Card(1))
Deck.cards.append(card.Card(1))
#for i in range(1,Deck.DeckSize+1):
#   print(Deck.cards.pop().name)
#zaczela sie runda
f.roundStart(participants,Deck,wagers)
for j in participants:
    if j.name != "dealer":
        for i in j.hands:
            f.playerTurn(Deck,i,j,participants)
f.dealerTurn(Deck,participants)
f.checkResult(Deck,participants)
for j in participants:
    if j.name != "dealer":
        for i in j.hands:
            print(j.name+" wygrywa "+str(i.result*i.wager))
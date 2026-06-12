import card
import deck
import hand
import player
import hand
participants=[]
dealer=player.Player("dealer")
player1=player.Player("player")
participants.append(dealer)
participants.append(player1)
Deck=deck.Deck(1)
Deck.shuffle()

#for i in range(1,Deck.DeckSize+1):
#   print(Deck.cards.pop().name)
#zaczela sie runda
player1.addHand(hand.Hand())
dealer.addHand(hand.Hand())
for j in participants:
    for i in j.hands:
        i.drawFrom(Deck)
        i.drawFrom(Deck)
for j in participants:
    for i in j.hands:
        print("\n"+j.name+":")
        if j.name=="dealer":
            print(i.show("half"))
        else:
            print(i.show("full"))
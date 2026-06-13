import card
import deck
import hand
import player
import functions as f
numberOfPlayers=1
participants=[]
wagers=[]
participants.append(player.Player("dealer"))
for i in range(numberOfPlayers):
    participants.append(player.Player("player"+str(i+1)))
    wagers.append(25)
wagers.reverse()
Deck=deck.Deck(1)
Deck.shuffle()

#for i in range(1,Deck.DeckSize+1):
#   print(Deck.cards.pop().name)
#zaczela sie runda
f.roundStart(participants,Deck,wagers)
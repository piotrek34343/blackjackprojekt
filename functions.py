import hand

def roundStart(participants,Deck,wagers):
    for j in participants:
        j.addHand(hand.Hand())
        for i in j.hands:
            i.drawFrom(Deck)
            i.drawFrom(Deck)
    for j in participants:
        for i in j.hands:
            print("\n" + j.name)
            if j.name == "dealer":
                print(i.show("half"))
            else:
                i.setWager(wagers.pop())
                print("stawka:"+str(i.wager))
                print(i.show("full"))
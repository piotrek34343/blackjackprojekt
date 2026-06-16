import game as g
playerStartInput=input("zaczac gre?")
Game=g.Game()
while(playerStartInput=="tak"):
    #zaczela sie runda
    Game.roundStart()
    for j in Game.participants:
        for i in j.hands:
            if j.name != "dealer":
                Game.playerTurn(i,j)
    Game.dealerTurn()
    Game.checkResult()
    Game.showResults()
    playerStartInput = input("zaczac kolejna runde?")
"""plik z ustawieniami które można dostosować(sporne reguły,preferencje).
Zostawiłem w nim ustawienia które nie są jeszcze zaimplementowane z nadzieją że uda mi się je zaimplementować
 przed oddaniem projektu"""
#można zmieniać:
splitSameValue=1 #decyduje o tym, czy mozna splitowac np dama-jopek(ustawienie na zero pozwala wylacznie na splitowanie par z tym samym symbolem)
numberOfDecks=1 #ilosc talii w grze
bjAfterSplit=0 # decyduje o tym czy po splicie mozna dostac wyplate 3 do 2 za blackjack
betStep=10 #ilosc o jaką zwieksza/zmniejsza sie zaklad
dealerHitOnSoft17=True #decyduje o tym czy dealer dobiera na miękkiej 17
notifySoft=False #czy informacja o ręce powinna informowac o "miękkim" wyniku?
#nie zmieniać(nyi)
allowedSplits=1 #dozwolona ilość splitów w jednej rundzie(dostosowac pozniej na podstawie mozliwosci ui)
numberOfPlayers=1 # tryb wielu graczy nie jest zaimplementowany

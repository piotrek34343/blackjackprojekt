class Card(object):
    def __init__(self,id):
        self.id = id
        self.suit =(id-1)//13
        self.rank = id%13
        match self.rank:
            case 1:
                self.value=1
                self.name="As "
            case 11:
                self.value=10
                self.name="Jopek "
            case 12:
                self.value=10
                self.name="Dama "
            case 0:
                self.value=10
                self.name="Krol "
            case _:
                self.name=str(self.rank)+" "
                self.value=self.rank
        match self.suit:
            case 0:
                self.name+= "Kier"
            case 1:
                self.name+= "Karo"
            case 2:
                self.name+= "Trefl"
            case 3:
                self.name+= "Pik"
    def __str__(self):
        return self.name
p1 = Pocasi(31,Pocasicko,SLUNECNO,25,14)
p1 = setPovetrnostniPodminky(pocasicko.ZATAZENO)
print(p1)

from enum import Enum
class Pocasicko(Enum):
    SLUNECNO = "Slunecno"
    ZATAZENO = "Zatazeno"
    BOURKA = "Bourka"
    SNIH = "Snih"

class Pocasi:
    def __init__(self,vitr,povetrnostniPodminky
        self.vitr = vitr
        self.povetrnostniPodminky = povetrnostniPodminky
        self.teplota = teplota
        self.vlhkost = vlhkost

    def getVitr(self):
        return self.vitr
    def setVitr(self,vitr):
        self.vitr = vitr
    def getPovetrnostniPodminky(self):
        return self.povetrnostniPodminky.value
    def setPovetrnostniPodminky(self,povetrnostniPodminky):
        self.povetrnostniPodminky = povetrnostniPodminky
    def getTeplota(self):

class Utulek:
    def __init__(self,Nazev:str,maxCapacity: int, seznamZvirat = None):
        self.Nazev = Nazev
        self.maxCapacity = maxCapacity
        if seznamZvirat is None:
            self.SeznamZvirat = []
        else:
            self.seznamZvirat = seznamZvirat

    def getNazev(self):
        return self.Nazev
    def getMaxKapacita(self):
        return self.MaximalniKapacita
    def getSeznamZvirat(self):
        return self.SeznamZvirat
    def pridatZvire(self,zvire:Zvire):
        if len(self.seznamZvirat) >= self.maxCapacity or zvire in self.seznamZvirat:
            print("Presazena kapacita utulku")
        else:
            self.seznamZvirat.append(zvire)
    def odeberZvire(self,zvire:Zvire):
        if zvire in self.seznamZvirat:
            
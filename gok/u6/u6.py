class Patient:
    def __init__(self, name:str,surname:str,birth_number:int,weight:float,height:int):
        self.name=name
        self.surname=surname
        self.birth_number=birth_number
        self.weight=weight
        self.height=height
        self.bmi=None
    # Getters
    def get_name(self):
        return self.name
    def get_surname(self):
        return self.surname
    def get_weight(self):
        return self.weight
    def get_height(self):
        return self.height
    # Setters
    def set_name(self,name:str):
        self.name=name
    # Methods
    def gain_weight(self,val:float):
        self.weight+=val
    def lose_weight(self,val:float):
        self.weight-=val
    def get_BMI(self):
        self.bmi=self.weight/((self.height/100)**2)
        return self.bmi
    # toString()
    def to_string(self):
        return f"Patient jmenem:{self.name} {self.surname}\
ma rodne cislo:{self.birth_number} meri: {self.height}cm a vazi: {self.weight}kg"

if __name__=="__main__":
    pass
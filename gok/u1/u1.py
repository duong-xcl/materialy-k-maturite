# importovani nahodnych funkci
    # pouzivat
import random
import random as rnd

    # nepouzivat
        # from random import randint
        # from random import randint as rndint

# Uloha 1 definujte ID list, naplnte ho 5 hodnotami a vypiste

# 1. Fce, ktera naplni list X nahodnymi hodnotami a vrati jej. V mainu jej pak printnu
    # Upravte funkci tak, ze muzete pomoci vstup. argumentu zmenit rozmezi hodnot

if __name__=="__main__":
    l1=list([0,1,2,3,4])
    l2=[4,3,2,1,0]
    print (l1)
    print (l2)
    pass

if __name__=="__main__":
    #print(random.randint(0,9))
    # for loopem vypiste 10 nahodnych cisel
    for i in range (0,10,1):
        print(random.randint(0,9),end=" ")
    pass

print("")

def fce10(x,a,b):
    return [random.randint(a,b) for i in range(x)]

if __name__=="__main__":
    for i in range(0,10):
        print(random.randint(0,9),end=" ")
    pass

# 2. Fce, ktera prijima list z fce1, kazdou sudou hodnotu vynasobi 2 a ke kazde liche hodnotu pricte 2
# vypiste list y fce 1 i z dce 2 a porovnejte spravnost

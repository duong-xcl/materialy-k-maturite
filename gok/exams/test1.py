import random
import random as rnd

# uloha 1
if __name__=="__main__":
    l1=list([0,1,2,3,4])
    print (l1)

# uloha 2
    for i in range (0,1,1):
        for j in range (0,5,1):
            print (l1)
# uloha 3
    for i in range (0,10,1):
        l2=print(random.randint(5,9),end=" ")

    print(" ")

# uloha 4
    for i in range (0,10,1):
        for j in range (0,1,1):
            print (l2,end=" ")
    print(f"V listu2 jsou prvky:", (l2))
import random
import random as rnd
# task 1
def type_and_value(var):
    print(f"Type: {type(var)} and value:{var}")

if __name__=="__main__":
    d1={}
    d1['Audi']="Audi, 4V, red, 2 000 000"
    d1['Hyundai']="Hyundai, 4V, black, 1 500 000"
    type_and_value(d1)
    print (d1['Audi'])
    print (d1['Hyundai'])

# task 2
for x in range(2):
    print(random.choice(['BMW', 'Hyundai', 'Honda', 'Audi']), end=" ")
    print(random.choice(['2V', '4V', '8V']), end=" ")
    print(random.choice(['white', 'black', 'red', 'blue', 'yellow', 'green', 'silver']), end=" ")
    print(random.choice(['1 500 000', '1 600 000', '1 700 000', '2 000 000', '800 000']), end=" - ")

    d1={}
    d1['name']="BMW","Hyundai","Honda","Audi"
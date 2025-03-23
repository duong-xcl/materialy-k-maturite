#Python dictionaries (slovniky)

#funkce pro vypsani datoveho typu a promenne. Funkce prijima promennou
def type_and_value(var):
    print(f"Type: {type(var)} and value:{var}")

if __name__=="__main__":
    d1={}
    d1['region']="Gansu"
    d1['city']="Lanzhou"
    type_and_value(d1)
    print (d1['region'])
    print (d1['city'])
    d2={'region':"Gansu"}
    d2['city']="Haixing"
    l1=[d1,d2] # Vypiste vsechny mesta listu slovniku l1
    for i in l1:
        print(i['city'])
    for i in range(len(l1)):
        print(l1[i]['city'])
    d3={"address":l1}

    for i in d3['address']:
        print(i['city'])
    
    # ALTERNATIVNI ZPUSOB
    for key,value in d3.items():
        if key is 'address':
            for i in value:
                print(i['city'])

   # print(type(d1))
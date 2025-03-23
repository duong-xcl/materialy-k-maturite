jmena=["Tomas","Karel","Josef","Simon"]
vek=[25,45,23,50]
imunita=[1,0.95,0.85,0]

clovek=[jmena,vek,imunita]

def vypis_parametr(ind:int):
    for i in clovek:
        print(i[ind])


if __name__=="__main__":
    vypis_parametr(0)


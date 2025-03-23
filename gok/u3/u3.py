# slovniky ++
import json
import random as rnd

# r je pro cteni - read
def load_config_json(filepath):
    with open(filepath,'r',encoding="utf-8") as jsonfile:
        config=json.load(jsonfile)
    return config

# w je pro upravovani a psani - write
def write_config_json(filepath,data):
    with open(filepath,'w',encoding="utf-8") as f:
        data=json.dumps(data,indent=2)
        f.write(data)


def create_people(n:int,name:list,surname:list):
    pattern={"people":[]}
    for i in range (n):
        pattern ['people'].append({"surname":surname[rnd.randint(0,len(surname)-1)],
                                    "name":name[rnd.randint(0,len(name)-1)]})
    return pattern

if __name__=="__main__":
    path=r"H:\gok\u3\cnf.json"
    conf=load_config_json(path)
    print("")
    name=['Huang', 'Bin', 'Hao', 'Fang', 'Nan', 'Ba', 'Mei', 'Xin', 'Gui', 'Ying', 'Xiao']
    surname=['Xue', 'Wang', 'Ma', 'Yi', 'San', 'Siu', 'Zhou', 'Chang', 'Li', 'Lee', 'Chan']
    path=r"H:\gok\u3\cnf2.json"
    lidi=create_people(15,name,surname)
    write_config_json(path,lidi)
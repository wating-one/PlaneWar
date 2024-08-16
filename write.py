import json
from constant import *
level_list=[
    {"level":1,"num1":20,"num2":0,"num3":0,"rank1":0,"rank2":0,"rank3":0},
    {"level":2,"num1":25,"num2":10,"num3":0,"rank1":0,"rank2":0,"rank3":0},
    {"level":3,"num1":25,"num2":10,"num3":2,"rank1":0,"rank2":0,"rank3":0},
    {"level":4,"num1":20,"num2":10,"num3":3,"rank1":1,"rank2":0,"rank3":0},
    {"level":5,"num1":20,"num2":10,"num3":3,"rank1":1,"rank2":1,"rank3":0},
    {"level":6,"num1":20,"num2":10,"num3":3,"rank1":1,"rank2":1,"rank3":1},
    {"level":7,"num1":20,"num2":10,"num3":4,"rank1":2,"rank2":1,"rank3":1},
    {"level":8,"num1":20,"num2":10,"num3":4,"rank1":2,"rank2":2,"rank3":1},
    {"level":9,"num1":20,"num2":10,"num3":5,"rank1":2,"rank2":2,"rank3":2},
    {"level":10,"num1":30,"num2":10,"num3":5,"rank1":2,"rank2":2,"rank3":2}
]
num1,num2,num3=0,0,0
for level in level_list:
    num1+=level["num1"]
    num2+=level["num2"]
    num3+=level["num3"]
    level['score']=num1*100+num2*500+num3*2000
    print(num1*100+num2*500+num3*2000)
# with open("levels.json","w") as f:
#     level_list=json.dump(level_list,fp=f)
import json
list={"p1":{"副露区":[],"出过的牌":[]}}
obj=json.dumps(list)
print(obj)
with open("test.json","w")as f:
    for i in obj:
        f.write(i)
b=eval(obj)
print(b)
print(json.loads(obj)['p1']['副露区'])
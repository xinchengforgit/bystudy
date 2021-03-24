import json
with open('majhong.json','r') as f:
    str=f.read()
    print(type(str))
str=json.loads(str)
print(type(str))
for i in str:
     if i.get("text")!=None:
         print(i.get("text"))



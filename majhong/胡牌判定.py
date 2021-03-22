import time,sys
import random #用于测试。
#公共参数，1套牌库，注意总共是4套。
pais=list(range(1,10))+list(range(11,20))+list(range(21,30))+list(range(31,38,2))+list(range(41,46,2))

def is_hu(d:list):
    if(len(d)%3!=2):
        return False  #不是3n+2型，胡牌失败
    double=[] #检测对子
    for x in set(d):
        if(d.count(x)>=2):
            double.append(x)  #存入对子
    if(len(double)==0):
         return False  ##对子都没有显然不可能和牌
    a1=d.copy()
    a2=[] #a2用来存放和牌后分组的结果
    for x in double:
        a1.remove(x)
        a1.remove(x)
        a2.append((x,x))
        for i in range(int(len(a1)/3)):
            if(a1.count(a1[0])==3):
                a2.append((a1[0],)*3)
                a1=a1[3:]  #三张一样的情况
            elif a1[0] in a1 and a1[0]+1 in a1 and a1[0]+2 in a1:
                a2.append((a1[0],a1[0]+1,a1[0]+2))
                a1.remove(a1[0]+2)
                a1.remove(a1[0]+1)
                a1.remove(a1[0])
            else:
                a1=d.copy()
                a2=[]
                break #如果上述不满足，那么回溯到一开始判断
        else:
            return True
    else:
        return False #如果上述遍历没有返回和牌成功，则需要返回和牌失败
print(pais)
dict={}
for i in range(1,10):
    dict["A%d" %i]=i
for i in range(1,10):
    dict["B%d" %i]=i+10
for i in range(1,10):
    dict["C%d" %i]=i+20
dict["D1"]=31
dict["D2"]=33
dict["D3"]=35
dict["D4"]=37
dict["E1"]=41
dict["E2"]=43
dict["E3"]=45

temp_list=[]
p=["A2","B2","A5","A5"]
for j in p:
            temp_list.append(dict[j])

print(temp_list)


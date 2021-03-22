import json
import random
import functools
import 胡牌判定
#首先要有一个存放麻将牌的东西

all_cards=[]
#饼万索风花为ABCDE
def card_init():
        for i in range(1,10):
            for j in range(1,5):
                all_cards.append("A%d" %i)
        for i in range(1,10):
            for j in range(1, 5):
                all_cards.append("B%d" %i)
        for i in range(1, 10):
            for j in range(1, 5):
                all_cards.append("C%d" %i)
        for i in range(1,5):
              for j in range(1,5):
                all_cards.append("D%d" %i)
        for i in range(1,4):
              for j in range(1,5):
                  all_cards.append("E%d" %i)
        random.shuffle(all_cards)
#以上是对初始麻将牌的操作
card_init()







### 将牌映射成列表的一个字典,方便之后进行胡牌的判定
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
print(len(all_cards))
#需要有四个玩家
class Player():
     def __init__(self):
        self.cards=[]
        self.outcards=[]
        self.vice_cards=[]
p1=Player()
p2=Player()
p3=Player()
p4=Player()
playerlist=[p1,p2,p3,p4]
p_num=random.randint(0,3)
#初始化每个玩家的手牌
def  init():
        for i in range(4):
            for j in range(13):
                playerlist[(i+p_num)%4].cards.append(all_cards.pop())##实现初始的摸牌功能
        for i in range(4):
                print(playerlist[(i+p_num)%4].cards)
        for i in range(4):
                playerlist[i].cards.sort()
                print(playerlist[i].cards)

init()
#实现每个玩家的出牌阶段
def get_your_card(cur):
    playerlist[cur].cards.append(all_cards.pop())
    print("%d号玩家，现在是你的出牌阶段," %cur)
    print('你此时的牌是:\n')
    print(playerlist[cur].cards)
    print('场上玩家依次打出的牌是:\n')
    for i in range(4):
        if(playerlist[(cur+i)%4].outcards):
          print("%d号玩家：" %((cur+i)%4),end="")
          print(playerlist[(cur+i)%4].outcards)
    print('场上玩家的副露区牌依次是:\n')
    for i in range(4):
        if(playerlist[(cur+i)%4].vice_cards):
          print(playerlist[(cur+i)%4].vice_cards)
    out_card=input("请输入你想要打出的牌")
    id=playerlist[cur].cards.index(out_card)
    playerlist[cur].outcards.append(out_card)
    del playerlist[cur].cards[id]
    playerlist[cur].cards.sort()
    return out_card
#判定能不能胡牌
def is_hu(cur,out_card):
    d=[]
    for()
    if(len(d)%3!=2):
        return False  #不是3n+2型，胡牌失败
    double=[] #检测对子
    for x in set(d):
        if(d.count(x)>=2):
            double.append(x)  #存入对子
    if(len(double)==0):
         return False
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


def wait(cur,out_card):
    for i in range(1,4):
        temp_list = []
        for j in playerlist[(i+cur)%4].cards:
            temp_list.append(dict[j])
        if temp_list.count(dict[out_card])>=2:
            print("%d号玩家:你现在的牌是:" %((cur+i)%4),end="")
            print(playerlist[(cur+i)%4].cards)
            chio=input("您可以选择碰,要碰吗(y or n)\n")
            if chio=='y':
                playerlist[(i+cur)%4].vice_cards.append(out_card)
                playerlist[(i+cur) % 4].vice_cards.append(out_card)
                playerlist[(i+cur) % 4].vice_cards.append(out_card)
                playerlist[i].outcards.remove(out_card)
                return (i+cur)%4    #如果碰后，那么牌河的牌要被移除
            elif chio=='n':
                continue
            else:
                print("输入不合法,默认跳过(滑稽)\n")
                continue
    ####接下来判断吃
    now=(cur+1)%4
    tp_list=[]
    for j in playerlist[now].cards:
        tp_list.append(dict[j])
    if
    return -1


def play_games():
    cur=p_num
    while (len(all_cards)>0):
          out_card=get_your_card(cur)
          for i in range(3):
              if is_hu((i+cur)%4,out_card):
                  choose=input("你可以选择是否胡牌(y or n)\n")
                  if choose=='y':
                     print("游戏结束,%d号玩家胡牌" %((cur+i)%4))
                     return (cur+i)%4
                  else:
                     continue
          temp=wait(cur,out_card)
          if temp!=-1:
              cur=temp #现在轮到这个人打出牌
              print('你此时的牌是:\n')
              print(playerlist[cur].cards)
              print('场上玩家依次打出的牌是:\n')
              for i in range(4):
                  if (playerlist[(cur + i) % 4].outcards):
                      print(playerlist[(cur + i) % 4].outcards + '\n')
              print('场上玩家的副露区牌依次是:\n')
              for i in range(4):
                  if (playerlist[(cur + i) % 4].vice_cards):
                      print(playerlist[(cur + i) % 4].vice_cards)
              out_card = input("请输入你想要打出的牌")
              id = playerlist[cur].cards.index(out_card)
              playerlist[cur].outcards.append((playerlist[cur].outcards))
              del playerlist[cur].cards[id]
          cur=(cur+1)%4   ###一轮打牌结束

init()
play_games()

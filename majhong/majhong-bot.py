import json
import random
import functools
#首先要有一个存放麻将牌的东西
import p3 as p3

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
    sorted(playerlist[cur].cards)
    print('你此时的牌是:\n')
    print(playerlist[cur].cards)
    print('场上玩家依次打出的牌是:\n')
    for i in range(4):
        if(playerlist[(cur+i)%4].outcards):
          print(playerlist[(cur+i)%4].outcards+'\n')
    print('场上玩家的副露区牌依次是:\n')
    for i in range(4):
        if(playerlist[(cur+i)%4].vice_cards):
          print(playerlist[(cur+i)%4].vice_cards)
    out_card=input("请输入你想要打出的牌")
    id=playerlist[cur].cards.index(out_card)
    playerlist[cur].outcards.append((playerlist[cur].outcards))
    del playerlist[cur].cards[id]
    return
def wait(cur):

get_your_card(p_num)


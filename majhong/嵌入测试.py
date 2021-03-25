from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
import test

from graia.application.message.elements.internal import Plain, Source, At
from graia.application.friend import Friend
from graia.application.group import Group, Member




















import json
import random
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
cur=p_num ###定义一个全局变量cur,表示当前出牌玩家
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


#实现每个玩家的摸牌阶段
def take_your_card(cur):
    new_card=all_cards.pop()
    if is_hu(cur,new_card):
        playerlist[cur].cards.append(new_card)
        print("%d号玩家,你现在的牌是:" % (cur), end="")
        print(playerlist[cur].cards)
        choose = input("你可以选择是否胡牌(y or n)\n")
        if choose=='y':
            print("游戏结束,%d号玩家胡牌" %cur)
            return 1
        else:
            return 0
    else:
        playerlist[cur].cards.append(new_card)
#实现每个玩家的出牌阶段
def out_your_card(cur):
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
          print("%d号玩家：" % ((cur + i) % 4), end="")
          print(playerlist[(cur+i)%4].vice_cards)
    out_card=input("请输入你想要打出的牌")
    playerlist[cur].outcards.append(out_card)
    playerlist[cur].cards.remove(out_card)
    playerlist[cur].cards.sort()
    return out_card
#判定能不能胡牌
def is_hu(cur,out_card):  ###就是准备要胡牌的玩家
    d=[]
    for i in playerlist[cur].cards:
        d.append(dict[i])
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
### 判断能不能碰
def is_peng(cur,out_card):
    if playerlist[cur].cards.count(out_card)>=2:
        return True
    return False
def is_chi(cur,out_card):
    d = []
    for i in playerlist[cur].cards:
        d.append(dict[i])
    num=dict[out_card]
    if (num + 1 in d and num + 2 in d) or (num - 1 in d and num + 1 in d) or ( num-1 in d and num-2 in d):
        return True
    return False


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
                playerlist[(i+cur) %4].cards.remove(out_card)
                playerlist[(i+cur) %4].cards.remove(out_card)
                playerlist[cur].outcards.remove(out_card)
                playerlist[(i+cur)%4].vice_cards.sort()
                return (i+cur)%4    #如果碰后，那么牌河的牌要被移除
            elif chio=='n':
                continue
            else:
                print("输入不合法,默认跳过(滑稽)\n")
                continue
    now=(cur+1)%4
    tp_list=[]
    num=dict[out_card]
    for j in playerlist[now].cards:
        tp_list.append(dict[j])
    if (num+1 in tp_list and  num+2 in tp_list) or (num-1 in tp_list and num+1 in tp_list) or (num-1 in tp_list and num-2 in tp_list) :
        print("%d号玩家你现在的牌是:" %(now) ,end="")
        print(playerlist[now].cards)
        chio=input("你现在可以吃上家的牌，要吃吗\n")
        if chio=='y':
            while 1:
                print("请输入你要用来吃上家的牌")
                a=input()
                b=input()  ###此处要修改
                card_a=dict[a]
                card_b=dict[b]
                judge_list=[]
                judge_list.append(card_a)
                judge_list.append(card_b)
                judge_list.append(num)
                judge_list.sort()
                if judge_list[0]==judge_list[1]-1 and judge_list[1] ==judge_list[2]-1:
                    playerlist[cur].outcards.remove(out_card)
                    playerlist[now].vice_cards.append(a)
                    playerlist[now].vice_cards.append(b)
                    playerlist[now].vice_cards.append(out_card)
                    playerlist[now].cards.remove(a)
                    playerlist[now].cards.remove(b)
                    playerlist[now].vice_cards.sort() ##洗一下牌好点
                    return now
                else:
                    print("输入不合法,请重新输入")
        else:
            pass

    return -1








def play_games():
    cur=p_num
    while (len(all_cards)>0):
          if take_your_card(cur):
              return cur
          out_card=out_your_card(cur)
          for i in range(3):
              if is_hu((i+cur)%4,out_card):
                  print("%d号玩家,你现在的牌是:" %((cur+i)%4),end="")
                  print(playerlist[(i+cur)%4].cards)
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
                      print("%d号玩家：" % ((cur + i) % 4), end="")
                      print(playerlist[(cur + i) % 4].outcards)
              print('场上玩家的副露区牌依次是:\n')
              for i in range(4):
                  if (playerlist[(cur + i) % 4].vice_cards):
                      print("%d号玩家：" % ((cur + i) % 4), end="")
                      print(playerlist[(cur + i) % 4].vice_cards)
              out_card = input("请输入你想要打出的牌")
              playerlist[cur].outcards.append(out_card)
              playerlist[cur].cards.remove(out_card)
              del playerlist[cur].cards[id]
          cur=(cur+1)%4
          print("当前牌堆还剩下%d张牌"%len(all_cards))###一轮打牌结束
















hu_queue=[False,False,False,False]
chi_queue=[False,False,False,False]
peng_queue=[False,False,False,False]
groupqueue=[]
game_start = False
run_game = False
playerqueue = []
loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="INITKEY6uvftEim",  # 填入 authKey
        account=2419743144,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


##定义游戏是否开始的标志，只有游戏开始时，接收到的消息才会被执行在游戏相关的函数里面
# @bcc.receiver("FriendMessage")
# async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
#     await app.sendFriendMessage(friend, MessageChain.create([
#        Plain("你好,"+friend.nickname),
#     ]))
# @bcc.receiver("FriendMessage")
# async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend, message: MessageChain):
#     text = message.asDisplay()
#     if text == "你好":
#         await app.sendFriendMessage(friend, MessageChain.create([
#             Plain("好你个大头鬼,能不爪巴")
#         ]))
#     else:
#         await app.sendFriendMessage(friend, MessageChain.create([
#             Plain("你好")
#         ]
#         ))


# @bcc.receiver('GroupMessage')
# async def group_message_listener(app: GraiaMiraiApplication,group:Group,member:Member):
# await app.sendGroupMessage(group,MessageChain.create([
#     Plain("this is test bot"),At(2240131203)
# ]))

# @bcc.receiver("GroupMessage")
# async def groupMessage(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
# message_str=message.json()
# print(message)
# print(member.name)
#
#
# with open("majhong.json",'w') as f:
#     for i in message_str:
#         f.write(i)


@bcc.receiver("GroupMessage")
###将游戏玩家加入玩家列表,并且开始游戏
async def join_games(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    global game_start, run_game,cur
    global playerqueue
    print(len(playerqueue))
    if game_start == True and run_game==False:
        if len(playerqueue) < 4:
            message_str = message.asDisplay()
            print(message_str)
            # if message_str == "加入游戏@" + str(app.connect_info.account) + " ":
            if message_str=='1':
                if member.id in playerqueue:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("憨批，你已经加入游戏了"), At(member.id)
                    ]))
                else:
                    playerqueue.append(member.id)
                    if (len(playerqueue)) < 4:
                        message_1=MessageChain.create([Plain("等待玩家加入游戏，现在加入游戏的玩家有:")])
                        for i in range(len(playerqueue)):
                            message_1.plus(MessageChain.create([At(playerqueue[i])]))
                        await app.sendGroupMessage(group,message_1)
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("玩家准备就绪，请输入2开始游戏\n"),
                        ]))
                        groupqueue.append(group.id)
                        run_game=True
                        # await app.sendGroupMessage(group, MessageChain.create([
                        #     Plain("正在给各位玩家分配手牌")
                        # ]))
                        # card_init()
                        # init()
                        # for i in range(0,4):
                        #     await app.sendFriendMessage(playerqueue[(i+p_num)%4],MessageChain.create(
                        #         [
                        #             Plain("您当前的牌是:"),
                        #             Plain(str(playerlist[(i+p_num)%4].cards))
                        #         ]
                        #     ))
                        # run_game = True
                        # while(len(all_cards)>0):
                        #     print(cur)
                        #     new_card = all_cards.pop()
                        #     playerlist[cur].cards.append(new_card)
                        #     await app.sendFriendMessage(playerqueue[cur], MessageChain.create(
                        #         [
                        #             Plain("现在是你的出牌阶段"),
                        #             Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                        #             Plain(str(playerlist[cur].cards))
                        #         ]
                        #     ))
                        #     await out_card()
                        #     cur=(cur+1)%4



@bcc.receiver("GroupMessage")
async def help_game(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    global game_start
    if game_start == True:
        message_str = message.asDisplay()
        if message_str == "？@" + str(app.connect_info.account) + " ":
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),
                Plain("\n"),
                Plain("这是一个关于麻将机器人的测试项目\n"),
                Plain("很遗憾，由于制作者现在的技术，在开始游戏的时候，其他的群聊功能会暂时关闭，等他以后有时间再研究一下吧\n"),
                Plain("下面开始本游戏的说明\n")
            ]))
            await app.sendGroupMessage(group, MessageChain.create(
                [
                    Plain("麻将规则很简单,见bygroup实习手册上写的\n"),
                    Plain('现在有请各位玩家加入游戏，请输入 "加入游戏@bot" 来加入游戏,当加入游戏的玩家等于四人时，游戏将开始')
                ]

            ))


@bcc.receiver("GroupMessage")
async def start_game(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    global game_start
    if game_start == False:
        message_str = message.asDisplay()
        if (message_str == "开始游戏@" + str(app.connect_info.account) + " "):
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("游戏已开始，请输入?@bot来查看游戏帮助"),
                At(member.id)
            ]))
            game_start = True

####定义玩家的摸牌


####接收玩家的请求
@bcc.receiver("FriendMessage")
async def out_card(app:GraiaMiraiApplication,friend:Friend,message:MessageChain):
    global cur
    if run_game==True and friend.id==playerqueue[cur]:
            message_str=message.asDisplay()
            print(message_str)
            print(type(message_str))
            if hu_queue[cur]==True:
                    if message_str=='y' or message_str=='Y':
                        await app.sendGroupMessage(groupqueue[0],MessageChain.create(
                            [
                                At(playerqueue[cur]),
                                Plain("胡牌了，游戏结束")
                            ]
                        ))   ####自摸的情况
                        run_game==False
                        start_game==False ###游戏结束后，将状态改回来即可
            else:
                    playerlist[cur].cards.remove(message_str)
                    playerlist[cur].cards.sort()
                    playerlist[cur].outcards.append(message_str)
                    print(groupqueue[0])
                    await app.sendGroupMessage(groupqueue[0], MessageChain.create([
                        At(playerqueue[cur]),
                        Plain("打出了: " + message_str)
                    ]))
                    # await app.sendFriendMessage(playerqueue[cur], MessageChain.create([
                    #     Plain("现在是你的出牌阶段"),
                    #     Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                    #     Plain(str(playerlist[cur].cards))]
                    # # )) 要修改的东西
                    messagechain1=MessageChain.create([Plain("当前玩家打出的牌是:\n")
                                              ])
                    for i in range (0,4):
                        if playerlist[i].outcards:
                            tempchain=MessageChain.create([
                            At(playerqueue[i]),
                            Plain(":"+str(playerlist[i].outcards)+"\n")])
                            messagechain1.plus(tempchain)
                    await app.sendGroupMessage(groupqueue[0],messagechain1)
                    messagechain1 = MessageChain.create([Plain("当前玩家副露区的牌是:\n")
                                                 ])
                    ###### 先判断玩家能否胡牌
                    for i in range(0, 4):
                        if playerlist[i].vice_cards:
                            tempchain = MessageChain.create([
                                At(playerqueue[i]),
                                Plain(":" + str(playerlist[i].vice_cards) + "\n")])
                            messagechain1.plus(tempchain)
                    await  app.sendGroupMessage(groupqueue[0], messagechain1)
                    for i in range(0,3):
                        if is_hu((cur+i)%4,message_str):
                            hu_queue[(cur+i)%4]=True
                    if hu_queue.count(True):
                            messagechain_hu = MessageChain.create(
                                [
                                    Plain("以下玩家胡牌:\n")
                                ]
                                )
                            for i in range(0, 3):
                                if hu_queue[(i + cur) % 4] == True:
                                    messagechain_hu.plus(MessageChain.create([
                                        At(playerqueue[(i + cur) % 4])
                                    ]))
                            await app.sendGroupMessage(groupqueue[0], messagechain_hu)
                            run_game == False
                            start_game == False
                    #####再判断玩家能否碰牌
                    for i in range(0,3):
                        if is_peng((i+cur)%4,message_str):
                            peng_queue[(i+cur)%4]=True
                            await app.sendFriendMessage(playerqueue[(i+cur)%4],MessageChain.create(
                                [
                                    Plain("你现在可以碰，要碰吗(y or n)，你有5s")
                                ]
                            ))
                            await asyncio.sleep(5)
                            peng_queue[(i+cur)%4]=False
                            await app.sendFriendMessage(playerqueue[(i+cur)%4],MessageChain.create(
                                [
                                    Plain("时间到")
                                ]
                            ))
                    if True in peng_queue:
                        await asyncio.sleep(5)  ####等待5s，看看有没有人碰
                        if peng_queue[cur]==True:
                            await app.sendFriendMessage(playerqueue[cur], MessageChain.create(
                                [
                                    Plain("现在是你的出牌阶段,你的牌是:"),
                                    Plain(str(playerlist[cur].cards))
                                ]
                            ))
                            peng_queue[cur]=False
                        else:
                            temp=cur
                            cur=(cur+1)%4 #没人碰就顺着下去
                            playerlist[cur].cards.append(all_cards.pop())
                            await  app.sendFriendMessage(playerqueue[cur],MessageChain.create([
                                Plain("现在是你的出牌阶段"),
                                Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                                Plain(str(playerlist[cur].cards))]
                            ))
                            peng_queue[temp]=False
                    if is_chi((cur+1)%4,message_str):
                            chi_queue[(1+cur) % 4] = True
                            await app.sendFriendMessage(playerqueue[(1+cur) % 4], MessageChain.create(
                                [
                                    Plain("你现在可以吃，要吃吗(y or n)，你有5s")
                                ]
                            ))
                            await asyncio.sleep(5)
                            chi_queue[(1+cur)%4]=False
                            await app.sendFriendMessage(playerqueue[(i + cur) % 4], MessageChain.create(
                                [
                                    Plain("时间到")
                                ]
                            ))
                    if True in chi_queue:
                        await asyncio.sleep(5)  ####等待5s，看看有没有人吃
                        if chi_queue[cur] == True:
                            await app.sendFriendMessage(playerqueue[cur], MessageChain.create(
                                [
                                    Plain("现在是你的出牌阶段,你的牌是:"),
                                    Plain(str(playerlist[cur].cards))
                                ]
                            ))
                            chi_queue[cur] =False
                        else:
                            temp=cur
                            cur = (cur + 1) % 4  # 没人吃就顺着下去
                            playerlist[cur].cards.append(all_cards.pop())
                            await  app.sendFriendMessage(playerqueue[cur], MessageChain.create([
                                Plain("现在是你的出牌阶段"),
                                Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                                Plain(str(playerlist[cur].cards))]
                            ))
                            chi_queue[temp]=False
                    else:
                        cur = (cur + 1) % 4  # 没人碰就顺着下去
                        playerlist[cur].cards.append(all_cards.pop())
                        await  app.sendFriendMessage(playerqueue[cur], MessageChain.create([
                            Plain("现在是你的出牌阶段"),
                            Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                            Plain(str(playerlist[cur].cards))
                        ]))






#### 开始游戏的阶段
@bcc.receiver("GroupMessage")
async def initgame(app:GraiaMiraiApplication,group:Group,message:MessageChain):
    global run_game,hu_queue
    message_str=message.asDisplay()
    if run_game==True and  message_str=='2' :
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("正在给各位玩家分配手牌")
        ]))
        card_init()
        init()
        for i in range(0, 4):
            await app.sendFriendMessage(playerqueue[(i + p_num) % 4], MessageChain.create(
                [
                    Plain("您当前的牌是:"),
                    Plain(str(playerlist[(i + p_num) % 4].cards))
                ]
            ))
        print(cur)
        out_card=all_cards.pop()
        playerlist[cur].cards.append(out_card)
        if is_hu(cur,out_card):
            hu_queue[cur]=True
            await app.sendFriendMessage(playerqueue[cur],MessageChain.create(
                [
                    Plain("现在是你的出牌阶段"),
                    Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                    Plain(str(playerlist[cur].cards))
                ]
            ))
            await app.sendFriendMessage(playerqueue[cur],MessageChain.create(
                [
                    Plain("你可以选择胡牌,要胡吗(y or n)"),
                ]
            ))
        else:
            await app.sendFriendMessage(playerqueue[cur],MessageChain.create(
                [
                    Plain("现在是你的出牌阶段"),
                    Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                    Plain(str(playerlist[cur].cards))
                 ]
                ))


@bcc.receiver("FriendMessage")
def choose_peng(app:GraiaMiraiApplication,frined:Friend,message:MessageChain):
    global cur
    if run_game==True:
        chose=playerqueue.index(frined.id)
        if peng_queue[chose]==True:
            message_str=message.asDisplay()
            if message_str=='n' or 'N':
                peng_queue[chose]=False
            else:
                out_card=playerlist[cur].outcards.pop()
                playerlist[chose].cards.remove(out_card)
                playerlist[chose].cards.remove(out_card)
                playerlist[chose].vice_cards.append(out_card)
                playerlist[chose].vice_cards.append(out_card)
                playerlist[chose].vice_cards.append(out_card)
                playerlist[chose].vice_cards.sort()
                cur=chose

@bcc.receiver("FriendMessage")
def choose_chi(app:GraiaMiraiApplication,frined:Friend,message:MessageChain):
    global cur
    if run_game == True:
        chose = playerqueue.index(frined.id)
        if chi_queue[chose] == True:
            message_str = message.asDisplay()
            temp=message_str[0:1]
            if temp=='n':
                chi_queue[chose]=False
            else:
                card1=message_str[2:4]
                card2=message_str[5:6]
                out_card = playerlist[cur].outcards.pop()
                playerlist[chose].cards.remove(card1)
                playerlist[chose].cards.remove(card2)
                playerlist[chose].vice_cards.append(card1)
                playerlist[chose].vice_cards.append(card2)
                playerlist[chose].vice_cards.append(out_card)
                playerlist[chose].vice_cards.sort()


app.launch_blocking()
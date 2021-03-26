from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
import pymysql

from graia.application.message.elements.internal import Plain, At
from graia.application.friend import Friend
from graia.application.group import Group, Member

import json
import random

# 首先要有一个存放麻将牌的东西
conn = pymysql.connect(host='localhost', user='root', password='', database='bystudy')
cursor = conn.cursor()

all_cards = []


# 饼万索风花为ABCDE
def card_init():
    for i in range(1, 10):
        for j in range(1, 5):
            all_cards.append("A%d" % i)
    for i in range(1, 10):
        for j in range(1, 5):
            all_cards.append("B%d" % i)
    for i in range(1, 10):
        for j in range(1, 5):
            all_cards.append("C%d" % i)
    for i in range(1, 5):
        for j in range(1, 5):
            all_cards.append("D%d" % i)
    for i in range(1, 4):
        for j in range(1, 5):
            all_cards.append("E%d" % i)
    random.shuffle(all_cards)


# 以上是对初始麻将牌的操作


### 将牌映射成列表的一个字典,方便之后进行胡牌的判定
dict = {}
for i in range(1, 10):
    dict["A%d" % i] = i
for i in range(1, 10):
    dict["B%d" % i] = i + 10
for i in range(1, 10):
    dict["C%d" % i] = i + 20
dict["D1"] = 31
dict["D2"] = 33
dict["D3"] = 35
dict["D4"] = 37
dict["E1"] = 41
dict["E2"] = 43
dict["E3"] = 45


# 需要有四个玩家
class Player():
    def __init__(self):
        self.cards = []
        self.outcards = []
        self.vice_cards = []


p1 = Player()
p2 = Player()
p3 = Player()
p4 = Player()
playerlist = [p1, p2, p3, p4]
p_num = random.randint(0, 3)  ###出牌玩家是随机的
cur = p_num  ###定义一个全局变量cur,表示当前出牌玩家


# 初始化每个玩家的手牌
def init():
    for i in range(4):
        for j in range(13):
            playerlist[(i + p_num) % 4].cards.append(all_cards.pop())  ##实现初始的摸牌功能
    for i in range(4):
        print(playerlist[(i + p_num) % 4].cards)
    for i in range(4):
        playerlist[i].cards.sort()
        print(playerlist[i].cards)


# 判定能不能胡牌
def is_hu(cur, out_card):  ###就是准备要胡牌的玩家
    d = []
    for i in playerlist[cur].cards:
        d.append(dict[i])
    if (len(d) % 3 != 2):
        return False  # 不是3n+2型，胡牌失败
    double = []  # 检测对子
    for x in set(d):
        if (d.count(x) >= 2):
            double.append(x)  # 存入对子
    if (len(double) == 0):
        return False
    a1 = d.copy()
    a2 = []  # a2用来存放和牌后分组的结果
    for x in double:
        a1.remove(x)
        a1.remove(x)
        a2.append((x, x))
        for i in range(int(len(a1) / 3)):
            if (a1.count(a1[0]) == 3):
                a2.append((a1[0],) * 3)
                a1 = a1[3:]  # 三张一样的情况
            elif a1[0] in a1 and a1[0] + 1 in a1 and a1[0] + 2 in a1:
                a2.append((a1[0], a1[0] + 1, a1[0] + 2))
                a1.remove(a1[0] + 2)
                a1.remove(a1[0] + 1)
                a1.remove(a1[0])
            else:
                a1 = d.copy()
                a2 = []
                break  # 如果上述不满足，那么回溯到一开始判断
        else:
            return True
    else:
        return False  # 如果上述遍历没有返回和牌成功，则需要返回和牌失败


### 判断能不能碰
def is_peng(cur, out_card):
    if playerlist[cur].cards.count(out_card) >= 2:
        return True
    return False


def is_chi(cur, out_card):
    d = []
    for i in playerlist[cur].cards:
        d.append(dict[i])
    num = dict[out_card]
    if (num + 1 in d and num + 2 in d) or (num - 1 in d and num + 1 in d) or (num - 1 in d and num - 2 in d):
        return True
    return False


peng_times = [0, 0, 0, 0]
chi_times = [0, 0, 0, 0]
hu_queue = [False, False, False, False]  ###判断接收胡牌玩家的指令
chi_queue = [False, False, False, False]  ###判断接收吃的玩家的指令
peng_queue = [False, False, False, False]  ###判断接收碰的玩家的指令
groupqueue = []  ####玩家qq号
game_start = False
run_game = False
playerqueue = []  ####玩家队列
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


@bcc.receiver("GroupMessage")
###将游戏玩家加入玩家列表,并且开始游戏
async def join_games(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    global game_start, run_game, cur
    global playerqueue
    print(len(playerqueue))
    if game_start == True and run_game == False:
        if len(playerqueue) < 4:
            message_str = message.asDisplay()
            print(message_str)
            # if message_str == "加入游戏@" + str(app.connect_info.account) + " ":
            if message_str == '1':
                if member.id in playerqueue:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("抱歉，你已经加入游戏了"), At(member.id)
                    ]))
                else:
                    playerqueue.append(member.id)
                    if (len(playerqueue)) < 4:
                        message_1 = MessageChain.create([Plain("等待玩家加入游戏，现在加入游戏的玩家有:")])
                        for i in range(len(playerqueue)):
                            message_1.plus(MessageChain.create([At(playerqueue[i])]))
                        await app.sendGroupMessage(group, message_1)
                    else:
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain("玩家准备就绪，请输入2开始游戏\n"),
                        ]))
                        groupqueue.append(group.id)
                        run_game = True



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
                    Plain("首先需要规范用户的输入，限于本人的技术力问题，请你打牌时务必遵守上述规则\n"),
                    Plain("当场上有人打出牌而你可以碰或吃的时候，你只有5s的时间选择，否则bot将会默认你不选择吃\n"),
                    Plain("此外关于吃和碰的输出规范\n   "),
                    Plain("如果你选择吃，请你务必以'y card1 card2'的规则向bot发话,否则可能会产生bugQAQ   "),
                    Plain("如果你选择碰，你只需要打出' y '即可 "),
                ]
            ))
            await app.sendGroupMessage(group,MessageChain.create(
                [
                    Plain("关于数据查询的部分，如果你要查询玩家信息，请输入查询玩家@该玩家   \n"),
                    Plain("如果你想查询上盘参与对局的玩家的话,请输入查询上局信息@bot   \n"),
                    Plain("如果你想查询场上某张牌还剩余几张的话,请私聊bot并输入 '查牌 牌名' ,注意牌名是区分大小写的  ")
                ]
            ))


@bcc.receiver("GroupMessage")
async def start_game(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    global game_start
    if game_start == False:
        message_str = message.asDisplay()
        if (message_str == "开始游戏@" + str(app.connect_info.account) + " "):
            await app.sendGroupMessage(group, MessageChain.create([
                Plain("游戏已开始，请输入?@bot来查看游戏帮助,请输入1来加入游戏对局匹配队列中 "),
                At(member.id)
            ]))
            game_start = True


####定义玩家的摸牌


####接收玩家的请求
@bcc.receiver("FriendMessage")
async def out_card(app: GraiaMiraiApplication, friend: Friend, message: MessageChain):
    global cur
    if run_game == True and friend.id == playerqueue[cur]:
        message_str = message.asDisplay()
        print(message_str)
        print(type(message_str))
        if hu_queue[cur] == True:
            if message_str == 'y' or message_str == 'Y':
                await app.sendGroupMessage(groupqueue[0], MessageChain.create(
                    [
                        At(playerqueue[cur]),
                        Plain("胡牌了，游戏结束")
                    ]
                ))  ####自摸的情况
                sql = '''
                select max(id) from pfd
                '''
                cursor.execute(sql)
                result = cursor.fetchone()
                max_num = result[0]
                if result[0] == None:
                    max_num = 0

                sql = '''
                          insert into pfd(id,
                          p1,p2,p3,p4,winner)values(%d,%s,%s,%s,%s,%s)
                           ''' % ((max_num + 1),str(playerqueue[0]), str(playerqueue[1]), str(playerqueue[2]), str(playerqueue[3]), str(friend.id))
                try:
                    cursor.execute(sql)
                    conn.comit()
                except:
                    conn.rollback()

                run_game == False
                start_game == False  ###游戏结束后，将状态改回来即可
        else:
            temp=playerlist[cur].cards[-1]
            if temp!=message_str:
                playerlist[cur].cards.remove(message_str)
                playerlist[cur].cards.sort()
                playerlist[cur].outcards.append(message_str)
                print(groupqueue[0])
                await app.sendGroupMessage(groupqueue[0], MessageChain.create([
                    At(playerqueue[cur]),
                    Plain("打出了: " + message_str)
                ]))
            else:
                playerlist[cur].cards.remove(message_str)
                playerlist[cur].cards.sort()
                playerlist[cur].outcards.append(message_str)
                await app.sendGroupMessage(groupqueue[0], MessageChain.create([
                    At(playerqueue[cur]),
                    Plain("打出了摸到的: " + message_str)
                ]))
            # await app.sendFriendMessage(playerqueue[cur], MessageChain.create([
            #     Plain("现在是你的出牌阶段"),
            #     Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
            #     Plain(str(playerlist[cur].cards))]
            # # )) 要修改的东西
            messagechain1 = MessageChain.create([Plain("当前玩家打出的牌是:\n")
                                                 ])
            for i in range(0, 4):
                if playerlist[i].outcards:
                    tempchain = MessageChain.create([
                        At(playerqueue[i]),
                        Plain(":" + str(playerlist[i].outcards) + "\n")])
                    messagechain1.plus(tempchain)
            await app.sendGroupMessage(groupqueue[0], messagechain1)
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
            for i in range(0, 3):
                if is_hu((cur + i) % 4, message_str):
                    hu_queue[(cur + i) % 4] = True
                    temp = groupqueue[(cur + i) % 4]
            if hu_queue.count(True):
                messagechain_hu = MessageChain.create(
                    [
                        Plain("以下玩家胡牌:\n")
                    ]
                )
                for i in range(1, 4):
                    if hu_queue[(i + cur) % 4] == True:
                        messagechain_hu.plus(MessageChain.create([
                            At(playerqueue[(i + cur) % 4])
                        ]))
                await app.sendGroupMessage(groupqueue[0], messagechain_hu)
                sql = '''
                select max(id) from pfd
                '''
                cursor.execute(sql)
                result = cursor.fetchone()
                max_num = result[0]
                if result[0] == None:
                    max_num = 0

                sql = '''
                                insert into pfd(id,p1,p2,p3,p4,winner)
                                values(%d,%s,%s,%s,%s,%s) 
                            ''' % ((max_num+1),
                str(groupqueue[0]), str(groupqueue[1]), str(groupqueue[2]), str(groupqueue[3]), str(temp))
                try:
                    cursor.execute(sql)
                    conn.comit()
                except:
                    conn.rollback()
                for i in range(0, 4):
                    sql = '''
                                    insert into playdata(name,peng,chi)
                                    values(%s,%d,%d)
                                ''' % (str(groupqueue[i]), peng_times[i], chi_times[i])
                    try:
                        cursor.execute(sql)
                        conn.comit()
                    except:
                        conn.rollback()
                ####将数据导入数据库中

                run_game == False
                start_game == False
            #####再判断玩家能否碰牌
            for i in range(1, 4):
                if is_peng((i + cur) % 4, message_str):
                    peng_queue[(i + cur) % 4] = True
                    peng_temp = (i + cur) % 4
                    await app.sendFriendMessage(playerqueue[(i + cur) % 4], MessageChain.create(
                        [
                            Plain("你现在可以碰，要碰吗(y or n)，你有15s")
                        ]
                    ))
                    print((i + cur) % 4)
                    await asyncio.sleep(15)
                    await app.sendFriendMessage((playerqueue[(i + cur) % 4], MessageChain.create(
                        [
                            Plain("碰的时间到，你现在不能打出碰的命令了:")
                        ]
                    )))
                    # peng_queue[(i+cur)%4]=False
                    # await app.sendFriendMessage(playerqueue[(i+cur)%4],MessageChain.create(
                    #     [
                    #         Plain("时间到")
                    #     ]
                    # ))
            if True in peng_queue:
                # await asyncio.sleep(10)  ####等待5s，看看有没有人
                await app.sendFriendMessage(playerqueue[peng_temp], MessageChain.create(
                    [
                        Plain("现在是你的出牌阶段"),
                        Plain(str(playerlist[peng_temp].cards))
                    ]
                ))
                cur = peng_temp
                peng_times[cur] = peng_times[cur] + 1
                peng_queue[cur] = False
                ###记录碰的列表
            else:

                if is_chi((cur + 1) % 4, message_str):
                    chi_queue[(1 + cur) % 4] = True
                    await app.sendFriendMessage(playerqueue[(1 + cur) % 4], MessageChain.create(
                        [
                            Plain("你现在可以吃，要吃吗(y or n)，你有15s")
                        ]
                    ))
                    await asyncio.sleep(15)
                    await app.sendFriendMessage((playerqueue[(i + cur) % 4], MessageChain.create(
                        [
                            Plain("吃的时间到，你现在不能打出吃的命令了:")
                        ]
                    )))
                # chi_queue[(1+cur)%4]=False,这个地方需要修改
                # await app.sendFriendMessage(playerqueue[(1 + cur) % 4], MessageChain.create(
                #     [
                #         Plain("时间到")
                #     ]
                # ))
                if True in chi_queue:  ####等待5s，看看有没有人吃
                    await app.sendFriendMessage(playerqueue[(1 + cur) % 4], MessageChain.create(
                        [
                            Plain("现在是你的出牌阶段"),
                            Plain(str(playerlist[(1 + cur) % 4].cards))
                        ]
                    ))
                    chi_queue[(1 + cur) % 4] = False
                    cur = (cur + 1) % 4
                    chi_times[cur] = chi_times[cur] + 1  ##记录吃的次数的列表
                else:
                    cur = (cur + 1) % 4  # 没人吃就顺着下去
                    playerlist[cur].cards.append(all_cards.pop())
                    await  app.sendFriendMessage(playerqueue[cur], MessageChain.create([
                        Plain("现在是你的出牌阶段"),
                        Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                        Plain(str(playerlist[cur].cards))
                    ]))


#### 开始游戏的阶段
@bcc.receiver("GroupMessage")
async def initgame(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    global run_game, hu_queue
    message_str = message.asDisplay()
    if run_game == True and message_str == '2':
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
        out_card = all_cards.pop()
        playerlist[cur].cards.append(out_card)
        if is_hu(cur, out_card):
            hu_queue[cur] = True
            await app.sendFriendMessage(playerqueue[cur], MessageChain.create(
                [
                    Plain("现在是你的出牌阶段"),
                    Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                    Plain(str(playerlist[cur].cards))
                ]
            ))
            await app.sendFriendMessage(playerqueue[cur], MessageChain.create(
                [
                    Plain("你可以选择胡牌,要胡吗(y or n)"),
                ]
            ))
        else:
            await app.sendFriendMessage(playerqueue[cur], MessageChain.create(
                [
                    Plain("现在是你的出牌阶段"),
                    Plain("您现在的手牌是(最右边的那张是新摸的牌)："),
                    Plain(str(playerlist[cur].cards))
                ]
            ))


@bcc.receiver("FriendMessage")
async def choose_peng(app: GraiaMiraiApplication, frined: Friend, message: MessageChain):
    global cur
    if run_game == True:
        chose = playerqueue.index(frined.id)
        print(chose)
        if peng_queue[chose] == True:
            print(chose)
            message_str = message.asDisplay()
            print(message_str)
            if message_str == 'n' or message_str == 'N':
                peng_queue[chose] = False
            else:
                out_card = playerlist[cur].outcards.pop()
                playerlist[chose].cards.remove(out_card)
                playerlist[chose].cards.remove(out_card)
                playerlist[chose].vice_cards.append(out_card)
                playerlist[chose].vice_cards.append(out_card)
                playerlist[chose].vice_cards.append(out_card)
                playerlist[chose].vice_cards.sort()
                print(peng_queue[chose])


@bcc.receiver("FriendMessage")
async def choose_chi(app: GraiaMiraiApplication, frined: Friend, message: MessageChain):
    global cur
    if run_game == True:
        chose = playerqueue.index(frined.id)
        if chi_queue[chose] == True:
            message_str = message.asDisplay()
            temp = message_str[0:1]
            if temp == 'n' or temp == 'N':
                chi_queue[chose] = False
            else:
                card1 = message_str[2:4]
                card2 = message_str[5:7]
                print("吃")
                print(card1)
                print(card2)
                print(chose)
                out_card = playerlist[cur].outcards.pop()
                playerlist[chose].cards.remove(card1)
                playerlist[chose].cards.remove(card2)
                playerlist[chose].vice_cards.append(card1)
                playerlist[chose].vice_cards.append(card2)
                playerlist[chose].vice_cards.append(out_card)
                playerlist[chose].vice_cards.sort()


@bcc.receiver("GroupMessage")
async def serch_data(app: GraiaMiraiApplication, member: Member, group: Group, message: MessageChain):
    message_str = message.asDisplay()
    if message_str[0:5] == '查询玩家@':
        print(message_str)
        message_str = message_str[5:-1]
        print(message_str)
        print(type(message_str))
        sql = '''
                select count(*) from pfd where p1=%s or p2=%s or p3=%s or p4=%s 
            ''' % (message_str, message_str, message_str, message_str)
        cursor.execute(sql)
        result = cursor.fetchone()
        tot = result[0]
        if tot != 0:
            sql = '''
                    select count(*) from pfd where winner=%s
                ''' % (message_str)
            cursor.execute(sql)
            result = cursor.fetchone()
            winn = result[0]
            win_rate = winn / tot  ###胜率
            sql = '''
                    select avg(peng),avg(chi) from playerdata
                    where name=%s  
                ''' % (message_str)
            cursor.execute(sql)
            result = cursor.fetchall()
            peng = result[0][0]
            chi = result[0][1]
            await app.sendGroupMessage(
                group, MessageChain.create([
                    At(member.id),
                    Plain(" 该玩家的胜率是%f,场均碰的次数是%f,场均吃的次数是%f" % (win_rate, peng, chi))
                ])
            )
        else:
            await app.sendGroupMessage(
                group, MessageChain.create([
                    At(member.id),
                    Plain("好像查询不到该玩家的数据欸，快邀请ta一起来打麻将吧")
                ])
            )


@bcc.receiver('FriendMessage')
async def search_card(friend:Friend,app:GraiaMiraiApplication,message:MessageChain):
    global start_game,run_game
    if run_game==True:
        message_str=message.asDisplay()
        print(message_str)
        if message_str[0:3]=="查牌 ":
            message_str=message_str[3:]
            print(message_str)
            num=playerqueue.index(friend.id)
            tot=0
            for i in range(0,3):
                tot=tot+playerlist[(num+i)%4].cards.count(message_str)
            tot=tot+all_cards.count(message_str)
            await app.sendFriendMessage(friend,MessageChain.create(
                [
                    Plain("%s 牌还剩下 %d 张" %(message_str,tot))
                ]
            ))

@bcc.receiver('GroupMessage')
async def search_last(app:GraiaMiraiApplication,message:MessageChain,group:Group,member:Member):
        message_str=message.asDisplay()
        if message_str=="查询上局信息@"+str(app.connect_info.account)+" ":
            sql='''
            select * from pfd where id=(select max(id) from pfd)
            '''
            cursor.execute(sql)
            result=cursor.fetchall()
            if len(result)!=0:
                for data in result:
                    pl1=data[1]
                    pl2=data[2]
                    pl3=data[3]
                    pl4=data[4]
                await app.sendGroupMessage(group,MessageChain.create(
                    [
                        At(member.id),
                        Plain(" 上局对局中参与的玩家有: "),
                        At(int(pl1)),
                        At(int(pl2)),
                        At(int(pl3)),
                        At(int(pl4)),
                        Plain(" 胜者是: "),
                        At(int(pl4))
                    ]
                    ))
            else:
                await app.sendGroupMessage(group,MessageChain.create(
                    [
                        At(member.id),
                        Plain("暂时没有对局信息哦，欢迎开始打麻将")
                    ]
                ))


app.launch_blocking()
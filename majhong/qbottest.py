from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
import test

from graia.application.message.elements.internal import Plain,Source,At
from graia.application.friend import Friend
from graia.application.group import Group, Member

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="INITKEY6uvftEim", # 填入 authKey
        account=2419743144, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
# app.getGroup(892525106)
# @bcc.receiver("FriendMessage")
# async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
#     await app.sendFriendMessage(friend, MessageChain.create([
#        Plain("你好,"+friend.nickname),
#     ]))
@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend, message: MessageChain):
       text=message.asDisplay()
       if text=="你好":
           await app.sendFriendMessage(friend,MessageChain.create([
               Plain("好你个大头鬼,能不爪巴")
           ]))
       else:
           await app.sendFriendMessage(friend,MessageChain.create([
               Plain("你好")
               ]
           ))



                







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
async def game_is_continue():
        pass
async def game_start(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    message_str = message.asDisplay()
    print(message_str)
    if message_str == "?@" + str(app.connect_info.account) + " ":
            await app.sendGroupMessage(group, MessageChain.create([
            Plain("还在测试中\n 2")
        ]))


@bcc.receiver("GroupMessage")
def help_game(app:GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    if




@bcc.receiver("GroupMessage")
async def start_game(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
        message_str=message.asDisplay()
        print(group.id)
        print(message_str)
        temp_str="开始游戏@"+str(app.connect_info.account)+" " #草有个空格的
        if message_str==temp_str:
            await app.sendGroupMessage(group,MessageChain.create([
                Plain("游戏开始，请输入？@bot来查看游戏帮助.  "),
                At(member.id)
           ]))






app.launch_blocking()
#### 接入bot

#### 1.学习过程

1.首先我根据往上的教程安装了mirai-api-http,然后安装了一下,graia.

然后它的官方文档给了一个这个

~~~python
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio

from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="graia-mirai-api-http-authkey", # 填入 authKey
        account=5234120587, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain("Hello, World!")
    ]))

app.launch_blocking()
~~~

告知我这个程序能够对每一个发送消息的人发送一个hello，world.

然后我很懵逼，先从函数看起,@bcc.recevier()不知道是什么东西,所以我百度了一下

函数修饰器，能够改变一些函数的作用(详情见我写的另一篇markdown),

async，也很懵逼，经过我的百度，这个表示这个函数是协程函数,

await是搭配这个函数使用的，对这些东西有了大致的了解后，我开始看文档，

然而这个玩意的文档，讲的就是如何实现这些函数，也完全没有给例子，所以我开始根据万用print()来猜测各个属性对象和函数的作用2333，通过我的不懈努力，我终于了解到了@bcc.receiver("")的作用，然后仿造案例，写出了一个任何一个群发消息回复hello，world的作用，

但是问题在于我现在不能够获得别人发给我消息的内容，经过我翻了一个上午文档和各种print()，终于找到了message这个对象是可以被receiver接收到的，并且里面包含了各种消息对象，了解到了如何接收消息和发送消息后，我终于可以考虑如何接入bot了.

#### 2.学习难处

首先就是关于进入开始游戏这个模块,因为我发现receiver接收到的东西好像是不能够自定义的，所以无论你发什么消息都会被所有函数都接收到，但是要实现bot功能的话就不能被这个东西干扰，此外我又发现了receiver里面的事件貌似是不能够自定义的,所以我考虑加入了run_game，start_game这几个全局变量，来指定哪些函数只有在游戏开始时，接收的信息才会被函数执行,之后我开始了对麻将的嵌入




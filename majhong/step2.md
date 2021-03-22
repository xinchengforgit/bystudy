#### 阶段2.5的实现

为什么要直接跳到阶段2.5呢，因为我现在还不会实现胡和吃的判断QAQ.

#### hello bot

因为我用的是python好像有很多不太一样的东西

##### 1.使用mirai-console-loader启动mirai-console

然而下好后cmd运行，显示'java' 不是内部或外部命令，也不是可运行的程序
或批处理文件。

所以先要取配置java的环境变量，emm没什么好说的

##### 2.使用 mirai-login-solver-selenium 处理滑块验证辅助登录

在成功启动的mcl窗口，运行命令登录qq：`login 账号 密码`

于是我们需要mirai的另一个项目 mirai-login-solver-selenium 来辅助登录
mirai-login-solver-selenium安装步骤 (需要先安装 Chrome 浏览器)
先结束掉之前运行的 mirai-console, 然后在命令行运行如下命令，添加该包。

安装完成后，就能实现基本的登陆了

#### 3.python pip安装graia-application-mirai

 实现后，将setting.xml内的东西改为自己所需要的，然后复制官方文档下的代码

~~~
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
        account=, # 你的机器人的 qq 号
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

就能够实现qbot发送hello,xxx的功能了


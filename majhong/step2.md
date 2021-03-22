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




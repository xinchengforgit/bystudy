#### 1.asynio事件循环

会去检测并执行某些代码  ,如果可执行则放入可执行列表里，执行完则移出列表，否则则一直循环

~~~python
import asyncio
loop=asyncio.get_event_loop()  构造这个循环
loop.run_until_complete(任务) 将任务放置再任务列表
~~~

#### 2.协程函数和协程对象

协程函数 ，再定义函数时 加上 async def，

协程对象，执行协程函数得到协程对象

~~~
async def func():
	pass
result=func()
~~~

内部代码不执行，只获得协程对象

如果想要运行协程函数，必须要将协程对象交给事件循环处理

可简化为

~~~
asyncio.run(协程对象)

~~~



#### 3.await关键字

await + 可等待对象

可等待对象主要有(协程对象,Future对象,task对象)

await遇到协程对象时，会跳转到改对象内部执行代码

await就是等待对象的值得到结果后继续往下执行

#### 4.task对象

在事件循环中并发的添加多个任务

可以使用asyncio.create_task()创建该对象

~~~python
eg:import asyncio
async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return "返回值"
async def main():
    print("main开始")
    task_list=[
        asyncio.create_task(func(),name='n1'),
        asyncio.create_task(func(),name='n2')
    ]
    done,pending=await asyncio.wait(task_list,timeout=None) ###timeout可以限制时间，如果超时了那么他的返回值则放到pending中，否则放在done中
    print(done,pending)
asyncio.run(main())



~~~
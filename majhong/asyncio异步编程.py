import asyncio
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
    print(type(list(done)[0]))
asyncio.run(main())


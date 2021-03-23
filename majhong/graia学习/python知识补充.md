#### 生成器函数

- 只要含有yield关键字的函数都是生成器函数
- yield不能和return公用
- yield必须写在函数内部
- return返回之后函数直接结束，而yield返回之后函数并不会结束。

- 生成器函数可以使用next()迭代，且每次next()只会返回一次yield的值，然后暂停，下次一次next()时会在当前位置继续，如果没有元素可以迭代了，还 执在行next()则需要给定一个默认值，不给默认值会报错；
- 如果在生成器函数中使用return，则会终止迭代，且不能得到返回值；

~~~
eg:def add():
    for i in range(10):
        yield i
g = add()
print(g)  # <generator object add at 0x10f6110f8>
print(next(g))  # 0
print(next(g))  # 1
~~~

#### 异步函数

我们可以使用async修饰将普通函数和生成器函数包装成异步函数和异步生成器。

```python
async def async_function():
    return 1
```

直接调用异步函数并不会获得返回值,而是返回一个coroutine对象

协程需要通过其他方式来驱动，因此可以使用这个协程对象的send方法给协程发送一个值：

```python
print(async_function().send(None))
```

然而如果通过上面的调用会抛出一个异常：

```python
StopIteration: 1
```

因为生成器/协程在正常返回退出时会抛出一个StopIteration异常，而原来的返回值会存放在StopIteration对象的value属性中，通过以下捕获可以获取协程真正的返回值：

```python
try:
    async_function().send(None)
except StopIteration as e:
    print(e.value)
```

在协程函数中，可以通过await语法来挂起自身的协程，并等待另一个协程完成直到返回结果：

```python
async def async_function():
    return 1

async def await_coroutine():
    result = await async_function()
    print(result)
    
run(await_coroutine())
# 1
```

await 的作用就是等待协程完成来返回结果

#### 函数装饰器

装饰器让你在一个函数的前后去执行代码

例如我想要在某函数前后再额外执行一些指令，那么我可以通过@修饰改函数来实现

eg:

~~~
from functools import wraps
def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)
    return decorated
 
@decorator_name
def func():
    return("Function is running")
 
can_run = True
print(func())
# Output: Function is running
 
can_run = False
print(func())
# Output: Function will not run
~~~

###### 常见应用

授权，它常常可以检验一个人是哦否被授权去使用一个web应用的端点（endpoint）

~~~python
from functools import wraps
def require_auth(f):
 	@wraps(f)
 	 def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
~~~

#### cls的含义

一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。

而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用

eg:

class A(object):

@staticmethod

def foo1(name):

print 'hello', name

def foo2(self, name):

print 'hello', name

@classmethod

def foo3(cls, name):

print 'hello', name
#### .friend模块

该类有个三个对象，id（qq号），nickname（昵称）,remark(评论)没有什么好说的

#### .group模块

```
class MemberPerm(Enum):
    "描述群成员在群组中所具备的权限"

    Member = "MEMBER"  # 普通成员
    Administrator = "ADMINISTRATOR"  # 管理员
    Owner = "OWNER"  # 群主
```

#### [graia](https://graiaproject.github.io/Application/graia.html).[application](https://graiaproject.github.io/Application/graia/application.html).[message](https://graiaproject.github.io/Application/graia/application/message.html).chain

首先由几个消息元素的类型："Plain", "At", "Image"

##### 几个重要的函数

1.从传入的序列(可以是元组 tuple, 也可以是列表 list) 创建消息链.

~~~
def create(
	cls,
	elements: Sequence[graia.application.message.elements.Element]
) -> graia.application.message.chain.MessageChain:
~~~



###### Args

- **elements (Sequence[T]):** 包含且仅包含消息元素的序列

###### Returns

> MessageChain: 以传入的序列作为所承载消息的消息链

2.内部接口, 会自动将作为外部态的消息元素转为内部态.

```
def parse_obj(cls: Type["MessageChain"], obj: List[Element]) -> 
```

3.get()

~~~
def get(self, element_class: Element) -> List[Element]:
        """获取消息链中所有特定类型的消息元素

        Args:
            element_class (T): 指定的消息元素的类型, 例如 "Plain", "At", "Image" 等.

        Returns:
            List[T]: 获取到的符合要求的所有消息元素; 另: 可能是空列表([]).
        """
        return [i for i in self.__root__ if type(i) is element_class]
~~~



#### graia.application模块

###### Attributes(属性)

- **broadcast (Broadcast):** 被指定的, 外置的事件系统, 即 `Broadcast Control`,
- **session (ClientSession):** 即 `aiohttp.ClientSession` 的实例, 用于与 `mirai-api-http` 通讯.
- **connectinfo (Session):** 用于描述会话对象, 其中最重要的属性是 `sessionKey`, 用于存储当前的会话标识.
- **logger (AbstractLogger):** 日志系统实现类的实例, 默认以 `logging` 为日志驱动.

##### 以下是我认为几个比较重要的模块

@error_wrapper

@requireAuthenticated

@applicationContextManager

**async def** **groupList**(self) -> List[[graia.application.group.Group](https://graiaproject.github.io/Application/graia/application/group.html#Group)]:

<details style="box-sizing: border-box; --shift: -40px; text-align: right; margin-top: var(--shift); margin-bottom: calc(0px - var(--shift)); clear: both; height: 0px; overflow: visible; color: rgb(33, 37, 41); font-family: system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;"><summary class="button" style="box-sizing: border-box; display: inline-block; cursor: pointer; border: 0px solid black; border-radius: 2px; font-size: 0.75rem; padding: 0px 0.7em; transition: all 100ms ease 0s; color: rgb(102, 102, 102); user-select: none;">View Source</summary></details>

获取当前会话账号所加入的所有群组的信息.

###### Returns

> List[Group]: 当前会话账号所加入的所有群组的信息


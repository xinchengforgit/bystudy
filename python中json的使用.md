##### python中json的使用

经过一下午试用了一下午jsoncpp，我决定放弃c++，太难用了QAQ，所以我改用了python(然后忘了很多只能边用边查)

##### 1.json导入

~~~
json.dumps 	将 Python 对象编码成 JSON 字符串
对应的关系为
dict	object
list, tuple	array
str, unicode	string
int, long, float	number
True	true
False	false
None	null
~~~

##### 2.json解码

~~~
json.loads 用于解码 JSON 数据。该函数返回 Python 字段的数据类型

~~~


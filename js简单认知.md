

### js学习

#### 1.js嵌入html的方法

JS是一门事件驱动型的编程语言,在JS中有很多事件，其中有一个事件是鼠标点击，单词:click，并且任何事件都会对应一个事件句柄，它是html标签的属性存在的

事件句柄内可以写JS代码，事件发生后执行

eg：js嵌入html的三种方式

##### 1.用js代码弹出消息框

例如在js中有一个内置对象叫做window,有一个函数叫alert

window.alter("消息");即可弹窗

~~~javascript
  eg:<input type="button" value="hello" onclick="window.alert('hello my js')" />
  //window可省略
~~~

##### 2.脚本块的方式

~~~javascript
 <script type="text/javascript">
 	js语句1
 	js语句2
    </script>
~~~

暴露在脚本块中的程序，在页面打开时执行，并且遵守自上而下的顺序依次执行



##### 3.将js代码写在一个单独的文件中

在需要的位置写上  <script type="text/javascript" src="xxx"></script>

同一个js文件可以被引入多次

#### 2.js变量

声明方法 var 变量名;

给变量赋值 变量名=值

js中的变量可以随意赋值(undefined也是一种值)

弱类型,右边是什么类型左边就是什么类型

###### 1.局部和全局变量

在函数体之外声明的变量属于全局变量，浏览器打开时声明关闭时销毁(占内存多)

在函数体中声明的变量，函数开始到函数结束的生命周期

**注意：当一个变量声明的时候没有加var关键字，无论在何处声明的，都是全局变量**

#### 3.函数

语法格式

1.function 函数名=(形参列表){

函数体

}

2.函数名=function(形参列表){

函数体

}

#### 4.数据类型

重点：Object类型

Object类型是所有类型的超类，默认继承Object类，

Object类包括 Prototype 属性（给类动态扩展属性和函数） ，constructor属性。

Object类默认包括 toString()，valueof()，toLocaleString()函数

定义方法：

1.function 类名(形参)

{
}

2.类名=function(形参)

{
}

创建对象的语法， new 构造方法名（形参） 

~~~javascript
eg:  function Student() {

        }
        var stu = new (Student)
~~~

声明属性(this表示当前对象)

~~~javascript
  function Student(a, b) {
            this.name = a
            this.val = b
      		this,getval =function()
            {
                return this.val //对象中的函数
			}
        }
~~~

访问属性拿.即可

可以通过prototype这个属性来给类动态扩展属性和函数

~~~javascript
Student.prototype.getval=function()
{
	return this.val
}
~~~

####  5.注册事件的基本方式

任何一个事件都对应一个事件句柄，事件句柄是在事件前添加on，

onxxx出现在一个标签的属性上

###### 1.使用回调函数

在程序中写出了函数，但由其他程序负责调用

~~~javascript
eg：<script type="text/javascript">
        function sayhello() {
            alert("hello")
        }
    </script>
    <input type="button" value="hello" onclick="sayhello()">
~~~

###### 2.使用纯js代码

1.先获取对象的id

2.给对象的事件句柄赋值

~~~javascript
 eg: <input type="input" id="1" value="hello">
    <script type="text/javascript">
        function sayhello() {
            alert("hello")
        }
        var obj = document.getElementById("1")
        obj.onclick = sayhello//注意此处不加括号
    </script>
~~~

void运算符,void()执行内部表达式，但不返回值

javascript:表示告诉浏览器后面是一段js代码
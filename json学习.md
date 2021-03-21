#### json简介

JavaScript object notation //数据交换格式

特点是:体积小，容易解析

##### 1.定义方法

~~~json
json的定义方法
  var jsonobj = {
            "sno": "110",
            "sname": "zhangsan",
            "ssex": "nan"
        }
        //json数组
        var stuents = [{ "sno": "110", "sname": "zhangsan" }, { "sno": "120", "sname": "lisi" }]
        for (var i = 0; i < stuents.length; i++) {
            var student = stuents[i]
        }//获取对象的方法，遍历即可
~~~



形如 key : value的格式

##### 2.复杂一些的json对象

~~~json
var user = {
            "userno": "110",
            "username": "zhangsan",
            "sex": "nan",
            "address": {
                "city": "jiangxi",
                "street": "kangle"
            }
        }
      //即value值可以是另一个json对象
      //user.address.city可以访问到"jiangxi"
~~~

##### 3.eval函数

eval函数可以将""里面的字符串当作js代码执行

也即是可以使用json格式的字符串转化为json对象


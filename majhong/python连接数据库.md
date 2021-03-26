#### python链接数据库

通过导入pymysql实现

首先建立连接

后面就是要连接的数据库的各项基本信息

conn=pymysql.connect()

cursor=conn.cursor()

可以获得数据库的游标,

cursor.excute(sql语句)

这样就可以执行sql语句了

如果是提交或者更新数据的话

conn.commit()来更新数据库
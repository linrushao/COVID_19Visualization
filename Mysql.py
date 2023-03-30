import pymysql

class Mysql(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='localhost',user='root',password='linrushao',database='covid',charset="utf8")
            self.cursor = self.conn.cursor()  # 游标对象
            print("连接数据库成功")
        except:
            print("连接失败")

    def getItems(self,page,keyword=None):
        sql = "select * from details"
        if keyword:
            sql = sql + " where province like '%" + keyword + "%'"
        self.cursor.execute(sql)
        items = self.cursor.fetchall()
        return items

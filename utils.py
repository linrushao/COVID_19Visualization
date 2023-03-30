import time
import pymysql


def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


def get_conn():
    # 建立连接
    conn = pymysql.connect(host="localhost", user="root", password="linrushao", db="web", charset="utf8")
    # c创建游标A
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    """

    :param sql:
    :param args:
    :return:
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def test():
    sql = "select * from details"
    res = query(sql)
    return res[0]


def get_c1_data():
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal),sum(dead) from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    return res[0]


def get_c2_data():
    sql = "SELECT SUM(vaccine_total) FROM vaccine"
    sql1 = 'SELECT vaccine_total FROM vaccine WHERE country = "中国"'
    res = query(sql)
    res1 = query(sql1)
    return res[0][0],res1[0][0]

def get_c3_data():
    sql = "SELECT content FROM vaccine_hotsearch"
    res = query(sql)
    list = []
    for i in res:
        # print(i[0])
        list.append(i[0])
    list1 = tuple(list)
    return list1

def get_c4_data():
    sql = "SELECT province,SUM(confirm) AS confirm FROM details WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1) GROUP BY province ORDER BY confirm DESC"
    res = query(sql)
    return res


def get_l1_data():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


def get_l2_data():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res


def get_r1_data():
    sql = "SELECT province,SUM(confirm) AS confirm FROM details where update_time=(select update_time from details order by update_time desc limit 1) GROUP BY province ORDER BY confirm DESC LIMIT 5"
    res = query(sql)
    return res


def get_r2_data():
    sql = "SELECT country,vaccine_total FROM vaccine ORDER BY vaccine_total DESC LIMIT 10"
    res = query(sql)
    return res


if __name__ == "__main__":
    # print(get_l1_data())
    # print(get_l2_data())
    # print(get_c1_data())
    # print(get_c2_data())
    print(get_r1_data())
    # print(test())
    # print(get_c4_data())
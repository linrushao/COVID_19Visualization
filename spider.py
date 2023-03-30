import sys
import pymysql
import json
import traceback
from selenium.webdriver import Chrome, ChromeOptions
import requests  # 自动爬去html页面，自动请求网络提交
from bs4 import BeautifulSoup  # 解析HTML/XMl页面，提取数据或信息
import time
from lxml import etree


def get_tencent_data():
    url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    url2 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    r1 = requests.get(url1, headers)
    r2 = requests.get(url2, headers)

    res1 = json.loads(r1.text,strict=False)
    res2 = json.loads(r2.text)

    data_all1 = res1["data"]
    data_all2 = json.loads(res2["data"])

    history = {}
    for i in data_all2["chinaDayList"]:
        ds = "2022." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_all2["chinaDayAddList"]:
        ds = "2022." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    details = []
    update_time = data_all1["lastUpdateTime"]
    data_country = data_all1["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return history, details

#疫苗数据
def parse_vaccine_data():
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=VaccineSituationData'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    }

    response = requests.post(url=url, headers=headers, timeout=3)

    data = response.text
    data_dict = json.loads(data)
    all_data = data_dict['data']['VaccineSituationData']
    temp = []
    index=0
    while index < len(all_data):
        country = all_data[index]['country']
        vaccine_date = all_data[index]['date']
        vaccine_type_c = all_data[index]['vaccinations']
        vaccine_total = str(all_data[index]['total_vaccinations'])
        vaccine_every = str(all_data[index]['total_vaccinations_per_hundred'])
        temp.append([country, vaccine_date, vaccine_type_c, vaccine_total, vaccine_every])
        index +=1
    return temp
        # print(
        #     '国家:' + country + '  ' + '日期:' + date + '  ' + '接种类型:' + type_c + '  ' + '累计接种/亿剂:' + all + '  ' + '每百人/亿剂:' + every)

def get_conn():
    # 建立连接
    conn = pymysql.connect(host="localhost", user="root", password="linrushao", db="web", charset="utf8")
    # c创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# 定义更新细节函数
def update_details():
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]  # 1代表最新数据
        conn, cursor = get_conn()
        sql1 = "truncate table details"
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
        # 对比当前最大时间戳

        li1 = li[0][0].split(" ")
        li2 = li1[0]
        cursor.execute(sql_query, li2)
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新疫情数据")
            cursor.execute(sql1)
            for item in li:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}疫情更新到最新数据")
        else:
            print(f"{time.asctime()}疫情已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)



# 插入历史数据
def insert_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0代表历史数据字典
        print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()
        sql1 = "truncate table history"
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            cursor.execute(sql1)
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# 更新历史数据
def update_history():
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0代表历史数据字典
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql1 = "truncate table history"
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        cursor.execute(sql1)
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

#疫苗数据更新
def update_details_vaccine():
    cursor = None
    conn = None
    try:
        dic = parse_vaccine_data()  # 0代表历史数据字典
        print(f"{time.asctime()}开始更新疫苗数据")
        conn, cursor = get_conn()
        sql1 = "truncate table vaccine"
        sql = "insert into vaccine(country, vaccine_date, vaccine_type_c, vaccine_total, vaccine_every) values(%s, %s, %s, %s, %s)"
        sql_query = 'select %s = (SELECT vaccine_date FROM vaccine ORDER BY id ASC LIMIT 1)'
        # 对比当前最大时间戳
        cursor.execute(sql_query, dic[0][1])
        if not cursor.fetchone()[0]:
            cursor.execute(sql1)
            print(f"{time.asctime()}开始更新疫苗数据")
            for item in dic:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}疫苗更新到最新数据")
        else:
            print(f"{time.asctime()}疫苗已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)



# 爬取热搜数据
def get_baidu_hot():

    url = 'https://top.baidu.com/board?tab=realtime'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    urls = requests.get(url, headers=headers)

    # 获取 response header时间
    # datatime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    urls.encoding = urls.apparent_encoding
    text = urls.text
    soup = BeautifulSoup(text, 'lxml')  # 网页解析器

    # #爬取标题
    # for i in soup.find_all(class_="c-single-text-ellipsis"):
    #     print(i.get_text())

    a = soup.find_all(class_="c-single-text-ellipsis")
    context = [i.get_text().strip() for i in a]
    return context



def update_hotsearch():
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()}开始更新热搜数据")
        conn, cursor = get_conn()
        sql1 = "truncate table hotsearch"
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        cursor.execute(sql1)
        for i in context:
            cursor.execute(sql, (ts, i))
        conn.commit()
        print(f"{time.asctime()}热搜数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

#爬取疫情热搜
def get_vaccine_hot():
    url = 'https://www.0797cx.cn/page213'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    urls = requests.get(url, headers=headers)

    urls.encoding = urls.apparent_encoding
    text = urls.text
    # print(soup)
    html_obj = etree.HTML(text)
    name_top = html_obj.xpath('//*[@id="layer70E54FE7C5A203100D4CACFC9DCA850D"]/div/div[2]/ul/li/p[1]/a/text()')
    # print(name_top)
    return name_top

def update_vaccine_hotsearch():
    cursor = None
    conn = None
    try:
        context = get_vaccine_hot()
        print(f"{time.asctime()}开始更新疫情热搜数据")
        conn, cursor = get_conn()
        sql1 = "truncate table vaccine_hotsearch"
        sql = "insert into vaccine_hotsearch(content) values(%s)"
        cursor.execute(sql1)
        for i in context:
            cursor.execute(sql,  i)
        conn.commit()
        print(f"{time.asctime()}疫情热搜数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == "__main__":
    # update_details_vaccine()
    get_tencent_data()
    # update_details()
    # insert_history()
    # update_history()
    # get_vaccine_hot()
    # update_hotsearch()
    # update_vaccine_hotsearch()
    # l = len(sys.argv)
    # if l == 1:
    #     s = """
    #     请输入参数
    #     参数说明，
    #     up_his 更新历史记录表
    #     up_hot 更新实时热搜
    #     up_det 更新详细表
    #     up_vaccine 更新疫苗表
    #     up_hot 更新实时疫情热搜
    #     """
    #     print(s)
    # else:
    #     order = sys.argv[1]
    #     if order == "up_his":
    #         update_history()
    #     elif order == "up_det":
    #         update_details()
    #     elif order == "up_hot":
    #         update_hotsearch()
    #     elif order == "up_vaccine":
    #         update_details_vaccine()
    #     elif order == "up_vaccine_search":
    #         update_vaccine_hotsearch()

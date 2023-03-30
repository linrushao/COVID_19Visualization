import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
import sys
import pymysql
sys.setrecursionlimit(100000)

class CoronaVirusSpider():

    def __init__(self):
        self.home_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'

    def get_conn(self):
        # 建立连接
        conn = pymysql.connect(host="localhost", user="root", password="linrushao", db="covid", charset="utf8")
        # c创建游标
        cursor = conn.cursor()
        return conn, cursor

    def close_conn(self,conn, cursor):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def get_content_from_url(self, url):
        response = requests.get(url)
        return response.content.decode('utf-8')

    def crawl_last_day_corona_virus_of_china(self):
        home_page = self.get_content_from_url(self.home_url)
        soup = BeautifulSoup(home_page, 'lxml')
        script = soup.find(id='getAreaStat')
        text = script.text

        json_str = re.findall(r'\[.+\]', text)[0]
        last_day_corona_virus_of_china = json.loads(json_str)
        corona_virus = []
        province = last_day_corona_virus_of_china[0]
        statistics_data_url = province['statisticsData']
        url = self.get_content_from_url(statistics_data_url)
        one_day = json.loads(url)["data"][0]
        print(one_day)
        one_day['provinceName'] = province['provinceName']
        print(one_day)
        # for province in tqdm(last_day_corona_virus_of_china, "采集1月22以来各省疫情信息"):
        #     statistics_data_url =province['statisticsData']
        #     statistics_data_json_str = self.get_content_from_url(statistics_data_url)
        #     statistics_data = json.loads(statistics_data_json_str)['data']
        #     for one_day in statistics_data:
        #         one_day['provinceName'] = province['provinceName']
        #     corona_virus.extend(statistics_data)
        # print(corona_virus)

if __name__ == '__main__':
    spider = CoronaVirusSpider().crawl_last_day_corona_virus_of_china()


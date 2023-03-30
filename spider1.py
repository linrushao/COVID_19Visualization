import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
import sys
sys.setrecursionlimit(100000)


class CoronaVirusSpider():

    def __init__(self):
        self.home_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'

    def get_content_from_url(self, url):
        response = requests.get(url)
        return response.content.decode('utf-8')

    def save(self, data, path):
        with open(path, 'w', encoding='utf-8')as fp:
            json.dump(data, fp, ensure_ascii=False)

    def crawl_last_day_corona_virus_of_china(self):
        home_page = self.get_content_from_url(self.home_url)
        soup = BeautifulSoup(home_page, 'lxml')
        script = soup.find(id='getAreaStat')
        text = script.text

        json_str = re.findall(r'\[.+\]', text)[0]
        data = json.loads(json_str)
        self.save(data, './data/last_day_corona_virus_of_china.json')

    def crawl_corona_virus_of_china(self):
        with open('./data/last_day_corona_virus_of_china.json',encoding='utf-8') as fp:
            last_day_corona_virus_of_china = json.load(fp)
        corona_virus = []
        for province in tqdm(last_day_corona_virus_of_china, "采集1月22以来各省疫情信息"):
            statistics_data_url =province['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']

            for one_day in statistics_data:
                one_day['provinceName'] = province['provinceName']
            corona_virus.extend(statistics_data)
            #print(corona_virus)
        self.save(corona_virus, './data/corona_virus_of_china.json')

    def crawl_corona_virus_of_GD(self):
        with open('./data/last_day_corona_virus_of_china.json', encoding='utf-8') as fp:
            last_day_corona_virus_of_china = json.load(fp)
        #print(last_day_corona_virus_of_china)
        dict_province_data = {}
        for i in last_day_corona_virus_of_china:
            for k in i.values():
                if k =='广东':
                    dict_province_data = i

        list_province_data = []
        list_province_data.append(dict_province_data)
        with open('./data/json_GD_data.json', 'w', encoding='utf-8')as fp:
            json.dump(list_province_data, fp, ensure_ascii=False)
        with open('./data/json_GD_data.json',encoding='utf-8') as fp:
            GD_data = json.load(fp)
        for province in tqdm(GD_data, "采集1月22以来广东省疫情信息"):
            statistics_data_url = province['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
        res_t = []
        res_z = []
        for i in statistics_data:
            times = i.get("dateId")
            per = i.get("confirmedIncr")
            res_t.append(times)
            res_z.append(per)
        return {"time": res_t, "price": res_z}

    def crawl_corona_virus_of_XG(self):
        with open('./data/last_day_corona_virus_of_china.json', encoding='utf-8') as fp:
            last_day_corona_virus_of_china = json.load(fp)
        #print(last_day_corona_virus_of_china)
        dict_province_data = {}
        for i in last_day_corona_virus_of_china:
            for k in i.values():
                if k =='香港':
                    dict_province_data = i

        list_province_data = []
        list_province_data.append(dict_province_data)
        with open('./data/json_XG_data.json', 'w', encoding='utf-8')as fp:
            json.dump(list_province_data, fp, ensure_ascii=False)
        with open('./data/json_XG_data.json',encoding='utf-8') as fp:
            XG_data = json.load(fp)
        for province in tqdm(XG_data, "采集1月22以来香港省疫情信息"):
            statistics_data_url = province['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
        res_t = []
        res_z = []
        for i in statistics_data:
            times = i.get("dateId")
            per = i.get("confirmedIncr")
            res_t.append(times)
            res_z.append(per)
        return {"time": res_t, "price": res_z}

    def crawl_corona_virus_of_JL(self):
        with open('./data/last_day_corona_virus_of_china.json', encoding='utf-8') as fp:
            last_day_corona_virus_of_china = json.load(fp)
        #print(last_day_corona_virus_of_china)
        dict_province_data = {}
        for i in last_day_corona_virus_of_china:
            for k in i.values():
                if k =='吉林':
                    dict_province_data = i

        list_province_data = []
        list_province_data.append(dict_province_data)
        with open('./data/json_JL_data.json', 'w', encoding='utf-8')as fp:
            json.dump(list_province_data, fp, ensure_ascii=False)
        with open('./data/json_JL_data.json',encoding='utf-8') as fp:
            JL_data = json.load(fp)
        for province in tqdm(JL_data, "采集1月22以来吉林省疫情信息"):
            statistics_data_url = province['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
        res_t = []
        res_z = []
        for i in statistics_data:
            times = i.get("dateId")
            per = i.get("confirmedIncr")
            res_t.append(times)
            res_z.append(per)
        return {"time": res_t, "price": res_z}

    def crawl_corona_virus_of_SH(self):
        with open('./data/last_day_corona_virus_of_china.json', encoding='utf-8') as fp:
            last_day_corona_virus_of_china = json.load(fp)
        #print(last_day_corona_virus_of_china)
        dict_province_data = {}
        for i in last_day_corona_virus_of_china:
            for k in i.values():
                if k =='上海':
                    dict_province_data = i

        list_province_data = []
        list_province_data.append(dict_province_data)
        with open('./data/json_SH_data.json', 'w', encoding='utf-8')as fp:
            json.dump(list_province_data, fp, ensure_ascii=False)
        with open('./data/json_SH_data.json',encoding='utf-8') as fp:
            SH_data = json.load(fp)
        for province in tqdm(SH_data, "采集1月22以来吉林省疫情信息"):
            statistics_data_url = province['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
        res_t = []
        res_z = []
        for i in statistics_data:
            times = i.get("dateId")
            per = i.get("confirmedIncr")
            res_t.append(times)
            res_z.append(per)
        return {"time": res_t, "price": res_z}

    def crawl_corona_virus(self, key):
        with open('./data/last_day_corona_virus_of_china.json', encoding='utf-8') as fp:
            last_day_corona_virus_of_china = json.load(fp)
        #print(last_day_corona_virus_of_china)
        dict_province_data = {}
        for i in last_day_corona_virus_of_china:
            for k in i.values():
                if k ==key:
                    dict_province_data = i

        list_province_data = []
        list_province_data.append(dict_province_data)
        with open("./data/json_'{}'_data.json".format(key), 'w', encoding='utf-8')as fp:
            json.dump(list_province_data, fp, ensure_ascii=False)
        with open("./data/json_'{}'_data.json".format(key), encoding='utf-8') as fp:
            data = json.load(fp)
        for province in tqdm(data, "采集1月22以来该省疫情信息"):
            statistics_data_url = province['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            statistics_data = json.loads(statistics_data_json_str)['data']
        res_t = []
        res_z = []
        res_v = []
        res_f = []
        res_z = []
        for i in statistics_data:
            times = i.get("dateId")
            per = i.get("confirmedIncr")
            incr = i.get("curedIncr")
            sum = i.get("confirmedCount")
            now = i.get("currentConfirmedCount")
            res_t.append(times)
            res_z.append(per)
            res_v.append(incr)
            res_f.append(sum)
            res_z.append(now)
        return {"time": res_t, "price": res_z, "incr": res_v, "sum": res_f[-1], "now": res_z[-1]}

    def run(self):
       print(self.crawl_corona_virus("广东"))
if __name__ == '__main__':
    spider = CoronaVirusSpider().crawl_corona_virus_of_china()

    spider.run()





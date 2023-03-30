import pymysql
from flask import Flask as _Flask, jsonify
from flask import request
from flask import render_template
from flask.json import JSONEncoder as _JSONEncoder
from jieba.analyse import extract_tags
import decimal
import utils
import string
from spider1 import CoronaVirusSpider


from Mysql import Mysql


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(_JSONEncoder, self).default(o)


class Flask(_Flask):
    json_encoder = JSONEncoder


app = Flask(__name__)


@app.route('/')
def hello_word3():
    return render_template("main.html")

# @app.route('/index')
# def name():
#     db = Mysql()
#     keyword = request.args.get('keyword')
#     items = db.getItems( keyword)
#     return render_template('index.html', items=items)

@app.route('/phc')
def index():
    return render_template('demo1.html')

@app.route('/api')
def get_data():
    key = request.args.get('key')


    get_value =CoronaVirusSpider().crawl_corona_virus(key)
    return jsonify({'data': get_value, 'success': 0})

# @app.route('/gets/',methods=['POST'])
# def search():
#     conn = pymysql.connect(user='root', host='localhost', passwd='linrushao', db='web',cursorclass=pymysql.cursors.DictCursor)
#     cur = conn.cursor()
#     S = request.values.get('question')
#     sql = "select province,city,confirm,confirm_add,heal,dead from details where province like '%"+S+"%'"
#     cur.execute(sql)
#     datas = cur.fetchall()
#     return render_template('index.html',items=datas)

@app.route('/time')
def get_time():
    return utils.get_time()


@app.route('/c1')
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({"confirm": data[0], "suspect": data[1], "heal": data[2], "dead": data[3]})


@app.route('/c2')
def get_c2_data():
    data = utils.get_c2_data()
    return jsonify({"vaccine_sj": data[0], "vaccine_zg": data[1]})

@app.route('/c3')
def get_c3_data():
    data = utils.get_c3_data()
    return jsonify(data)

@app.route('/c4')
def get_c4_data():
    data = utils.get_c4_data()
    d = []
    for i in data:
        k = i[0]
        v = i[1]
        d.append({"name": k,"value": v})
    return jsonify({"kws": d})

@app.route('/l1')
def get_l1_data():
    data = utils.get_l1_data()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for a, b, c, d, e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


@app.route('/l2')
def get_l2_data():
    data = utils.get_l2_data()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


@app.route('/r1')
def get_r1_data():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k, v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


@app.route('/r2')
def get_r2_data():
    data = utils.get_r2_data()
    res = []
    for tup in data:
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({'data': res})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

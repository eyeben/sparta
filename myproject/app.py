from flask import Flask, render_template, jsonify, request
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.data  # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantexts = re.split(cleanr, raw_html)
    lists = []
    for i in cleantexts:
        if (i != '' and i != '\n'):
            lists.append(i)
    cleantext = re.sub(cleanr, '/', raw_html)
    if len(lists) != 0:
        return lists


def get_context(url_comes_here, range_comes_here):
    data_list = []
    source = requests.get(url_comes_here, headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(source.text, 'html.parser')

    # select를 이용해서, tr들을 불러오기
    first_data = soup.select(range_comes_here)
    for i in first_data:
        data_list.append(cleanhtml(str(i)))
    return data_list


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/data', methods=['POST'])
def write_data():
    form_receive = request.form['give_form']
    title_receive = request.form['give_title']
    url_receive = request.form['give_url']
    keyword_receive = request.form['give_keyword']
    range_receive = request.form['give_range']
    if len(range_receive) == 0:
        range_receive = 'html'
    context1 = get_context(url_receive, range_receive)
    if form_receive == 'm':

        included=[]
        for i in context1[0]:
            if keyword_receive in i:
                included.append(i)
        print(included)
        data = {
            'form': form_receive,
            'title': title_receive,
            'url': url_receive,
            'keyword': keyword_receive,
            'range': range_receive,
            'compare1': included,   # 구, 신
            'compare2': included
        }
    else:
        data = {
            'form': form_receive,
            'title': title_receive,
            'url': url_receive,
            'keyword': keyword_receive,
            'range': range_receive,
            'compare1': context1,
            'compare2': context1
        }
    db.data.insert_one(data)
    print(data)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '작성 성공'})


@app.route('/data/update', methods=['POST'])
def gangshin():
    title = request.form['give_title']
    print(title)

    datas = list(db.data.find({}, {'_id': False}))

    for da in datas:
        try:
            new_context = get_context(da['url'], da['range'])
            answer = []
            for i in new_context:
                answer += i
            db.data.update_one({'title': da['title']}, {'$pull': {'compare1'}})
            db.data.update_one({'title': da['title']}, {'$set': {'compare1': da['compare2']}})
            db.data.update_one({'title': da['title']}, {'$pull': {'compare2'}})
            db.data.update_one({'title': da['title']}, {'$set': {'compare2': answer}})
            print('[',answer,']')
        except ValueError:
            continue


    return jsonify({'result': 'success'})


@app.route('/data', methods=['GET'])
def recieve_data():
    datas = list(db.data.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'msg': datas})


@app.route('/data', methods=['DELETE'])
def remove_chunk():
    title = request.form['title_give']
    db.data.delete_one({'title': title})
    return jsonify({'result': 'success'})


# 15.164.94.252
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

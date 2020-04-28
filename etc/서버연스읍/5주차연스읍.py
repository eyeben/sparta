from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.물살사람                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/orders', methods=['POST'])
def write_review():
    name_receive = request.form['name_give']
    amount_receive = request.form['amount_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    info = {
        'name': name_receive,
        'amount': amount_receive,
        'address': address_receive,
        'phone': phone_receive
    }
    db.orders.insert_one(info)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '작성 성공'})


@app.route('/orders', methods=['GET'])
def read_reviews():
    list_all=list(db.orders.find({},{'_id':0}))
    print(list_all)
    return jsonify({'result': 'success', 'msg': list_all})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
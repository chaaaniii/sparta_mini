from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.2frhcdl.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

#메인 화면

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/cheers", methods=["POST"])
def cheer_post():
    nickname_receive = request.form['nickname_give']
    cheer_receive = request.form['cheer_give']

    cheer_list = list(db.cheerpost.find({}, {'_id': False}))
    count = len(cheer_list) + 1

    doc = {
        'nickname': nickname_receive,
        'cheer':cheer_receive,
    }
    db.cheerpost.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/cheers", methods=["GET"])
def bucket_get():
    cheer_list = list(db.cheerpost.find({}, {'_id': False}))
    return jsonify({'cheer': cheer_list})

# 팀원 상세 페이지

@app.route('/detail')
def detail():
    return render_template('sub_page_1.html')

@app.route("/details", methods=["GET"])
def web_detail_get():
    user_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'user': user_list})

# 상세페이지 댓글 부분

@app.route("/comments", methods=["POST"])
def comment_post():
    member_no = request.form.get('memberNum_give',False)
    username_receive = request.form.get('username_give',False)
    comment_receive = request.form.get('comment_give',False)

    print(member_no)
    comment_list = list(db.commentdb.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'username': username_receive,
        'comment':comment_receive,
        'member_no':member_no
    }
    db.commentdb.insert_one(doc)

    return jsonify({'msg':'댓글 등록!'})

@app.route("/comments", methods=["GET"])
def comment_get():
    comment_list = list(db.commentdb.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
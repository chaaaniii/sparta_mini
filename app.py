from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.2frhcdl.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

#메인 화면

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/cheers", methods=["POST"])
def cheer_post():
    nickname_receive = request.form['nickname_give']
    cheer_receive = request.form['cheer_give']
    num_receive = request.form.get('num_give')
    pwd_receive = request.form.get('pwd_give')

    cheer_list = list(db.cheerpost.find({}, {'_id': False}))
    count = len(cheer_list) + 1

    doc = {
        'chnum':count,
        'nickname': nickname_receive,
        'cheer':cheer_receive,
        'saved_pwd':pwd_receive
    }
    db.cheerpost.insert_one(doc)
    return jsonify({'msg': '방명록 등록 완료!'})

@app.route("/cheers", methods=["GET"])
def cheer_get():
    cheer_list = list(db.cheerpost.find({}, {'_id': False}))
    return jsonify({'cheer': cheer_list})

@app.route("/cheers", methods=["DELETE"])
def cheer_delete():
    num_receive = request.form.get('chnum_give')
    # if(pwd_receive == comp_pwd):
    db.cheerpost.delete_one({'chnum': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})

# 팀원 상세 페이지

@app.route('/detail')
def detail():
    return render_template('sub_page_1.html')

@app.route("/details", methods=["GET"])
def web_detail_get():
    user_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'user': user_list})

@app.route("/tmis",methods=["GET"])
def web_tmi_get():
    tmi_list = list(db.tmi.find({},{'_id':False}))
    return jsonify({'tmi':tmi_list})

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
        'member_no': int(member_no),
        'username': username_receive,
        'comment':comment_receive,
        'conum': count,
    }
    db.commentdb.insert_one(doc)

    return jsonify({'msg':'댓글 등록!'})

@app.route("/comments", methods=["GET"])
def comment_get():
    comment_list = list(db.commentdb.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

@app.route("/comments", methods=["DELETE"])
def comment_delete():
    conum_receive = request.form.get('conum_give')
    db.commentdb.delete_one({'conum': int(conum_receive)})
    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
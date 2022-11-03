from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('mongodb+srv://test:sparta@cluster0.2frhcdl.mongodb.net/Cluster0?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://test:sparta@cluster0.afmxt02.mongodb.net/Cluster0?retryWrites=true&w=majority')
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
    print("서버가 받은 cheer값",cheer_receive)

    cheer_list = list(db.cheerpost.find({}, {'_id': False}))
    count = len(cheer_list)



    doc = {
        'chnum':count,
        'nickname': nickname_receive,
        'cheer':cheer_receive,
        'saved_pwd':pwd_receive,
    }
    db.cheerpost.insert_one(doc)
    return jsonify({'msg': '방명록 등록 완료!'})

@app.route("/cheers", methods=["GET"])
def cheer_get():
    cheer_list = list(db.cheerpost.find({}, {'_id': False}))
    return jsonify({'cheer': cheer_list})

@app.route("/cheers", methods=["DELETE"])
def cheer_delete():
    idx_receive = request.form.get('idx_give')
    compPwd_receive = request.form.get('compPwd_give')
    

    print('인덱스 :',idx_receive, '생성할 때 넣은 비밀번호 :',db_pwd, '/ 삭제하려고 넣은 비밀번호 :',compPwd_receive)
    if db_pwd == None :
        db_pwd = ''
    elif compPwd_receive == None :
        compPwd_receive == ''

    if db_pwd == compPwd_receive:
        db.cheerpost.delete_one({'chnum': int(delNum_receive)})
        return jsonify({'msg': '삭제 완료'})
    else:
        return jsonify({'msg': '비밀번호가 틀렸습니다'})

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
    compwd_receive = request.form.get('compwd_give')

    # print(member_no)
    comment_list = list(db.commentdb.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'member_no': int(member_no),
        'username': username_receive,
        'comment':comment_receive,
        'conum': count,
        'saved_copwd': compwd_receive
    }
    db.commentdb.insert_one(doc)

    return jsonify({'msg':'댓글 등록!'})

@app.route("/comments", methods=["GET"])
def comment_get():
    comment_list = list(db.commentdb.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

@app.route("/comments", methods=["DELETE"])
def comment_delete():
    delConum_receive = request.form.get('conum_give')
    compPwd2_receive = request.form.get('compPwd2_give')
    db2_pwd = list(db.commentdb.find({}, {'_id': False}))[int(delConum_receive) - 1]['saved_copwd']

    print('삭제할 방명록 번호:', delConum_receive, '생성할 때 넣은 비밀번호 :',db2_pwd, '/ 삭제하려고 넣은 비밀번호 :',compPwd2_receive)
    if db2_pwd == None :
        db2_pwd = ''
    elif compPwd2_receive == None :
        compPwd2_receive == ''

    if db2_pwd == compPwd2_receive:
        db.commentdb.delete_one({'conum': int(delConum_receive)})
        return jsonify({'msg': '삭제 완료'})
    else:
        return jsonify({'msg': '비밀번호가 틀렸습니다'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)

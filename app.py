from flask import Flask, request, render_template, redirect, url_for, abort, session
import dbdb

app = Flask(__name__)

app.secret_key = b'aaa!111/'

@app.route('/')
def index():
    return render_template('main.html')
    
# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        ret = dbdb.select_user(id, pw)
        if ret != None:
            return "안녕하세요~ {} 님".format(id)
            #return '''
            #    <script> alert("안녕하세요~ {}님");
            #    location.href="/form"
            #    </script>
            #'''.format(id)
        else:
            return "아이디 또는 패스워드를 확인 하세요."

# 로그아웃(session 제거)
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('form'))
    
# 로그인 사용자만 접근 가능으로 만들면
@app.route('/form') 
def form():
    if 'user' in session:
        return render_template('test.html')
    return redirect(url_for('login'))

# 회원 가입
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        id = request.form["id"]
        pw = request.form["pw"]
        name = request.form["name"]
        ret = dbdb.check_id(id)
        if ret != None:
            return '''
                    <script>
                    alert('다른 아이디를 사용하세요');
                    location.href='/join';
                    </script>
                    '''
        # id와 pw가 db 값이랑 비교 해서 맞으면 맞다 틀리면 틀리다
        dbdb.insert_user(id, pw, name)
        return redirect(url_for('login'))

@app.route('/getinfo')
def getinfo():
    ret = dbdb.select_all()
    return render_template('getinfo.html', data=ret)

if __name__ == '__main__':
    app.run(debug=True)

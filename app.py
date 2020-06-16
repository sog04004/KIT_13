from flask import Flask, request, render_template, redirect, url_for, abort, session
import dbdb

app = Flask(__name__)

app.secret_key = b'aaa!111/'

@app.route('/')
def main():
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
            session['user'] = id
            return '''
                <script> alert("안녕하세요~ {}님");
                location.href="/"
                </script>
                '''.format(id)
        else:
            return "아이디 또는 패스워드를 확인 하세요."

# 로그아웃(session 제거)
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main'))

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

#로그인 사용자만 이용 가능 (학생정보)
@app.route('/getinfo')
def getinfo():
    if 'user' in session:
        ret = dbdb.select_all()
        return render_template('getinfo.html', data=ret)
    return '''
        <script> alert("로그인 후에 이용 가능합니다");
        location.href="/login"
        </script>
        '''

if __name__ == '__main__':
    app.run(debug=True)

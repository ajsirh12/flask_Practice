import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect

from models import db
from models import Fcuser

from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)

# html을 Controller에서 만들어서 View로 전달하는데 Controller와 View를 분리
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login이 된 경우
        session['userid'] = form.data.get('userid')

        return redirect('/')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

# 127.0.0.1/
@app.route('/')
def hello():
    userid = session.get('userid', None)
    print(userid)
    return render_template('hello.html', userid=userid)

# 127.0.0.1/resgister
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    # if request.method=='Post':
    #     print('post')
    #     if form.validate_on_submit():
    #         fcuser = Fcuser()
    #         fcuser.userid = form.data.get('userid')
    #         fcuser.username = form.data.get('username')
    #         fcuser.password = form.data.get('password')
    #         fcuser.repassword = form.data.get('repassword')
    #
    #         print(fcuser.username)
    #
    #         db.session.add(fcuser)
    #         db.session.commit()
    #
    #         return redirect('/')
    #     else:
    #         print('retry')
    # elif request.method == 'GET':
    #     print('get')
    # else:
    #     print('tlqk')
    if request.method=='GET':
        print('get')
    else:
        if form.validate_on_submit():
            fcuser = Fcuser()
            fcuser.userid = form.data.get('userid')
            fcuser.username = form.data.get('username')
            fcuser.password = form.data.get('password')
            fcuser.repassword = form.data.get('repassword')

            print(fcuser.username)

            db.session.add(fcuser)
            db.session.commit()

            return redirect('/')
        else:
            print('retry')

    return render_template('register.html', form=form)

if __name__ == '__main__':
    print('hello')
    basedir = os.path.abspath(os.path.dirname(__file__))
    print('basedir:{}'.format(basedir))
    dbfile = os.path.join(basedir, 'db.sqlite')
    print('file:{}'.format(dbfile))

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY']='qwerasd'  # 임의의 문자열

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)


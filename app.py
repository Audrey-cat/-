from flask import redirect, Flask, render_template, request, flash, session
from datetime import timedelta
import pymysql
import config
from exts import db
app = Flask(__name__)
# app.secret_key="123"
app.config.from_object(config)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
db.init_app(app)


@app.route('/')
def indeddx():
    return redirect('/login')
    return 'index'



@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/doLogin',methods=['GET','POST'])
def doLogin():
    name = request.form.get("uname")
    pwd = request.form.get("upwd")
    # conn = pymysql.connect(
    #     host="127.0.0.1",
    #     port=3306,
    #     db="pcmp1",
    #     user="root",
    #     password="root",
    #     charset="utf8"
    # )
    if name=="pea" and pwd=="111":
        session['name']=name
        return "登陆成功"
        # return render_template("main.html")
    else:
        flash("密码不正确")
        return render_template("login.html")

@app.route('/main')
def main1():
    return render_template("main.html")
#
# @app.route('/jinja')
# def jinja():
#     uname = "pea"
#     list = [111,222,333]
#     return render_template("jinja.html", name=uname, l1=list)



if __name__ == '__main__':
    app.run()

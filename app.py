from flask import redirect, Flask, render_template, request, flash, session,url_for
from datetime import timedelta
import pymysql
# JSON文件
import json

# import其他py文件
import config
from exts import db

app = Flask(__name__)
# app.secret_key="123"
app.config.from_object(config)# 就完成了项目的数据库的配置
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
db.init_app(app)
var=[]

# 网页每个页面和跳转的路由
@app.route('/')
def hello_world():
    return render_template('base.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        #pass
        session.permanent= True
        return redirect(url_for('hello_world'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        pass
        return redirect(url_for('login'))

@app.route('/schoolQuery', methods=['GET', 'POST'])
def schoolQuery():
    if request.method == 'GET':
        return render_template('schoolQuery.html')
    else:
        pass

@app.route('/catQuery', methods=['GET', 'POST'])
def catQuery():
    if request.method == 'GET':
        return render_template('catQuery.html')
    else:
        pass

# 干嘛用的 我再看看
@app.context_processor
def my_context_processor():
    user=0
    if session.permanent == True:
        user = 1
    print(user)
    if user == 1:
        return{"user":user }
    return {}

# @app.route('/doLogin',methods=['GET','POST'])
# def doLogin():
#     name = request.form.get("uname")
#     pwd = request.form.get("upwd")
#     # conn = pymysql.connect(
#     #     host="127.0.0.1",
#     #     port=3306,
#     #     db="pcmp1",
#     #     user="root",
#     #     password="root",
#     #     charset="utf8"
#     # )
#     if name=="pea" and pwd=="111":
#         session['name']=name
#         return "登陆成功"
#         # return render_template("main.html")
#     else:
#         flash("密码不正确")
#         return render_template("login.html")


#
# @app.route('/jinja')
# def jinja():
#     uname = "pea"
#     list = [111,222,333]
#     return render_template("jinja.html", name=uname, l1=list)






if __name__ == '__main__':
    app.run()

from flask import redirect, Flask, render_template, request, flash, session,url_for
from datetime import timedelta
import pymysql
import config
from exts import db
app = Flask(__name__)
# app.secret_key="123"
app.config.from_object(config)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
db.init_app(app)
var=[]

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
        allcourses = [
            {'name': '面向对象编程'},
            {'name': '数据库原理'},
            {'name': '软件构造基础'},
            {'name': '计算机科学与技术'},
            {'name': '微观经济学'},
            {'name': '宏观经济学'},
            {'name': '计量经济学'},
            {'name': '人格心理学'},
            {'name': '认知心理学'},
            {'name': '普通心理学'},
        ]
        return render_template('schoolQuery.html',allcourses=allcourses)
    else:
        pass

@app.route('/catQuery', methods=['GET', 'POST'])
def catQuery():
    if request.method == 'GET':
        courses = [
            {'name': '面向对象编程', 'school': '太原理工大学'},
            {'name': '数据库原理', 'school': '东南大学'},
            {'name': '软件构造基础', 'school': '武汉大学'},
            {'name': '计算机科学与技术', 'school': '东北大学'},
            {'name': '微观经济学', 'school': '兰州大学'},
            {'name': '宏观经济学', 'school': '武汉大学'},
            {'name': '计量经济学', 'school': '北京邮电大学'},
            {'name': '人格心理学', 'school': '浙江大学'},
            {'name': '认知心理学', 'school': '华北电力大学'},
            {'name': '普通心理学', 'school': '浙江大学'},
        ]
        return render_template('catQuery.html',courses=courses)
    else:
        pass
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

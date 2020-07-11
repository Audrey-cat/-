from flask import redirect, Flask, render_template, request, flash, session,url_for
from datetime import timedelta
import pymysql
# JSON文件
import json

# import其他py文件
import config
from exts import db

from models import User, Course, Majors

app = Flask(__name__)
# app.secret_key="123"
app.config.from_object(config)# 就完成了项目的数据库的配置
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
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,
                                 User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('home'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，如果被注册了，就不能再注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'手机号码已被注册，请更换！'
        else:

            # 两次密码不相等
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写！'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()

                # 注册成功，跳转到登录界面

                return redirect(url_for('login'))


#获取数据库中课程的信息
@app.route('/schoolQuery', methods=['GET', 'POST'])
def schoolQuery():
    if request.method == 'GET':
        allcourses=[]
        course1 = Course.query.all()
        for i in course1:
            allcourses.append({'name':i.Cname})
        return render_template('schoolQuery.html',allcourses=allcourses)
    else:
        pass

#获取数据库中学校和专业的信息
@app.route('/catQuery', methods=['GET', 'POST'])
def catQuery():
    if request.method == 'GET':
        courses = []
        course2 = Majors.query.all()
        for i in course2:
            courses.append({'name': i.Mname,'school':i.Sname})
        return render_template('catQuery.html',courses=courses)
    else:
        pass


@app.context_processor
def my_context_processor():
    user=0
    if session.permanent == True:
        user = 1
    #print(user)
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

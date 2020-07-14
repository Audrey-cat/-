'''
author: 徐婉青，高煜嘉，黄祉琪，文天尧
create: 2020-07-09
update: 2020-07-14
'''

from flask import redirect, Flask, render_template, request, flash, session,url_for
from datetime import timedelta
# import其他py文件
import config
import re
from exts import db

from crawler import crawler
from models import User, Course, Majors, Category, Attend

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random


app = Flask(__name__)
app.config.from_object(config)# 完成了项目的数据库的配置
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1) # 默认缓存控制的最大期限
db.init_app(app)
var=[]


@app.route('/') # http://127.0.0.1:5000/ 打开网站时页面
def hello_world():
    #crawler.main()
    return render_template('base.html')

@app.route('/home') # http://127.0.0.1:5000/home 首页
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST']) # http://127.0.0.1:5000/login 登陆
def login():
    if request.method == 'GET':
        return render_template('login.html') # 引入login.html
    else:
        telephone = request.form.get('telephone') # 获取登录输入信息
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,
                                 User.password == password).first()
        user2 = User.query.filter(User.email == telephone,
                                  User.password == password).first()
        if user:
            session['user_id'] = user.id # 以手机号登录
            # 如果想在31天内都不需要登录
            return redirect(url_for('home'))
        elif user2:
            session['user_id'] = user2.id # 以邮箱登录
            # 如果想在31天内都不需要登录
            return redirect(url_for('home'))
        else:
            flash('电话号码/邮箱或者密码错误，请确认后再登录！')   # 登录信息错误则提示错误信息
            return render_template('login.html')


@app.route('/logout',methods=['GET','POST']) # http://127.0.0.1:5000/login 退出登录
def logout():
    session.pop('user_id')
    return redirect(url_for('login')) # 点”退出登录“则返回到登陆页面

#发送邮件
def mail(my_sender,my_user,my_pass,verifyCode):
    ret = True
    try:
        text = "验证码为:" + str(verifyCode)
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = formataddr(["From nicead.top", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "验证码"  # 邮件的主题，也可以说是标题


        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

verifyCode = str(random.randint(100000,999999))#生成随机验证码
@app.route('/vertifyEmail', methods=['GET', 'POST'])  # http://127.0.0.1:5000/vertifyEmail 验证邮箱
def vertifyEmail():
    if request.method == 'GET':
        return render_template('vertifyEmail.html')  # 点”找回密码“则返回到发送邮箱验证码页面
    else:
        email = request.form.get('email') #获取输入的邮箱
        my_sender = '919849055@qq.com'  # 发件人邮箱账号
        my_pass = 'ibufdqkojmgsbcig'  # 发件人邮箱密码
        my_user = str(email)  # 收件人邮箱账号
        #查看邮箱是否存在
        user = User.query.filter(User.email == email).first()
        if user:
            #发送邮箱
            ret = mail(my_sender,my_user,my_pass,verifyCode)
            if ret:
                print("邮件发送成功")#邮件发送成功，跳转到修改密码界面
                return redirect(url_for('retrievePwd',userEmail=email))
            else:
                print("邮件发送失败") #邮件发送失败可以选择重新发送
                return render_template('vertifyEmail.html')
        else:
            flash('邮箱不存在') #若用户没有使用注册时的邮箱，或者邮箱填写错误 那么邮箱有可能不存在，需要重新填写
            return render_template('vertifyEmail.html')
#用户修改密码
@app.route('/retrievePwd?userEmail=<userEmail>',methods=['GET','POST']) # http://127.0.0.1:5000/retrievePwd 找回密码
def retrievePwd(userEmail):
    if request.method == 'GET':
        return render_template('retrievePwd.html') # 点”发送验证码验证“则返回到找回密码页面
    else:
        vertifynum = request.form.get('vertifynum')  # 检测验证码
        password = request.form.get('password')  #新的密码
        password2 = request.form.get('password2')  #重新输入密码
        #若验证码与之前发送的一致
        if vertifynum == verifyCode:
            print('验证成功')
            #查看该用户的密码
            user = User.query.filter(User.email == userEmail).first()
            if password != password2:
                return u'两次密码不相等，请核对后再填写！'
            else:
                #修改密码
                user.password = password
                db.session.commit()
                return redirect(url_for('login'))
        else:
            print('验证失败')
            return render_template('retrievePwd.html')




@app.route('/register',methods=['GET','POST']) # http://127.0.0.1:5000/register 注册
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone') # 从输入框内获取注册数据
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        #手机号码验证，如果被注册了，就不能再注册
        user = User.query.filter(User.telephone == telephone).first()
        user2 = User.query.filter(User.email == email).first()
        if user and user2:
            return u'手机号码或邮箱已被注册，请更换！'
        else:

            # 两次密码不相等
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写！'
            else:
                user = User(telephone=telephone,username=username,password=password1,email=email)
                db.session.add(user)
                db.session.commit()

                # 注册成功，跳转到登录界面

                return redirect(url_for('login'))

@app.route('/userCenter',methods=['GET','POST']) # http://127.0.0.1:5000/userCenter 个人中心
def userCenter():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    name = user.username
    telephone = user.telephone
    email = user.email
    return render_template('userCenter.html',name=name,telephone=telephone,email=email)


#选择“学校专业查询”显示课程列表：全部课程+学校名称+专业名称+课程详情
@app.route('/schoolQuery', methods=['GET', 'POST'])
def schoolQuery():
    if request.method == 'GET':
        allcourses=[] # 存放课程名、学校名、专业名和课程详情
        majors = Majors.query.all()
        for i in majors:
            course = Course.query.filter(i.MID == Course.MID).all()
            for j in course:
                allcourses.append({'cid':j.CID, 'name':j.Cname,'school':i.Sname,'major':i.Mname,'info':j.Cinfo})

        # 尝试使用下拉选择框
        # schools = []
        # school_major = []
        # major = Majors.query.all()
        # for i in major:
        #     school_major.append({'school':i.Sname,'major':i.Mname})
        #
        # for i in major:
        #     if {'school':i.Sname} in schools:
        #         pass
        #     else:
        #         schools.append({'school':i.Sname})
        #
        # schoolid = request.form.get('schoolid')
        # print(schoolid)

        # 先引入schoolQuery.html，同时根据后面传入的参数，对html进行修改渲染。

        return render_template('schoolQuery.html', allcourses=allcourses)
    else:
        pass
        # acname = request.form.get('cname')
        # print(acname)
        # acourse = Course.query.filter(Course.Cname == acname)
        # cid = acourse.CID
        # user_id = session.get('user_id')
        # if user_id:
        #     attend = Attend(id=user_id, CID=cid)
        #     db.session.add(attend)
        #     db.session.commit()
        # else:
        #     pass
        # return redirect(url_for('schoolQuery'))


@app.route('/attend/<acid>', methods=['GET', 'POST'])
def attend(acid):

    if request.method == 'GET':
        return redirect(url_for('schoolQuery'))
    else:
        # cid = filter(str.isdigit(),acid)
        print(acid)
        length=len(acid)-1
        cid = int(acid[0:length])
        print(cid)
        user_id = session.get('user_id')
        if user_id:
            attend = Attend(id=user_id, CID=int(cid))
            db.session.add(attend)
            db.session.commit()
        else:
            pass
        return redirect(request.referrer or url_for(home))



#选择“专业大类查询”显示课程列表：专业大类+全部课程+开课大学+课程详情
@app.route('/catQuery', methods=['GET', 'POST'])
def catQuery():
    if request.method == 'GET':
        # categories = [] #下拉框选项
        # categorys = Category.query.all()
        # for i in categorys:
        #     if {'name':i.Tname} in categories:
        #         pass
        #     else:
        #         categories.append({'name':i.Tname})

        # allcourses = [] #课程（课程名+开课大学）
        # majors = Majors.query.all()
        # for i in majors:
        #     course = Course.query.filter(Course.MID == i.MID).all()
        #     for j in course:
        #         allcourses.append({'name':j.Cname,'school':i.Sname})

        allcourses = []  # 课程（专业大类+课程名+开课大学+课程详情）
        category = Category.query.all()
        for i in category:
            course = Course.query.filter(i.CID == Course.CID).all()
            for j in course:
                majors = Majors.query.filter(j.MID == Majors.MID).all()
                for m in majors:
                    allcourses.append({'cid':j.CID, 'category':i.Tname,'name':j.Cname,'school':m.Sname,'info':j.Cinfo})

        return render_template('catQuery.html', allcourses=allcourses)
    else:
        pass

#课程名字查找显示查询结果
@app.route('/courseQueryResult')
def courseQueryResult():
    q = request.args.get('q')
    course = Course.query.filter(Course.Cname.like('%'+q+'%')).all()

    allcourses = []#课程（课程名+开课大学+课程详情）
    #print(len(course))
    if len(course) != 0:
        for i in course:
            major = Majors.query.filter(Majors.MID == i.MID).first()
            allcourses.append({'cid':i.CID, 'name':i.Cname,'school':major.Sname,'info':i.Cinfo})
    else:
        pass
    return render_template('courseQuery.html',allcourses=allcourses)

#学校专业查找显示查询结果
@app.route('/schoolQueryResult')
def schoolQueryResult():
    # s = request.args.get('s')
    # m = request.args.get('m')
    # majors = Majors.query.filter(Majors.Sname == s, Majors.Mname == m).all()
    # mid = []
    # for i in majors:
    #     mid.append({'mid': i.MID})
    #
    # allcourses = []
    # if len(mid) != 0:
    #     course = Course.query.all()
    #     for i in course:
    #         if {'mid': i.MID} in mid:
    #             allcourses.append({'name': i.Cname, 'school': s, 'major': m})
    #
    # else:
    #     pass
    # return render_template('schoolQuery.html', allcourses=allcourses)
    s = request.args.get('s')
    m = request.args.get('m')
    majors = Majors.query.filter(Majors.Sname.like('%'+s+'%'),Majors.Mname.like('%'+m+'%')).all()

    # s_m = []
    # for i in majors:
    #     s_m.append({'mid':i.MID,'school':i.Sname,'major':i.Mname})

    allcourses = [] # 存放课程名、学校名、专业名和课程详情
    # if len(s_m) != 0:
    if len(majors) != 0:
        course = Course.query.all()
        for i in course:
            # for j in s_m:
            #     if i.MID == j['mid']:
            #         allcourses.append({'name': i.Cname, 'school': j['school'], 'major': j['major']})
            for j in majors:
                if i.MID == j.MID:
                    allcourses.append({'cid':i.CID, 'name':i.Cname,'school':j.Sname,'major':j.Mname,'info':i.Cinfo})
    else:
        pass
    return render_template('schoolQuery.html', allcourses=allcourses)

#专业大类查找显示查询结果
@app.route('/catQueryResult')
def catQueryResult():
    q = request.args.get('q')
    category = Category.query.filter(Category.Tname.like('%'+q+'%')).all()

    allcourses = []  # 课程（专业大类+课程名+开课大学）
    for i in category:
        course = Course.query.filter(i.CID == Course.CID).all()
        for j in course:
            majors = Majors.query.filter(j.MID == Majors.MID).all()
            for m in majors:
                allcourses.append({'cid':j.CID, 'category': i.Tname, 'name': j.Cname, 'school': m.Sname,'info':j.Cinfo})

    return render_template('catQuery.html', allcourses=allcourses)
    # allcourses = []
    # for i in category:
    #     course = Course.query.filter(i.CID == Course.CID).all()

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
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
    # main()
    app.run()
    # main()



'''
author: 徐婉青，高煜嘉，黄祉琪，文天尧
create: 2020-07-09
update: 2020-07-23
'''

import smtplib
from io import BytesIO

from flask import redirect, Flask, render_template, request, flash, session, url_for, make_response
from datetime import timedelta
# import其他py文件
import config
from captcha import validate_picture
from exts import db
import re
import difflib
from models import User, Course, Majors, Category, Attend, newCourse, Comments
from crawler import sjtu_life, NK_Economy, crawler, fudan_life, sjtu_cl
from crawler import seu_math, xmu_cpst, uibe_law, seu_building, zs_cs, uibe_it
from email.mime.text import MIMEText
from email.utils import formataddr
import random
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter
# from apscheduler.schedulers.background import BackgroundScheduler
import jieba  # 结巴分词
import numpy as np  # numpy数据处理库
import matplotlib.pyplot as plt  # 图像展示库
from wordcloud import WordCloud, STOPWORDS  # 词云展示库
from os import path

from PIL import Image  # 图像处理库

from sqlalchemy import func

import course_analyze

app = Flask(__name__)
app.config.from_object(config)  # 完成了项目的数据库的配置
db.init_app(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)  # 默认缓存控制的最大期限

var = []


@app.route('/')  # http://127.0.0.1:5000/ 打开网站时页面
def hello_world():
    # rows = db.session.query(func.count(Category.CID)).scalar()  # 查询表的总行数
    # print(rows)

    # 使用爬虫
    # def docrawler():
    #     sjtu_life.main()
    #     crawler.main()
    #     NK_Economy.main()
    #     fudan_life.main()
    #     sjtu_cl.main()
    #     seu_math.main()
    #     xmu_cpst.main()
    #     uibe_law.main()
    #     seu_building.main()
    #     zs_cs.main()
    #     uibe_it.main()
    #     print('爬虫数据更新')

    # 定时器更新爬虫
    # sched = BackgroundScheduler()
    # sched.add_job(docrawler, 'cron', hour='12', minute='14', second='00')
    # sched.start()

    # 取出数据库数据，存入txt
    # course = Course.query.with_entities(Course.Cname).all()
    #
    # f = open('templates/words.txt','w',encoding='utf-8')
    # for i in course:
    #     f.write(i[0])

    # 进行词频分析
    # f = open('templates/words.txt','r',encoding='utf-8')
    # txt = f.read()
    # words = jieba.lcut(txt) # 使用精确模式对文本进行分词
    # counts = {} # 使用键值对的的形式存储词语及其出现的次数
    #
    # for word in words:
    #     if len(word) == 1: # 单个词语不计算在内
    #         continue
    #     else:
    #         counts[word] = counts.get(word,0) + 1 # 遍历所有词语，每出现一次其对应的值加1
    #
    # items = list(counts.items())
    # items.sort(key=lambda x: x[1], reverse=True) # 根据词语出现的次数进行从大到小排序
    # print(len(items))
    #
    # f.close()
    #
    # f = open('templates/wordsana.txt', 'w', encoding='utf-8')
    # number = len(items)
    # for i in range(number):
    #     word, count = items[i]
    #     count = str(count)
    #     f.write(word+' '+count+'\n')
    #
    #     # print("{0:<5}{1:>5}".format(word,count))

    # 按照网上代码做词云
    # d = path.dirname(__file__)#当前文件路径
    #
    # # file = open(path.join(d,'static\\templates\words.txt')).read()
    # file = open('templates/words.txt', 'r', encoding='utf-8').read()
    #
    # # 进行分词
    # default_mode = jieba.cut(file)
    # text = " ".join(default_mode)
    # # alice_mark = np.array(Image.open(path.join(d,"static\\images\courseUpdate.png")))
    # alice_mark = np.array(Image.open('static/images/coursePredict.jpg.jpg'))
    # stopwords = set(STOPWORDS)
    # stopwords.add("said")
    # wc = WordCloud(
    # #     设置字体，不指定就会出现乱码
    #     font_path=r'D:\DownloadFromInternet\DownloadedByMe\dd\msyh.ttf',
    #     background_color = "white",
    #     max_words=50,
    #     mask=alice_mark,
    #     stopwords=stopwords
    # )
    # # 生成词云
    # wc.generate(text)
    #
    # #存到文件里
    # wc.to_file(path.join(d,"result1.jpg"))
    #
    # #展示
    # plt.imshow(wc, interpolation="bilinear")
    # plt.axis("off")
    # plt.figure()
    # plt.imshow(alice_mark,cmap=plt.cm.gray,interpolation='bilinear')
    # plt.axis("off")
    # plt.show()

    # 查询数据库记录条数！！！
    # attended = db.session.query(func.count(Attend.id)).filter(Attend.id == user_id,Attend.CID == int(cid)).scalar()
    return render_template('base.html')


# 点击首页，进入首页页面
@app.route('/home')  # http://127.0.0.1:5000/home 首页
def home():
    courses = []
    courses5 = Course.query.order_by(Course.Attend.desc())[0:5]
    for course5 in courses5:
        comment = Comments.query.filter(Comments.CID == course5.CID).all()
        comments = len(comment)
        major = Majors.query.filter(Majors.MID == course5.MID).first()
        courses.append({'cid': course5.CID, 'name': course5.Cname,
                        'school': major.Sname, 'major': major.Mname, 'info': course5.Cinfo, 'attend': course5.Attend,'comments':comments})

    return render_template('home.html', courses=courses)


@app.route('/course')  # http://127.0.0.1:5000/course 课程页
def course():
    return render_template('course.html')


# 爬虫函数
# def docrawler():
#     uibe_law.main()
#     seu_building.main()

# 课程更新
@app.route('/course/courseUpdate')  # http://127.0.0.1:5000/course/courseUpdate 更新课程页
def courseUpdate():
    # 执行爬虫函数，获取更新的课程
    # docrawler()

    allcourses = []  # 存放课程名、学校名、专业名和课程详情
    newcourse = newCourse.query.all()
    # 获取更新的课程
    for i in newcourse:
        course = Course.query.filter(i.CID == Course.CID).first()
        comment = Comments.query.filter(Comments.CID == i.CID).all()
        comments = len(comment)
        majors = Majors.query.filter(course.MID == Majors.MID).all()
        for j in majors:
            allcourses.append(
                {'cid': course.CID, 'name': course.Cname, 'school': j.Sname, 'major': j.Mname, 'info': course.Cinfo,'comments':comments})

    user_id = session.get('user_id')
    id = 0
    if user_id:
        id = user_id
    total = len(allcourses)
    PER_PAGE = 10  # 每页列表行数
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
    start = (page - 1) * PER_PAGE  # 每一页开始位置
    end = start + PER_PAGE  # 每一页结束位置
    pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3
    courses = allcourses[start:end]  # 进行切片处理

    context = {
        'pagination': pagination,
        'courses': courses,
        'id': id
    }

    return render_template('courseUpdate.html', user_id=user_id, **context)


# 点击首页轮播图图3，进入大学介绍页面
@app.route('/universityInfo')  # http://127.0.0.1:5000/universityInfo 大学介绍页面
def getUniversityInfo():
    return render_template('universities.html')

# 课程预测
@app.route('/course/coursePredict')  # http://127.0.0.1:5000/course/coursePredict 课程预测页
def coursePredict():
    return render_template('coursePredict.html')

# 课程推荐
@app.route('/course/courseRecommend')  # http://127.0.0.1:5000/course/courseUpdate 课程推荐页
def courseRecommend():
    user_id = session.get('user_id')
    if user_id:
        attend = Attend.query.filter(Attend.id == user_id).first()
        if attend:
            courses = course_analyze.calculate(user_id)
            return render_template('courseRecommend.html', courses=courses, user_id=user_id)
        else:
            flash("没有参与课程无法推荐课程哦")
            return render_template('course.html')
    else:
        flash("未登录无法推荐课程哦")
        return render_template('course.html')



rCode = str(random.randint(100000, 999999))
def domail(my_sender, my_user, my_pass,rCode):
    ret = True
    try:
        text="您已经成功的注册了皮卡丘课程管理平台，并绑定了本邮箱，验证码为："+ str(rCode)+ "。请您返回页面来验证，若非本人操作，请忽略此信息。"
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


# 注册
@app.route('/register', methods=['GET', 'POST'])  # http://127.0.0.1:5000/register 注册
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')  # 从输入框内获取注册数据
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        # 手机号码验证，如果被注册了，就不能再注册
        my_sender = '919849055@qq.com'  # 发件人邮箱账号
        my_pass = 'ibufdqkojmgsbcig'  # 发件人邮箱密码
        my_user = str(email)  # 收件人邮箱账号

        user = User.query.filter(User.telephone == telephone).first()
        user2 = User.query.filter(User.email == email).first()
        if  user or user2:
            flash("手机号码或邮箱已被注册，请更换!")
            return redirect(url_for('register'))
        else:
            # 密码不符合
            # 两次密码不相等
            if password1 != password2:
                flash("两次密码不相等，请核对后再填写!")
                return redirect(url_for('register'))
            else:
                ret = domail(my_sender, my_user, my_pass,rCode)
                if ret:
                    print("邮件发送成功")  # 邮件发送成功，跳转到修改密码界面
                    return redirect(url_for('registerCode',telephone=telephone, username=username, password=password1, email=email))

                else:
                    print("邮件发送失败")  # 邮件发送失败可以选择重新发送
                    flash("邮件发送失败")
                    return redirect(url_for('register'))

                    #return render_template('register.html')


# 注册成功，跳转到登录界面
@app.route('/registerCode?email=<email>?telephone=<telephone>?username=<username>?password=<password>', methods=['GET', 'POST'])  # http://127.0.0.1:5000/retrievePwd 找回密码
def registerCode(telephone,username,password,email):
    if request.method == 'GET':
        return render_template('registerCode.html')  # 点”发送验证码验证“则返回到找回密码页面
    else:
        vertifynum = request.form.get('vertifynum')  # 检测验证码
        # 若验证码与之前发送的一致
        if vertifynum == rCode:
            print('验证成功')
            user = User(telephone=telephone, username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            # 查看该用户的密码
            return redirect(url_for('login'))
        else:
            print('验证失败')
            flash("验证码错误，请核准填写")
            return render_template('registerCode.html')

# 生成验证码图片
@app.route('/pic')
def get_pic():
    # 造图片
    im, s = validate_picture(4)  # im表示验证码图片，s表示验证码的字符串
    # 把图片转成二进制形式存入内存，防止将图片放在文件中占用大量磁盘
    buffer = BytesIO()
    im.save(buffer, 'jpeg')
    buf_bytes = buffer.getvalue()
    # 构建response
    response = make_response(buf_bytes)
    response.headers['Content-Type'] = 'image/jpg'
    # 保存s
    session['pic_code'] = s
    return response

# 登录
@app.route('/login', methods=['GET', 'POST'])  # http://127.0.0.1:5000/login 登陆
def login():
    if request.method == 'GET':
        return render_template('login.html')  # 引入login.html
    else:
        telephone = request.form.get('telephone')  # 获取登录输入信息
        password = request.form.get('password')
        captcha = request.form.get('captcha') # 获取输入的验证码
        # 从session中取值
        code = session.get('pic_code')
        if code.lower() != captcha.lower():
            flash('验证码错误！')
            return render_template('login.html')

        user = User.query.filter(User.telephone == telephone,
                                 User.password == password).first()
        user2 = User.query.filter(User.email == telephone,
                                  User.password == password).first()
        if user:
            session['user_id'] = user.id  # 以手机号登录
            # 如果想在31天内都不需要登录
            return redirect(url_for('home'))
        elif user2:
            session['user_id'] = user2.id  # 以邮箱登录
            # 如果想在31天内都不需要登录
            return redirect(url_for('home'))
        else:
            flash('电话号码/邮箱或者密码错误，请确认后再登录！')  # 登录信息错误则提示错误信息
            return render_template('login.html')


# 找回密码——发送邮件
def mail(my_sender, my_user, my_pass, verifyCode):
    ret = True
    try:
        text = "验证码为:" + str(verifyCode)+"。您正在找回密码，请勿将验证码告知他人，若非本人操作请忽略此信息。"
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


# 找回密码——验证邮箱
verifyCode = str(random.randint(100000, 999999))  # 生成随机验证码


@app.route('/vertifyEmail', methods=['GET', 'POST'])  # http://127.0.0.1:5000/vertifyEmail 验证邮箱
def vertifyEmail():
    if request.method == 'GET':
        return render_template('vertifyEmail.html')  # 点”找回密码“则返回到发送邮箱验证码页面
    else:
        email = request.form.get('email')  # 获取输入的邮箱
        my_sender = '919849055@qq.com'  # 发件人邮箱账号
        my_pass = 'ibufdqkojmgsbcig'  # 发件人邮箱密码
        my_user = str(email)  # 收件人邮箱账号
        # 查看邮箱是否存在
        user = User.query.filter(User.email == email).first()
        if user:
            # 发送邮箱
            ret = mail(my_sender, my_user, my_pass, verifyCode)
            if ret:
                print("邮件发送成功")  # 邮件发送成功，跳转到修改密码界面
                return redirect(url_for('retrievePwd', userEmail=email))
            else:
                print("邮件发送失败")  # 邮件发送失败可以选择重新发送
                return render_template('vertifyEmail.html')
        else:
            flash('邮箱不存在')  # 若用户没有使用注册时的邮箱，或者邮箱填写错误 那么邮箱有可能不存在，需要重新填写
            return render_template('vertifyEmail.html')


# 找回密码
@app.route('/retrievePwd?userEmail=<userEmail>', methods=['GET', 'POST'])  # http://127.0.0.1:5000/retrievePwd 找回密码
def retrievePwd(userEmail):
    if request.method == 'GET':
        return render_template('retrievePwd.html')  # 点”发送验证码验证“则返回到找回密码页面
    else:
        vertifynum = request.form.get('vertifynum')  # 检测验证码
        password = request.form.get('password')  # 新的密码
        password2 = request.form.get('password2')  # 重新输入密码
        # 若验证码与之前发送的一致
        if vertifynum == verifyCode:
            print('验证成功')
            # 查看该用户的密码
            user = User.query.filter(User.email == userEmail).first()
            if password != password2:
                return u'两次密码不相等，请核对后再填写！'
            else:
                # 修改密码
                user.password = password
                db.session.commit()
                return redirect(url_for('login'))
        else:
            print('验证失败')
            return render_template('retrievePwd.html')


# 退出登录
@app.route('/logout', methods=['GET', 'POST'])  # http://127.0.0.1:5000/logout 退出登录
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))  # 点”退出登录“则返回到登陆页面


# 进入个人中心
@app.route('/userCenter', methods=['GET', 'POST'])  # http://127.0.0.1:5000/userCenter 个人中心
def userCenter():
    # if request.method == 'GET':
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    name = user.username
    telephone = user.telephone
    email = user.email
    attendcourses = []  # 存放参与的课程
    acourses = Attend.query.filter(Attend.id == user_id).all()
    for acourse in acourses:
        course = Course.query.filter(Course.CID == acourse.CID).first()
        comment = Comments.query.filter(Comments.CID == acourse.CID).all()
        comments = len(comment)
        majors = Majors.query.filter(Majors.MID == course.MID).first()
        attendcourses.append(
            {'cid': course.CID, 'name': course.Cname, 'school': majors.Sname, 'majors': majors.Mname,
             'info': course.Cinfo,'comments':comments})
    # return render_template('userCenter.html', name=name, telephone=telephone, email=email, allcourses=attendcourses)

    total = len(attendcourses)

    PER_PAGE = 10  # 每页列表行数
    # total = allcourses.count() # 总行数
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
    start = (page - 1) * PER_PAGE  # 每一页开始位置
    end = start + PER_PAGE  # 每一页结束位置
    pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3
    courses = attendcourses[start:end]  # 进行切片处理

    context = {
        'pagination': pagination,
        'courses': courses
    }

    return render_template('userCenter.html', name=name, telephone=telephone, email=email, **context)


# 修改密码
@app.route('/changePwd', methods=['GET', 'POST'])  # http://127.0.0.1:5000/changePwd 修改密码
def changePwd():
    if request.method == 'GET':
        return render_template('changePwd.html')  # 点”修改密码“则进入修改密码页面
    else:
        password = request.form.get('password')  # 新的密码
        password2 = request.form.get('password2')  # 重新输入密码
        if password != password2:
            return u'两次密码不相等，请核对后再填写'
        else:
            # 修改密码
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            user.password = password
            db.session.commit()
            return redirect(url_for('userCenter'))


# 修改用户名
@app.route('/changeName', methods=['GET', 'POST'])  # http://127.0.0.1:5000/changeName 修改用户名
def changeName():
    if request.method == 'GET':
        return render_template('changeName.html')
    else:
        name = request.form.get('username')  # 新的用户名
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        user.username = name
        db.session.commit()
        return redirect(url_for('userCenter'))


# 修改手机号
@app.route('/changePhone', methods=['GET', 'POST'])  # http://127.0.0.1:5000/changePhone 修改手机号
def changePhone():
    if request.method == 'GET':
        return render_template('changePhone.html')
    else:
        telephone = request.form.get('telephone')  # 新的手机号
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            flash("该手机号已经被注册")
            return redirect(url_for('changePhone'))
        else:
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            user.telephone = telephone
            db.session.commit()
            return redirect(url_for('userCenter'))


# 参与课程
@app.route('/attend/<acid>', methods=['GET', 'POST'])
def attend(acid):
    if request.method == 'GET':
        return redirect(url_for('schoolQuery'))
    else:
        cid = acid
        course = Course.query.filter(Course.CID == cid).first()
        mid = course.MID
        major = Majors.query.filter(Majors.MID == mid).first()
        user_id = session.get('user_id')
        if user_id:
            attend = Attend(id=user_id, CID=int(cid))
            # attended = Attend.query.filter(Attend.id == user_id,Attend.CID == int(cid)).first()
            # attended = db.session.query(func.count(Attend.id)).filter(Attend.id == user_id,Attend.CID == int(cid)).scalar()
            try:
                major.MAttend = major.MAttend + 1
                course.Attend = course.Attend + 1
                db.session.add(attend)
                db.session.commit()
                session['attended'] = 0
            except Exception:
                print("已添加此课程")
        else:
            pass

        return redirect(request.referrer or url_for(home))

# 查找参与课程
@app.route('/attendSearch')
def attendsearch():
    q = request.args.get('q')
    print(q)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    name = user.username
    telephone = user.telephone
    email = user.email
    attends = Attend.query.filter(Attend.id == user_id).all()
    allnames = []
    allcourses = []
    allname = []
    for attend in attends:
        course = Course.query.filter(Course.CID == attend.CID).first()
        cname = course.Cname
        print(cname)
        allnames.append(cname)
    print(allnames)
    for aname in allnames:
        if q in aname:
            allname.append(aname)
            print(aname)
    for name in allname:
        course = Course.query.filter(Course.Cname == name).first()
        major = Majors.query.filter(Majors.MID == course.MID).first()
        allcourses.append(
            {'cid': course.CID, 'name': course.Cname, 'school': major.Sname, 'majors': major.Mname,
             'info': course.Cinfo})
    # return render_template('userCenter.html', name=name, telephone=telephone, email=email, allcourses=allcourses)
    # return render_template('userCenter.html', allcourses=allcourses)
    total = len(allcourses)
    PER_PAGE = 10  # 每页列表行数
    # total = allcourses.count() # 总行数
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
    start = (page - 1) * PER_PAGE  # 每一页开始位置
    end = start + PER_PAGE  # 每一页结束位置
    pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3
    courses = allcourses[start:end]  # 进行切片处理

    context = {
        'pagination': pagination,
        'courses': courses
    }

    return render_template('userCenter.html', **context)


# 取消参与课程
@app.route('/cancel_attend/<cacid>', methods=['GET', 'POST'])
def cancel_attend(cacid):
    if request.method == 'GET':
        return redirect(url_for('userCenter'))
    else:
        # print(cacid)
        # length=len(cacid)-1

        cid = cacid
        course1 = Course.query.filter(Course.CID == cid).first()
        mid = course1.MID
        major = Majors.query.filter(Majors.MID == mid).first()
        user_id = session.get('user_id')
        if user_id:
            course = Attend.query.filter(Attend.CID == cid, Attend.id == user_id).first()
            major.MAttend = major.MAttend - 1
            course1.Attend = course1.Attend - 1
            db.session.delete(course)
            db.session.commit()
        else:
            pass
        return redirect(url_for('userCenter'))


# 选择“学校专业查询”显示课程列表：全部课程+学校名称+专业名称+课程详情
@app.route('/schoolQuery', methods=['GET'])
def schoolQuery():
    # if request.method == 'GET':
    allcourses = []  # 存放课程名、学校名、专业名和课程详情
    courseNum = []  # 全部课程号

    for i in Course.query.all():
        courseNum.append(i.CID)

    total = len(courseNum)
    PER_PAGE = 10  # 每页列表行数
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
    start = (page - 1) * PER_PAGE  # 每一页开始位置
    end = start + PER_PAGE  # 每一页结束位置
    pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3

    courseRange = courseNum[start:end]  # 获取该分页所包含的课程号数组
    courses = Course.query.filter(Course.CID.in_(courseRange)).all()  # 该分页所包含的course信息

    for j in courses:
        majors = Majors.query.filter(Majors.MID == j.MID).first()
        comment = Comments.query.filter(Comments.CID == j.CID).all()
        comments = len(comment)
        allcourses.append({'cid': j.CID, 'name': j.Cname, 'school': majors.Sname, 'major': majors.Mname, 'info': j.Cinfo,'comments':comments})

    user_id = session.get('user_id')
    id = 0
    if user_id:
        id = user_id

    context = {
        'pagination': pagination,
        'courses': allcourses,
        'id': id
    }

    # 先引入schoolQuery.html，同时根据后面传入的参数，对html进行修改渲染。
    return render_template('schoolQuery.html', **context, user_id=user_id)


# 选择“专业大类查询”显示课程列表：专业大类+全部课程+开课大学+课程详情
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
        user_id = session.get('user_id')
        id = 0
        if user_id:
            id = user_id

        courses = []  # 课程（专业大类+课程名+开课大学+课程详情）
        courseNum = []  # 全部课程号
        for i in Category.query.all():
            courseNum.append(i.CID)

        total = len(courseNum)
        PER_PAGE = 10  # 每页列表行数
        page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
        start = (page - 1) * PER_PAGE  # 每一页开始位置
        end = start + PER_PAGE  # 每一页结束位置
        pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3

        courseRange = courseNum[start:end]  # 获取该分页所包含的课程号数组
        category = Category.query.filter(Category.CID.in_(courseRange)).all()  # 该分页所包含的category信息

        for j in category:
            course = Course.query.filter(j.CID == Course.CID).first()
            majors = Majors.query.filter(course.MID == Majors.MID).first()
            comment = Comments.query.filter(Comments.CID == j.CID).all()
            comments = len(comment)
            courses.append(
                {'cid': course.CID, 'category': j.Tname, 'name': course.Cname, 'school': majors.Sname,
                 'info': course.Cinfo,'comments':comments})

        context = {
            'pagination': pagination,
            'courses': courses,
            'id': id
        }

        return render_template('catQuery.html', **context, user_id=user_id)
    else:
        pass


# 课程名字查找显示查询结果
@app.route('/courseQueryResult')
def courseQueryResult():
    q = request.args.get('q')
    course = Course.query.filter(Course.Cname.like('%' + q + '%')).all()
    user_id = session.get('user_id')
    id = 0
    if user_id:
        id = user_id
    allcourses = []  # 课程（课程名+开课大学+课程详情）
    # print(len(course))
    # if len(course) != 0:
    for i in course:
        comment = Comments.query.filter(Comments.CID == i.CID).all()
        comments = len(comment)
        major = Majors.query.filter(Majors.MID == i.MID).first()
        allcourses.append({'cid': i.CID, 'name': i.Cname, 'school': major.Sname, 'info': i.Cinfo,'comments':comments})

    total = len(allcourses)
    PER_PAGE = 10  # 每页列表行数
    # total = allcourses.count() # 总行数
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
    start = (page - 1) * PER_PAGE  # 每一页开始位置
    end = start + PER_PAGE  # 每一页结束位置
    pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3
    courses = allcourses[start:end]  # 进行切片处理

    context = {
        'pagination': pagination,
        'courses': courses,
        'id': id
    }

    return render_template('courseQuery.html', **context, user_id=user_id)


# 学校专业查找显示查询结果
@app.route('/schoolQueryResult')
def schoolQueryResult():
    user_id = session.get('user_id')
    id = 0
    if user_id:
        id = user_id

    s = request.args.get('s')
    m = request.args.get('m')
    majors = Majors.query.filter(Majors.Sname.like('%' + s + '%'), Majors.Mname.like('%' + m + '%')).all()

    allcourses = []  # 存放课程名、学校名、专业名和课程详情
    courseNum = []  # 全部课程号

    for i in Course.query.all():
        for j in majors:
            if i.MID == j.MID:
                courseNum.append(i.CID)

    total = len(courseNum)
    PER_PAGE = 10  # 每页列表行数
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
    start = (page - 1) * PER_PAGE  # 每一页开始位置
    end = start + PER_PAGE  # 每一页结束位置
    pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3

    courseRange = courseNum[start:end]  # 获取该分页所包含的课程号数组
    courses = Course.query.filter(Course.CID.in_(courseRange)).all()  # 该分页所包含的course信息

    for m in courses:
        comment = Comments.query.filter(Comments.CID == m.CID).all()
        comments = len(comment)
        for n in majors:
            if m.MID == n.MID:
                allcourses.append({'cid': m.CID, 'name': m.Cname, 'school': n.Sname, 'major': n.Mname, 'info': m.Cinfo,
                                   'comments': comments})

    context = {
        'pagination': pagination,
        'courses': allcourses,
        'id': id
    }

    return render_template('schoolQuery.html', **context, user_id=user_id)


# 专业大类查找显示查询结果
@app.route('/catQueryResult')
def catQueryResult():
    q = request.args.get('q')
    category = Category.query.filter(Category.Tname.like('%' + q + '%')).all()
    user_id = session.get('user_id')
    id = 0
    if user_id:
        id = user_id
    courses = []  # 课程（专业大类+课程名+开课大学）
    courseNum = []  # 全部课程号
    for i in category:
        courseNum.append(i.CID)

    total = len(courseNum)
    PER_PAGE = 10  # 每页列表行数
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
    start = (page - 1) * PER_PAGE  # 每一页开始位置
    end = start + PER_PAGE  # 每一页结束位置
    pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3
    courseRange = courseNum[start:end]
    category = Category.query.filter(Category.CID.in_(courseRange)).all()  # 该分页所包含的category信息

    for j in category:
        course = Course.query.filter(j.CID == Course.CID).all()
        for n in course:
            comment = Comments.query.filter(Comments.CID == n.CID).all()
            comments = len(comment)
            majors = Majors.query.filter(n.MID == Majors.MID).all()
            for m in majors:
                courses.append(
                    {'cid': n.CID, 'category': j.Tname, 'name': n.Cname, 'school': m.Sname, 'info': n.Cinfo,'comments':comments})

    context = {
        'pagination': pagination,
        'courses': courses,
        'id': id
    }

    return render_template('catQuery.html', **context, user_id=user_id)


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


@app.route('/comment/<ccid>',methods=['GET','POST'])
def comment(ccid):
    if request.method == 'GET':
        # course=Course.query.filter(Course.CID==ccid).first()
        courses = Comments.query.filter(Comments.CID==ccid).all()

        commentNum = []
        for i in courses:
            commentNum.append(i.id)

        total = len(commentNum)
        PER_PAGE = 10  # 每页列表行数
        page = request.args.get(get_page_parameter(), type=int, default=1)  # 获取页码，默认为第一页
        start = (page - 1) * PER_PAGE  # 每一页开始位置
        end = start + PER_PAGE  # 每一页结束位置
        pagination = Pagination(bs_version=3, page=page, total=total)  # Bootstrap的版本，默认为3
        commentRange = commentNum[start:end]
        # category = Category.query.filter(Category.CID.in_(commentRange)).all()  # 该分页所包含的category信息
        comments = Comments.query.filter(Comments.id.in_(commentRange)).all()

        course = Course.query.filter(Course.CID == ccid).first()
        cname = course.Cname
        allcomments = []
        # comments = Comments.query.filter(Comments.CID == ccid).all()
        for comment in comments:
            user = User.query.filter(User.id == comment.user_id).first()
            allcomments.append({'user_name': user.username, 'content': comment.content,
                                'datetime': comment.create_time})

        context = {
            'pagination': pagination,
            'allcomments': allcomments,
            'id': id
        }

        return render_template('comment.html',**context,cname=cname)
    else:
        user_id = session.get('user_id')
        if user_id:
            content = request.form.get('content')
            if len(content)==0:
                flash('评论内容不能为空！')
            else:
                comment = Comments(content=content, user_id=user_id, create_time=datetime.now(), CID=ccid)
                db.session.add(comment)
                db.session.commit()

            return redirect(url_for('comment', ccid=ccid))
        else:
            flash('请先登录再进行评论！')
            return redirect(url_for('comment', ccid=ccid))




#
# @app.route('/jinja')
# def jinja():
#     uname = "pea"
#     list = [111,222,333]
#     return render_template("jinja.html", name=uname, l1=list)


if __name__ == '__main__':
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)  # 默认缓存控制的最大期限
    #app.run(host='0.0.0.0',port=80)
    app.run()

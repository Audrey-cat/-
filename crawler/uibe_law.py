'''
author: 文天尧
create: 2020-07-15
update: 2020-07-15
'''
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
from models import Majors, Course, Category,newCourse
from exts import db


def main():
    baseurl = "http://law.uibe.edu.cn/jwjx/jpkc/index.htm"
    # 1.爬取网页
    datalist = getData(baseurl)
    # 3.保存数据
    saveData(datalist)

# 课程链接
findLink = re.compile(r'<a href="(.*)">')
# 课程名
findName = re.compile(r'">(.*)</a>')


# 爬取网页
def getData(baseurl):
    datalist = []

    html = askURL(baseurl)  # 保存获取到的网页源码

    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('ul', class_="newlist"):  # 查找符合要求的字符串，形成列表
        # data = [] # 保存所有信息
        item = str(item)
        # print('---------------------------')
        #
        # print(item)
        # print('---------------------------')

        link = re.findall(findLink, item)
        name = re.findall(findName, item)

        for i in range(0, len(link)):
            link[i] = "http://law.uibe.edu.cn/jwjx/jpkc/" + link[i]
            datalist.append({'name': name[i], 'link': link[i]})

    print(datalist)
    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向服务器发送消息
        "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    }
    # 用户代理，表示告诉服务器，我们是什么类型的机器/浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)  # 发出请求了，返回一个response对象
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

#保存数据
def saveData(datalist):
    # 检查专业是否已经在专业表中
    majors1 = Majors.query.filter(Majors.Mname == '法学', Majors.Sname == '对外经济贸易大学').first()
    if majors1:
        # 如果存在，获取专业编号
        mid = majors1.MID
    else:
        # 不存在，获取当前最大专业编号值，继续编码，专业存入表中
        mmajors = Majors.query.order_by(Majors.MID.desc()).first()
        mid = mmajors.MID + 1
        majors = Majors(SID=1007, Sname='对外经济贸易大学', MID=mid, Mname='法学')
        db.session.add(majors)
        db.session.commit()
    for data in datalist:
        # 检查该课程是否已经存在
        dataname = data['name'][0:20]
        course1 = Course.query.filter(Course.MID == mid, Course.Cname == dataname).first()
        if course1:
            pass
        else:
            # 获取课程编号最大值
            mcourse = Course.query.order_by(Course.CID.desc()).first()
            cid = mcourse.CID + 1
            # 将课程存入表中

            course = Course(MID=mid, CID=cid, Cname=data['name'], Cinfo=data['link'])
            newcourse = newCourse(CID=cid)
            db.session.add(course)
            db.session.add(newcourse)
            db.session.commit()
            category = Category(TID=1007, Tname='法学类', CID=cid)
            db.session.add(category)
            db.session.commit()


if __name__ == "__main__":
    main()

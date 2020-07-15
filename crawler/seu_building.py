'''
author: 黄祉琪
create: 2020-07-15
update: 2020-07-15
'''
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
from models import Majors,Course,Category
from exts import db


findCourse = re.compile(r'<span class="column-name">(.*?)</span>',re.S)
findLink = re.compile(r' href="(.*?)"',re.S)

def main():
    baseurl = "https://arch.seu.edu.cn/9416/list.htm"
    # 1爬取网页
    datalist = getData(baseurl)
    # 3保存数据
    saveData(datalist)



# 爬取网页
def getData(baseurl):
    datalist = []
    course = {}
    html = askURL(baseurl)  # 保存获取到的网页源码
    # 2逐一解析数据
    i = 0
    soup = BeautifulSoup(html, "html.parser")
    #    print(soup.a.attrs['href'])
    for item in soup.find_all('span', class_="column-list-wrap clearfix"):  # 查找符合要求的字符串，形成列表
        item = str(item)
        # print(item)
        courseName = re.findall(findCourse, item)
        courseLink = re.findall(findLink, item)
        print(courseLink)
        print(courseName)

    for i in range(0, len(courseLink)):
        datalist.append({'name': courseName[i], 'link': 'https://arch.seu.edu.cn' + courseLink[i]})

    print(datalist)
    return datalist

# 得到一个指定url的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向服务器发送消息（伪装用）
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    }
    # 用户代理，表示告诉服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接受什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据
def saveData(datalist):
    # 检查专业是否已经在专业表中
    majors1 = Majors.query.filter(Majors.Mname == '建筑学院', Majors.Sname == '东南大学').first()
    if majors1:
        # 如果存在，获取专业编号
        mid = majors1.MID
    else:
        # 不存在，获取当前最大专业编号值，继续编码，专业存入表中
        mmajors = Majors.query.order_by(Majors.MID.desc()).first()
        mid = mmajors.MID + 1
        majors = Majors(SID=1005, Sname='东南大学', MID=mid, Mname='建筑学院')
        db.session.add(majors)
        db.session.commit()
    for data in datalist:
        # 检查该课程是否已经存在
        course1 = Course.query.filter(Course.MID == mid, Course.Cname == data['name']).first()
        if course1:
            pass
        else:
            # 获取课程编号最大值
            mcourse = Course.query.order_by(Course.CID.desc()).first()
            cid = mcourse.CID + 1
            # 将课程存入表中
            course = Course(MID=mid, CID=cid, Cname=data['name'], Cinfo=data['link'])
            db.session.add(course)
            db.session.commit()
            category = Category(TID=1008, Tname='建筑类', CID=cid)
            db.session.add(category)
            db.session.commit()


'''
author: 徐婉青
create: 2020-07-15
update: 2020-07-15
'''

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
from models import Majors,Course,Category,newCourse
from exts import db


def main():

    baseurl = "http://life.sjtu.edu.cn/Data/List/kcjs?page="
    #1爬取网页
    datalist = getData(baseurl)
    #3保存数据
    saveData(datalist)
    print(datalist)

findCourseName = re.compile(r'.*?\d{3} (.*?).doc')

#爬取网页
def getData(baseurl):
    datalist = []
    page = 1
    while page<=15:
        html = askURL(baseurl+str(page))  # 保存获取到的网页源码
        # 2逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_='down-left fl'):  # 查找符合要求的字符串，形成列表
            # print(item) #测试：查课程item全部信息
            item = str(item)
            courseName = re.findall(findCourseName, item)[0]
            datalist.append(courseName)
        page = page+1
    return datalist

#得到一个指定url的网页内容
def askURL(url):
    head = {    #模拟浏览器头部信息，向服务器发送消息（伪装用）
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    #用户代理，表示告诉服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接受什么水平的文件内容）
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    #print(html)
    return html

#保存数据
def saveData(datalist):
    # 检查专业是否已经在专业表中
    majors1 = Majors.query.filter(Majors.Mname == '生命科学技术学院', Majors.Sname == '上海交通大学').first()
    if majors1:
        # 如果存在，获取专业编号
        mid = majors1.MID
    else:
        # 不存在，获取当前最大专业编号值，继续编码，专业存入表中
        mmajors = Majors.query.order_by(Majors.MID.desc()).first()
        mid = mmajors.MID + 1
        majors = Majors(SID=1002, Sname='上海交通大学', MID=mid, Mname='生命科学技术学院')
        db.session.add(majors)
        db.session.commit()
    for data in datalist:
        # 检查该课程是否已经存在
        course1 = Course.query.filter(Course.MID == mid , Course.Cname == data).first()
        if course1:
            pass
        else:
            # 获取课程编号最大值
            mcourse = Course.query.order_by(Course.CID.desc()).first()
            cid = mcourse.CID + 1
            # 将课程存入表中
            course = Course(MID=mid, CID=cid, Cname=data, Cinfo="http://life.sjtu.edu.cn/Data/List/kcjs")
            newcourse = newCourse(CID=cid)
            db.session.add(course)
            db.session.add(newcourse)
            db.session.commit()
            category = Category(TID=1002, Tname='生命科学类', CID=cid)
            db.session.add(category)
            db.session.commit()




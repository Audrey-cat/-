'''
author: 高煜嘉，徐婉青
create: 2020-07-11
update: 2020-07-12
'''

from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error

from flask import session

from models import Majors,Course,Category,newCourse
from exts import db
def main():
    baseurl = "https://www.tsinghua.edu.cn/hjxy/jxjw/bksjx/kcjs.htm"
    #1爬取网页
    datalist = getData(baseurl)
    #dbpath = "course.db"
    #3保存数据
    saveData(datalist)
    print("save...")

findCourse = re.compile(r'<strong>(.*?)<',re.S)
#findTeacher = re.compile(r'任课教师：(.*?)<br/>')
#findHours = re.compile(r'学&nbsp;&nbsp;&nbsp; 时：(\d*)<br/>',re.S)
#findCredits = re.compile(r'学分：(\d*)<br>',re.S)
#findDepartment = re.compile(r'开课院系：(.*?)<br/>')
#findDescription = re.compile(r'内容简介：<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(.*)<br/>',re.S)

#爬取网页
def getData(baseurl):
    datalist = []
    html = askURL(baseurl) #保存获取到的网页源码
    #2逐一解析数据
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.find_all('div',id="vsb_content"):  #查找符合要求的字符串，形成列表
        #print(item) 测试：查看课程item全部信息
        #data = [] #理应保存一个课程的所有信息，但由于这个网页的特殊性，没法实现，所以最终数组
        item = str(item)
        for i in range(0,35):
            courseName = re.findall(findCourse,item)[i]
            courseName = re.sub('\xa0',"",courseName)
            datalist.append(courseName)
            #department = re.findall(findDepartment, item)[0]
            #datalist.append(department)
            #teacher = re.findall(findTeacher, item)[i]
            #datalist.append(teacher)
            # hours = re.findall(findHours, item)[i]
            # data.append(hours)
            # courseCredits = re.findall(findCredits, item)
            # data.append(courseCredits)
            # courseDescription = re.findall(findDescription, item)
            # data.append(courseDescription)
        #datalist.append(data)

    #print(datalist)
    return datalist

#得到一个指定url的网页内容
def askURL(url):
    head = {    #模拟浏览器头部信息，向服务器发送消息（伪装用）
    "User-Agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_5) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 83.0.4103.116 Safari / 537.36"
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
    return html

#保存数据
def saveData(datalist):
    # 检查专业是否已经在专业表中
    majors1 = Majors.query.filter(Majors.Mname == '环境学院',
                                   Majors.Sname == '清华大学').first()
    if majors1:
        # 如果存在，获取专业编号
        mid = majors1.MID
    else:
        # 不存在，获取当前最大专业编号值，继续编码，专业存入表中
        mmajors = Majors.query.order_by(Majors.MID.desc()).first()
        mid = mmajors.MID + 1
        majors = Majors(SID=1001, Sname='清华大学', MID=mid, Mname='环境学院')
        db.session.add(majors)
        db.session.commit()
    for data in datalist:
        # 检查该课程是否已经存在
        course1 = Course.query.filter(Course.MID == mid and Course.Cname == data).first()
        if course1:
            pass
        else:
            # 获取课程编号最大值
            mcourse = Course.query.order_by(Course.CID.desc()).first()
            cid = mcourse.CID + 1
            # 将课程存入表中
            course = Course(MID=mid, CID=cid, Cname=data, Cinfo="https://www.tsinghua.edu.cn/hjxy/jxjw/bksjx/kcjs.htm")
            newcourse = newCourse(CID=cid)
            db.session.add(course)
            db.session.add(newcourse)
            db.session.commit()
            category = Category(TID=1001, Tname='环境类', CID=cid)
            db.session.add(category)
            db.session.commit()





if __name__ == '__main__':
    main()

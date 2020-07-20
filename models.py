'''
author: 徐婉青
create: 2020-07-09
update: 2020-07-11
'''

from exts import db
from sqlalchemy import ForeignKey
from datetime import datetime


# 用户表
class User(db.Model):
    __tablename__ = 'user1'  # __xx__表示被保护字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(50), nullable=False)


# 学校专业表
class Majors(db.Model):
    __tablename__ = 'Majors'
    SID = db.Column(db.Integer, nullable=False)  # 学校ID
    Sname = db.Column(db.String(12), nullable=False)  # 学校名称
    MID = db.Column(db.Integer, primary_key=True)  # 专业ID
    Mname = db.Column(db.String(12), nullable=False)  # 专业名称
    MAttend = db.Column(db.Integer, nullable=False,default=0)


# 课程表（按专业）
class Course(db.Model):
    __tablename__ = 'Course'
    MID = db.Column(db.Integer, ForeignKey("Majors.MID"), nullable=False)  # 专业ID
    CID = db.Column(db.Integer, primary_key=True)  # 课程ID
    Cname = db.Column(db.String(20), nullable=False)  # 课程名称
    Cinfo = db.Column(db.String(100), nullable=False)  # 课程信息
    Attend = db.Column(db.Integer, nullable=False,default=0)

#更新表单
class newCourse(db.Model):
    __tablename__ = 'newCourse'
    CID = db.Column(db.Integer, primary_key=True)  # 课程ID

# 课程表（按大类）
class Category(db.Model):
    __tablename__ = 'Category'
    TID = db.Column(db.Integer, nullable=False)  # 大类ID
    Tname = db.Column(db.String(12), nullable=False)  # 大类名称
    CID = db.Column(db.Integer, ForeignKey("Course.CID"), primary_key=True)  # 课程ID


class Attend(db.Model):
    __tablename__ = "Attend"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    CID = db.Column(db.Integer, ForeignKey("Course.CID"), primary_key=True, nullable=False)


class Comments(db.Model):
    __tablename__ = "Comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now())
    CID = db.Column(db.Integer, ForeignKey("Course.CID"), nullable=False)
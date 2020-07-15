'''
author: 徐婉青
create: 2020-07-09
update: 2020-07-12
'''

import os

DEBUG = True
SECRET_KEY = os.urandom(24)

# 配置数据库信息并连接数据库
HOSTNAME = 'rm-bp1ajr0maxj8bsn114o.mysql.rds.aliyuncs.com'
PORT = '3306'
DATABASE = 'pcmp0'
USERNAME = 'pea_xwq'
PASSWORD = 'xwq993961218'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

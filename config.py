import os

DEBUG = True
SECRET_KEY = os.urandom(24)

HOSTNAME = 'rm-bp1ajr0maxj8bsn114o.mysql.rds.aliyuncs.com'
PORT = '3306'
DATABASE = 'pcmp0'
USERNAME = 'pea_xwq'
PASSWORD = 'xwq993961218'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
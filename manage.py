'''
author: 徐婉青
create: 2020-07-09
update: 2020-07-09
'''

from flask_script import Manager  # 存放在终端写的脚本
from flask_migrate import Migrate, MigrateCommand
from app import app  # manager初始化需要app
from exts import db
from models import User,Course,Category,Comments,Majors

manager = Manager(app)  # 初始化

# 使用migrate绑定app和db
migrate = Migrate(app, db)
# 添加迁移脚本命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

# 用来写命令的文件



from exts import db

class User(db.Model):
    __tablename__='user1'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(10),nullable=False)
    password = db.Column(db.String(50),nullable=False)

# gaiyixia
#尝试push的没用注释

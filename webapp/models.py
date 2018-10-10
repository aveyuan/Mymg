#encoding:utf-8
from .exis import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

#用户信息表
class User(db.Model,UserMixin):
    __tablename__="mymg_user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    nickname = db.Column(db.String(50))
    email = db.Column(db.String(50))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

#微语
class Micros(db.Model):
    __tablename__ = "mymg_micros"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    time = db.Column(db.DateTime)
    content = db.Column(db.TEXT)

#时间进程
# class Stime(db.Model):
#     __tablename__ = "mymg_stime"
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     s_time = db.Column(db.DateTime)
#     e_time = db.Column(db.DateTime)
#     content = db.Column(db.TEXT)

#计划
# class Todo(db.Model):
#     __tablename__ = "mymg_todo"
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     content = db.Column(db.TEXT)
#     t_time = db.Column(db.DateTime) #提醒时间
#     status = db.Column(db.String(8)) #状态

#朋友
class Fmg(db.Model):
    __tablename__ = "mymg_fmg"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.String(4))
    birthday = db.Column(db.String(50))
    birth_type = db.Column(db.String(8))
    phone1 = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))
    wechat = db.Column(db.String(100))
    qq = db.Column(db.String(50))
    love = db.Column(db.String(255))
    halt = db.Column(db.String(255))
    note = db.Column(db.TEXT)
    a_time = db.Column(db.DateTime)
    u_time = db.Column(db.DateTime)
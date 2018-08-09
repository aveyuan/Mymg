#encoding:utf-8
#mysql
from os import path
SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:@localhost/mymg'
#sqlite
#SQLALCHEMY_DATABASE_URI='sqlite:///webapp/mymg.db'

SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY='HELLO WORKD'

#邮箱设置
MAIL_SERVER = '' #发信邮箱服务器
MAIL_PORT = 25 #端口
MAIL_USERNAME = '' #帐号
MAIL_PASSWORD = '' #密码

#想要开启生日提醒和任务提醒首先得配置邮箱，然后访问{站点/mail}即可发送邮件
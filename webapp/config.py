#encoding:utf-8
#mysql
import os
#开启下面这个用于连接mysql
#SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:@localhost/myuse'
#默认使用sqlite3不用安装数据库，很方便
#sqlite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR, 'mymg.db')
#数据库及加密
SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY='HELLO WORKD' #可以自定义长度

#邮箱设置
MAIL_SERVER = '' #发信邮箱服务器
MAIL_PORT = 25 #端口
MAIL_USERNAME = '' #帐号
MAIL_PASSWORD = '' #密码

#想要开启生日提醒和任务提醒首先得配置邮箱，然后访问{站点/mail}即可发送邮件
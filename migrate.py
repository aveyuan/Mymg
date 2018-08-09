#encoding:utf-8
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from webapp.exis import db
from webapp.models import User
from webapp import app

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.command
def init_user():
    user=User.query.filter(User.username=='admin').first()
    if user is not None:
        return u"用户已存在"
    else:
        user = User(username='admin',nickname=u'管理员',password='123456')
        db.session.add(user)
        db.session.commit()
        return (u'初始化创建用户成功\n用户名:admin\n密码:123456\n请及时修改密码')

@manager.shell
def shell():
    return dict(app=app,db=db,User=User)

if __name__=="__main__":
    manager.run()

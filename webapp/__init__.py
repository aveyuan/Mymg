#encoding:utf-8
from flask import Flask,url_for,redirect,request,json,jsonify,render_template,flash
from .exis import db
from .models import *
from . import config
from flask_login import LoginManager,login_required,logout_user,login_user,current_user
from .form import *
from datetime import datetime
from os import path
from werkzeug.security import generate_password_hash
from flask_mail import Mail,Message
import operator
import time
from .oton import this_month



app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
login_manager = LoginManager()
login_manager.session_protection="strong"
login_manager.login_view="login"
login_manager.init_app(app)


mails = Mail()
mails.init_app(app)




#获取邮箱信息
def get_email():
    user = User.query.first()
    if user:
        return user.email
    #如果为空也要返回的
    return None

#这只todo_ids，在发送邮件的时候进行检查，避免重复发送邮件
todo_ids = []

#待办获得
# def todo_get():
#     todo = Todo.query.filter(Todo.status == "待完成").all()
#     for todo in todo:
#         t = str(todo.t_time)
#         # 先转换为时间数组,然后转换为其他格式
#         timeStruct = time.strptime(t, "%Y-%m-%d %H:%M:%S")
#         strTime = time.strftime("%Y-%m-%d %H:%M", timeStruct) #得到最终的时间
#         #获取系统上的时间进行比对
#         systime = datetime.now().strftime("%Y-%m-%d %H:%M")
#         #如果相等而且发送列表ID没有这个ID就发送邮件
#         if systime == strTime:
#             if todo.id in todo_ids:
#                 continue
#             else:
#                 todo_ids.append(todo.id)
#                 sendmail("计划任务提醒","您的计划任务内容:<br>%s<br>已经到了提醒时间: %s<br>祝计划愉快！" % (todo.content,todo.t_time))
#                 Todo.query.filter_by(id=todo.id).update({"status":"已完成"})
#                 db.session.commit()


#邮件发送
def sendmail(title,content):
    msg = Message(title, sender=config.MAIL_USERNAME, recipients=[get_email()])
    msg.html = content
    mails.send(msg)


@login_manager.user_loader
def user_load(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@login_required
def index():
    return redirect(url_for('micros'))


#登录页面
@app.route("/login/",methods=['POST','GET'])
def login():
    #判断是否有用户登录，如果登录了就不让访问登录页面了
    try:
        if current_user.username:
            return redirect(url_for('index'))
    except:
        pass

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remeberme.data)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash(u'登陆失败！用户名或密码错误，请重试！', 'danger')
        if form.errors:
            flash(u'登陆失败，请尝试重新登陆.', 'danger')
    return render_template('login.html',form=form)


#微语
@app.route('/micros/',methods=['POST','GET'])
@login_required
def micros():
    if request.method=="POST":
        micro = Micros(time=datetime.now(),content=request.form.get('content'))
        db.session.add(micro)
        db.session.commit()
        return redirect(url_for('micros'))

    page = request.args.get('page', type=int,default=1)
    limit = request.args.get('limit', type=int,default=10)
    micro = Micros.query.order_by(Micros.id.desc()).paginate(page, limit, error_out=False)
    counts = micro.total;
    return render_template('micros.html',micro=micro,counts=counts,page=page)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#时间
# @app.route('/stime/',methods=['POST','GET'])
# @login_required
# def stime():
#     if request.method=="POST":
#         stime = Stime(s_time=request.form.get('s_time'),e_time=request.form.get('e_time'),content=request.form.get('content'))
#         db.session.add(stime)
#         db.session.commit()
#         return redirect(url_for('stime'))
#
#     page = request.args.get('page', type=int,default=1)
#     limit = request.args.get('limit', type=int,default=10)
#     stime = Stime.query.order_by(Stime.id.desc()).paginate(page, limit, error_out=False)
#     counts = stime.total;
#     return render_template('stime.html',stime=stime,counts=counts,page=page)

#待办
# @app.route('/todo/',methods=['POST','GET'])
# @login_required
# def todo():
#     if request.method=="POST":
#         todo = Todo(t_time=request.form.get('t_time'),status="待完成",content=request.form.get('content'))
#         db.session.add(todo)
#         db.session.commit()
#         return redirect(url_for('todo'))
#
#     page = request.args.get('page', type=int,default=1)
#     limit = request.args.get('limit', type=int,default=10)
#     #获取到未完成的待办并添加到渲染
#     todo = Todo.query.filter(Todo.status=="待完成").order_by(Todo.id.desc()).paginate(page, limit, error_out=False)
#     counts = todo.total;
#     ok = Todo.query.filter(Todo.status=="已完成").all()
#     ok = len(ok)
#     return render_template('todo.html',todo=todo,counts=counts,page=page,ok=ok)

#待办完成
# @app.route('/todo_done/')
# @login_required
# def todo_done():
#
#     page = request.args.get('page', type=int,default=1)
#     limit = request.args.get('limit', type=int,default=10)
#     todo = Todo.query.filter(Todo.status=="已完成").order_by(Todo.id.desc()).paginate(page, limit, error_out=False)
#     counts = todo.total;
#     return render_template('todo_done.html',todo=todo,counts=counts,page=page)
#
# @app.route("/todo_complete")
# def todo_complete():
#     id = request.args.get('id')
#     Todo.query.filter_by(id=id).update({"status":"已完成"})
#     db.session.commit()
#     return redirect(url_for('todo_list'))

#待办列表
# @app.route('/todo_list/')
# @login_required
# def todo_list():
#
#     page = request.args.get('page', type=int,default=1)
#     limit = request.args.get('limit', type=int,default=10)
#     todo = Todo.query.filter(Todo.status=="待完成").order_by(Todo.id.desc()).paginate(page, limit, error_out=False)
#     counts = todo.total;
#     return render_template('todo_list.html',todo=todo,counts=counts,page=page)

#修改密码
@app.route('/update_pass/',methods=['GET','POST'])
@login_required
def update_pass():
    form = Updateuser()
    user = User.query.first()
    if form.validate_on_submit():
        if form.password1.data != form.password2.data:
            flash(u'两次密码不一致')
        else:
            User.query.filter_by(id=user.id).update({"password_hash":generate_password_hash(form.password1.data)})
            db.session.commit()
            flash(u'密码修改成功')
            return redirect(url_for('update_pass'))
    return render_template('update_pass.html',form=form)

#修改信息
@app.route('/update_info/',methods=['GET','POST'])
@login_required
def update_info():
    user = User.query.first()
    if request.method=="POST":
        User.query.filter_by(id=user.id).update({"nickname":request.form.get('nickname')})
        User.query.filter_by(id=user.id).update({"email":request.form.get('email')})
        flash(u'更新用户信息成功')
        db.session.commit()
        return redirect(url_for('update_info'))
    return render_template('update_info.html',user=user,form=form)

@app.route('/user')
@login_required
def user():
    return render_template('user.html')

@app.route('/fmg/')
@login_required
def fmg():
    return render_template('fmg.html')

@app.route('/fmg_list')
@login_required
def fmg_list():
    fmg = Fmg.query.all()
    return render_template('fmg_list.html',fmg=fmg)

@app.route('/fmg_birthday/')
@login_required
def fmg_birthday():
    birth=[]
    fmg = Fmg.query.all()
    n_today = this_month() #今天的旧历日子
    x_month = datetime.now().strftime("%m") #新历月
    x_day = datetime.now().strftime("%d") #新历日
    for fmg in fmg:
        if fmg.birth_type=="农历":
            #转换月份
            t_month = datetime.strptime(fmg.birthday, "%Y-%m-%d")
            s_month = datetime.strftime(t_month,"%m")
            s_day = datetime.strftime(t_month,"%d")
            if int(s_month) == int(n_today[0]):
                cj = int(s_day) - int(n_today[1])
                birth.append({"id":fmg.id,"name":fmg.name,"sex":fmg.sex,"birth_type":fmg.birth_type,"birthday":fmg.birthday,"phone1":fmg.phone1,"cj":cj,"qq":fmg.qq})

        else:
            t_month = datetime.strptime(fmg.birthday, "%Y-%m-%d")
            s_month = datetime.strftime(t_month,"%m")
            s_day = datetime.strftime(t_month,"%d")
            if int(s_month) == int(x_month):
                cj = int(s_day) - int(x_day)
                birth.append({"id":fmg.id,"name":fmg.name,"sex":fmg.sex,"birth_type":fmg.birth_type,"birthday":fmg.birthday,"phone1":fmg.phone1,"cj":cj,"qq":fmg.qq})
    #排序未做
    birth=sorted(birth, key=operator.itemgetter('cj'))

    return render_template("fmg_birthday.html",birth=birth)

birth=[]
def fmg_mail():
    fmg = Fmg.query.all()
    n_today = this_month() #今天的旧历日子
    x_month = datetime.now().strftime("%m") #新历月
    x_day = datetime.now().strftime("%d") #新历日
    for fmg in fmg:
        if fmg.birth_type=="农历":
            #转换月份
            t_month = datetime.strptime(fmg.birthday, "%Y-%m-%d")
            s_month = datetime.strftime(t_month,"%m")
            s_day = datetime.strftime(t_month,"%d")
            if int(s_month) == int(n_today[0]):
                if int(s_day)==int(n_today[1]) and fmg.id not in birth:
                    mail_title = "%s今天过生日啦" % fmg.name
                    mail_content = "姓名:%s&nbsp;&nbsp;&nbsp;&nbsp性别:%s&nbsp;&nbsp&nbsp;&nbsp生日类型:%s&nbsp;&nbsp&nbsp;&nbsp生日时间:%s&nbsp;&nbsp&nbsp;&nbsp<br>电话:%s<br>喜欢:%s<br>讨厌:%s<br>请带上你的祝福吧！" % (
                        fmg.name,fmg.sex,fmg.birth_type,fmg.birthday,fmg.phone1,fmg.love,fmg.halt
                    )
                    #sendmail(mail_title,mail_content)
                    birth.append(fmg.id)

        else:
            t_month = datetime.strptime(fmg.birthday, "%Y-%m-%d")
            s_month = datetime.strftime(t_month,"%m")
            s_day = datetime.strftime(t_month,"%d")
            if int(s_month) == int(x_month):
                if s_day==x_day and fmg.id not in birth:
                    mail_title = "%s今天过生日啦" % fmg.name
                    mail_content = "姓名:%s&nbsp;&nbsp;&nbsp;&nbsp性别:%s&nbsp;&nbsp&nbsp;&nbsp生日类型:%s&nbsp;&nbsp&nbsp;&nbsp生日时间:%s&nbsp;&nbsp&nbsp;&nbsp<br>电话:%s<br>喜欢:%s<br>讨厌:%s<br>请带上你的祝福吧！" %(fmg.name,fmg.sex,fmg.birth_type,fmg.birthday,fmg.phone1,fmg.love,fmg.halt
                    )
                    sendmail(mail_title,mail_content)
                    birth.append(fmg.id)

#如果时间在每天的凌晨就解锁
def unlook_birth():
    if datetime.now().strftime("%H%M") == "0000":
        birth.clear()

@app.route('/add_fmg/',methods=['POST','GET'])
@login_required
def add_fmg():
    if request.method=="POST":
        fmg = Fmg(name=request.form.get('name'),
                  sex=request.form.get('sex'),
                  birthday=request.form.get('birthday'),
                  birth_type=request.form.get('birth_type'),
                  phone1=request.form.get('phone1'),
                  phone2=request.form.get('phone2'),
                  wechat=request.form.get('wechat'),
                  qq=request.form.get('qq'),
                  love=request.form.get('love'),
                  halt=request.form.get('halt'),
                  note=request.form.get('note'),
                  a_time=datetime.now(),
                  u_time=datetime.now()
                  )
        db.session.add(fmg)
        db.session.commit()
        return redirect(url_for("fmg_list"))
    date = datetime.now().date()
    return render_template('add_fmg.html',date=date)

@app.route('/fmg_more/')
@login_required
def fmg_more():
    id = request.args.get('id')
    fmg = Fmg.query.get(int(id))
    return render_template('fmg_more.html',fmg=fmg)

@app.route('/fmg_edit/')
@login_required
def fmg_edit():
    id = request.args.get('id')
    fmg = Fmg.query.get(int(id))
    return render_template('fmg_edit.html', fmg=fmg)

@app.route('/update_fmg',methods=['POST'])
@login_required
def update_fmg():
    if request.method=="POST":
        id = request.form.get('id')
        name = request.form.get('name')
        sex = request.form.get('sex')
        birthday = request.form.get('birthday')
        birth_type = request.form.get('birth_type')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        wechat = request.form.get('wechat')
        qq = request.form.get('qq')
        love = request.form.get('love')
        halt = request.form.get('halt')
        note = request.form.get('note')

        Fmg.query.filter_by(id=id).update({"name":name})
        Fmg.query.filter_by(id=id).update({"sex":sex})
        Fmg.query.filter_by(id=id).update({"birthday":birthday})
        Fmg.query.filter_by(id=id).update({"birth_type":birth_type})
        Fmg.query.filter_by(id=id).update({"phone1":phone1})
        Fmg.query.filter_by(id=id).update({"phone2":phone2})
        Fmg.query.filter_by(id=id).update({"wechat":wechat})
        Fmg.query.filter_by(id=id).update({"qq":qq})
        Fmg.query.filter_by(id=id).update({"love":love})
        Fmg.query.filter_by(id=id).update({"halt":halt})
        Fmg.query.filter_by(id=id).update({"note":note})
        db.session.commit()
        return redirect(url_for('fmg_list'))
@app.route("/fmg_delete/")
@login_required
def fmg_delete():
    id = request.args.get('id')
    fmg = Fmg.query.get(int(id))
    db.session.delete(fmg)
    db.session.commit()
    return redirect(url_for('fmg_list'))

@app.route('/mail/')
def mail():
    unlook_birth()
    fmg_mail()
    return jsonify({"mssage":"ok"})

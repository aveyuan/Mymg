#encoding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,DateTimeField,SubmitField,BooleanField,SelectField,IntegerField
from wtforms.validators import DataRequired,Length

#登录验证
class LoginForm(FlaskForm):
    username = StringField(u'用户名',validators=[DataRequired(u'用户名不能为空')])
    password = PasswordField(u'密码',validators=[DataRequired(u'密码不能为空')])
    remeberme = BooleanField(render_kw={"lay-skin":"primary","title":u"记住我"})

#修改密码
class Updateuser(FlaskForm):
    password1 = PasswordField(u'密码',validators=[DataRequired(u'密码不能为空')])
    password2 = PasswordField(u'重复密码', validators=[DataRequired(u'密码不能为空')])
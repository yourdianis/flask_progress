import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel
from exts import redis_client

class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20,message="密码格式错误！")])
    #密码等于前面输入的密码
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证：
    # 1.邮箱是否被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱以及被注册了！")

    # 2.验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # Redis中获取验证码
        stored_captcha = redis_client.get(f"captcha:{email}")
        if not stored_captcha or stored_captcha.decode('utf-8') != captcha:
            raise wtforms.ValidationError(message="验证码错误或已过期")


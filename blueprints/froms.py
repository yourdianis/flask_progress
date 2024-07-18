import wtforms
from sqlalchemy.testing.pickleable import User
from wtforms.validators import Email, Length, EqualTo
from models import UserModel
from exts import redis_client


# From主要就是用来验证前端提交的数据是否符合数据
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(walidators=[Email(message="邮箱格式错误！！！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！！！")])
    username = wtforms.StringField(validators=[Length(min=2, max=20, message="用户名格式错误！！！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码码格式错误！！！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # 自定义验证：
    # 1. 邮箱是否被注册
    # 2. 验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        stored_captcha = redis_client.get(f"captcha:{email}")
        if not stored_captcha or stored_captcha != captcha:
            raise wtforms.ValidationError(message="验证码错误或已过期")

import random
from flask import Blueprint, render_template, jsonify, redirect, url_for
from exts import mail, redis_client, db
from flask_mail import Message
from flask import request
import string
from .forms import RegisterForm
from models import UserModel
from werkzeug.security import generate_password_hash

bp = Blueprint("auth", __name__, url_prefix='/auth')


@bp.route('/login')
def login():
    pass


# GET：从服务器请求获取数据
# POST：将客户端的数据提交给服务器
@bp.route('/register', methods=['GET','POST'])
def register():

    if request.method == "GET":
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 验证用户输入的验证码和邮箱的是否对应
        # 表单验证：flask-wtf: wtfroms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            # 创建一个新的用户实例，使用generate_password_hash方法对密码进行哈希处理。
            user = UserModel(username=username, email=email, password=generate_password_hash(password))
            # 将新创建的用户添加到数据库会话中。
            db.session.add(user)
            # 提交数据库会话，将新用户信息保存到数据库中。
            db.session.commit()
            # 重定向到登录页面。
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route('/captcha/email')
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    if not email:
        return "缺少邮箱参数", 400

    # 验证码{4/6: 数组，字面，数组和字面的组合}
    source = string.digits * 4
    # 生成4位随机验证码
    captcha = ''.join(random.choices(source, k=4))

    # 创建邮件内容
    message = Message(
        subject="知了网站注册验证码！",
        recipients=[email],
        body=f"您的验证码是：{captcha}, 您正在通过邮箱登录【XXX的网站】，该验证码5分钟内有效，请勿泄露于他人。"
    )
    try:
        # 发送邮件
        mail.send(message)
        # 缓存验证码：memcached/redis
        email_captcha = redis_client.setex(f"captcha:{email}", 300, captcha)

        # 验证存储是否成功
        stored_captcha = redis_client.get(f"captcha:{email}")
        if stored_captcha:
            print(f"验证码成功存储: {stored_captcha}")
        else:
            print("验证码存储失败")


    except Exception as e:
        error_message = f"邮件发送失败: {str(e)}"
        print(error_message)  # 打印错误信息以便调试
        return error_message, 500

    print(f"验证码: {captcha}")  # 打印验证码以便调试
    # RESTful API
    # {code: 200/400/500, message: "", data: {}}
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route('/mail/test')
def mail_test():
    try:
        message = Message(
            subject="邮箱测试",
            recipients=["3275594770@qq.com"],  # 确保邮箱地址正确
            body="Test"
        )
        mail.send(message)
        return "邮件发送成功"
    except Exception as e:
        error_message = f"邮件发送失败: {str(e)}"
        print(error_message)
        return error_message, 500


#测试是否连接上了redis
@bp.route('/test_redis')
def test_redis():
    try:
        redis_client.ping()
        return "Successfully connected to Redis"
    except Exception as e:
        return f"Error connecting to Redis: {e}"

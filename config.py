# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import time
# 数据库的配置信息
# MySQL所在的主机名
HOSTNAME = "192.168.0.71"
# MySQL监听的端口号,默认3306
PORT = 3306
# 连接MySQL的用户名,读者用自己设置的
USERNAME = "root"
# 连接MySQL的密码,读者用自己的
PASSWORD = "123456"
# MySQL上创建的数据库名称
DATABASE = ("zhiliaooa")

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱地址
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = "3275594770@qq.com"
MAIL_PASSWORD = "dhyajcywjfgwchcd"
MAIL_DEFAULT_SENDER = "3275594770@qq.com"
MAIL_DEBUG = True


# Redis 配置
REDIS_URL = "redis://:123456@192.168.0.49:6379/0"


# # 发送者和接收者邮箱
# sender_email = "3275594770@qq.com"
# receiver_email = "3275594770@qq.com"
#
# # 创建邮件内容
# msg = MIMEMultipart()
# msg['From'] = sender_email
# msg['To'] = receiver_email
# msg['Subject'] = 'Test Email'
# body = 'This is a test email.'
# msg.attach(MIMEText(body, 'plain'))
#
#
# def send_email():
#     global MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL, MAIL_USERNAME, MAIL_PASSWORD, sender_email, receiver_email, msg
#
#     server = None
#     try:
#         if MAIL_USE_SSL:
#             server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, timeout=10)
#         else:
#             server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=10)
#             if MAIL_USE_TLS:
#                 server.starttls()
#
#         server.set_debuglevel(1)  # 启用调试输出
#         server.login(MAIL_USERNAME, MAIL_PASSWORD)
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#         print('Email sent successfully')
#     except smtplib.SMTPServerDisconnected as e:
#         print(f'SMTPServerDisconnected: {e}')
#         print('Attempting to reconnect...')
#         try:
#             time.sleep(5)  # 等待几秒钟再尝试重新连接
#             if MAIL_USE_SSL:
#                 server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, timeout=10)
#             else:
#                 server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=10)
#                 if MAIL_USE_TLS:
#                     server.starttls()
#
#             server.login(MAIL_USERNAME, MAIL_PASSWORD)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#             print('Email sent successfully on retry')
#         except Exception as retry_error:
#             print(f'Retry failed: {retry_error}')
#     except Exception as e:
#         print(f'Failed to send email: {e}')
#     finally:
#         if server:
#             try:
#                 server.quit()
#             except Exception as e:
#                 print(f'Error closing connection: {e}')
#
#
# # 发送邮件
# send_email()
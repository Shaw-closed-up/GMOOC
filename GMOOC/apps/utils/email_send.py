# -*- coding: utf-8 -*-
# @Time    : 2017/12/13 23:47
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : email_send.py
# @Software: PyCharm

from users.models import EmailVerifyCode
from random import Random
from django.core.mail import send_mail
from GMOOC.settings import EMAIL_HOST,EMAIL_PORT,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,EMAIL_USE_TLS,EMAIL_FROM

#随机生成验证吗，长度可调
def random_str(random_length=8):
    code = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    random = Random()
    length = len(chars)-1
    for i in range(random_length):
        code += chars[random.randint(0,length)]
    return code


def send_email(email, send_type='register'):
    ###########################生成随机验证码存入数据库中###########################
    #继承模型
    email_record = EmailVerifyCode()
    if send_type == 'update':
        code = random_str(4)    #如果是更新邮箱则发送4位验证码
    else:
        code = random_str(16)
    #将随机生成code存入数据库中
    email_record.code = code
    #将管理的邮箱传入数据库中
    email_record.email = email
    #定义发送类型
    email_record.send_type = send_type
    email_record.save()

    ###########################发送激活邮件###########################
    email_title = ''
    email_body = ''
    receive_email = email

    if send_type == 'register':
        email_title = '慕学在线激活连接'
        email_body = '请点击下方连接，激活注册：'+'http://127.0.0.1:8000/active/{0}'.format(code)

    if send_type =='find_password':
        email_title = '慕学在线密码找回连接'
        email_body = '请点击下方连接，进行密码找回：' + 'http://127.0.0.1:8000/password_reset/{0}'.format(code)

    if send_type == 'update':
        email_title = '慕学在线更新邮箱的验证码'
        email_body = '更新邮箱的验证码是：' +code

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [receive_email])





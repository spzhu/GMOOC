# -*- coding: utf-8 -*-
'''
__author__ = 'spzhu'
__date__ = '2018-03-02 18:59:50'
'''
import random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from gmooc.settings import EMAIL_FROM


def gen_random_str(random_length=8):
    str = ''
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    length = len(chars) - 1
    for i in range(random_length):
        str+=chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    random_str = gen_random_str(16)
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == "register":
        email_title = "慕学在线账号激活"
        email_body = "请点击下面链接激活您的账号: http://127.0.0.1:8000/active/{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("send mail successful.")
        else:
            print("send mail failed.")
    elif send_type == "forget":
        email_title = "慕学在线密码找回"
        email_body = "请点击下面链接重置您的密码: http://127.0.0.1:8000/reset/{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    return send_status

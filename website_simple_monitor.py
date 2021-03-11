# -*- coding: utf8 -*-
import ssl
import smtplib
import urllib.request
from email.mime.text import MIMEText
from email.header import Header

# 关闭ssl验证
ssl._create_default_https_context = ssl._create_unverified_context


def sendEmail(content, to_user):
    '''
    发送邮件
    :param content: 发送的邮件内容
    :param to_user: 发送的目标用户
    :return:
    '''
    sender = 'service@anycodes.cn'  # 发送者邮箱地址
    receivers = [to_user]  # 目标用户的邮箱地址

    # 邮件内容
    mail_msg = content
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("网站监控", 'utf-8')
    message['To'] = Header("站长", 'utf-8')
    subject = "网站监控告警"
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        smtpObj.login('发送邮件的邮箱地址', '密码')
        smtpObj.sendmail(sender, receivers, message.as_string())
    except Exception as e:
        print(e)


def getStatusCode(url):
    '''
    获取网站的状态码
    :param url: 网址
    :return: 状态码
    '''
    return urllib.request.urlopen(url).getcode()


def handler(event, context):
    # 待监控的地址
    url = "http://www.anycodes.cn"

    # 如果状态不为200，则进行告警
    if getStatusCode(url) == 200:
        print("您的网站%s可以访问！" % (url))
    else:
        sendEmail("您的网站%s 不可以访问！" % (url), "接受人邮箱地址")

    return None

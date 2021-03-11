# -*- coding: utf8 -*-
import ssl
import re
import socket
import smtplib
import urllib.request
from email.mime.text import MIMEText
from email.header import Header

# 设置整体的请求超时时间
socket.setdefaulttimeout(2.5)
# 关闭ssl验证
ssl._create_default_https_context = ssl._create_unverified_context


def getWebTime():
    '''
    获取网站的延时信息
    :return: 每个节点的延时
    '''
    service_content = []
    service_status = True

    node = [
        ('62a55a0e-387e-4d87-bf69-5e0c9dd6b983', '江苏宿迁[电信]'),
        ('f403cdf2-27f8-4ccd-8f22-6f5a28a01309', '广东佛山[电信]'),
        ('5bea1430-f7c2-4146-88f4-17a7dc73a953', '河南新乡[多线]'),
        ('1f430ff0-eae9-413a-af2a-1c2a8986cff0', '河南新乡[多线]'),
        ('ea551b59-2609-4ab4-89bc-14b2080f501a', '河南新乡[多线]'),
        ('2805fa9f-05ea-46bc-8ac0-1769b782bf52', '黑龙江哈尔滨[联通]'),
        ('722e28ca-dd02-4ccd-a134-f9d4218505a5', '广东深圳[移动]'),
        ('8e7a403c-d998-4efa-b3d1-b67c0dfabc41', '广东深圳[移动]'),
    ]

    url = "*某测速网站地址*"
    for eve_node in node.split('\n'):
        node_name = eve_node[1]
        form_data = {
            'guid': eve_node[0],
            'host': 'anycodes.cn',
            'ishost': '1',
            'encode': 'ECvBP9vjbuXRi0CVhnXAbufDNPDryYzO',
            'checktype': '1',
        }
        headers = {
            'Host': '*某测速网站地址*',
            'Origin': '*某测速网站地址*',
            'Referer': '*某测速网站地址*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            service_info = urllib.request.urlopen(
                urllib.request.Request(
                    url=url,
                    data=urllib.parse.urlencode(form_data).encode('utf-8'),
                    headers=headers
                )
            ).read().decode("utf-8")
            try:
                alltime = re.findall("alltime:'(.*?)'", service_info)[0]
                conntime = re.findall("conntime:'(.*?)'", service_info)[0]
                downtime = re.findall("downtime:'(.*?)'", service_info)[0]
                temp_service_content = "%s\t总耗时:%s\t链接耗时:%s\t下载耗时:%s" % (node_name, alltime, conntime, downtime)
            except:
                temp_service_content = "%s链接异常！" % (node_name)
                service_status = False
        except:
            temp_service_content = "%s链接超时！" % (node_name)
            service_status = False
        service_content.append(temp_service_content)
    return (service_status, service_content)


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


def handler(event, context):
    # 待监控的地址
    url = "http://www.anycodes.cn"

    service_status, service_content = getWebTime()
    if not service_status:
        sendEmail("您的网站%s的状态：<br>%s" % (url, "<br>".join(service_content)), "service@52exe.cn")

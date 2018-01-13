#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/5 16:31
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : utilities.py

import os
from traceback import print_exc
from flask import render_template
import sys

# reload(sys) # for python2
# sys.setdefaultencoding('utf-8')


def send_email(to_list, subject, content, template, files, **kwargs):
    from smtplib import SMTP_SSL
    from email.header import Header
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart

    to_list = ['xtet2008@126.com'] if not to_list else to_list
    to_list = [to_list] if not isinstance(to_list, list) else to_list

    mail_info = {
        "from": "370726390@qq.com",
        "to": to_list,
        "hostname": "smtp.qq.com",
        "username": "370726390@qq.com",
        "password": "sdfbcdgqmbjwbjca",
        "mail_subject": subject,
        "mail_text": content,
        "mail_encoding": "utf-8"
    }

    smtp = SMTP_SSL(mail_info.get('hostname'))
    smtp.set_debuglevel(0)  # 1 will be print mail send msg log , 0 hiden the mail send log
    smtp.ehlo(mail_info.get('hostname'))
    smtp.login(mail_info.get('username'), mail_info.get('password'))

    msg = MIMEMultipart()
    msg['Subject'] = Header(mail_info.get('mail_subject'), mail_info.get('mail_encoding'))
    msg['From'] = mail_info.get('from')
    msg['To'] = ';'.join(to_list)
    if mail_info.get('mail_text'):
        msg.attach(MIMEText(mail_info.get('mail_text'), _subtype='plain', _charset=mail_info.get('mail_encoding')))
    if template:
        subtype = 'html' if os.path.splitext(template)[1] == '.html' else 'plain'
        msg.attach(MIMEText(render_template(template, **kwargs), _subtype=subtype, _charset='utf-8'))


    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=os.path.basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
            part.set_charset('utf-8')
            msg.attach(part)

    try:
        smtp.sendmail(mail_info.get('from'), mail_info.get('to'), msg.as_string())
    except Exception as e:
        print (e)
        print (e.message)
        return False
    finally:
        smtp.quit()
    return True


def send_message(msg):
    result = False

    if not msg:
        return result

    import top.api

    url = "gw.api.taobao.com"
    port = 80
    appkey = "23344039"
    secret = "b0e38514ff1ba7e10f3847af902c6cfa"

    req = top.api.AlibabaAliqinFcSmsNumSendRequest(url, port)
    req.set_app_info(top.appinfo(appkey, secret))

    req.extend = ""
    req.sms_type = "normal"
    req.sms_free_sign_name = "张胜"
    req.sms_param = "{name:\'%s\'}" % (msg)
    print( req.sms_param)
    req.rec_num = "18618458391"
    req.sms_template_code = "SMS_121945033"
    try:
        resp = req.getResponse()
        result = True
        print (resp)
    except Exception as e:
        print_exc()

    return result
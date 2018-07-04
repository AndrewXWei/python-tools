# encoding=utf8
"""
send email (need a valid email agent on the server)
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import smtplib

def send_mail(me, to_list, content, subject, attachfilepath, attachfilename):
    """
    send email
    :param to_list:
    :param content:
    :param subject:
    :return:
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    # contents html
    cont = MIMEText(content, _subtype='html', _charset='utf8')
    msg.attach(cont)

    # add attachment
    att1 = MIMEText(open(attachfilepath, 'rb').read(), 'base64', 'utf8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment;filename="' + attachfilename + '"'
    msg.attach(att1)

    s = smtplib.SMTP()
    s.connect()
    for item in to_list:
        if item.find(".com") != -1:
            s.sendmail(me, item, msg.as_string())
    s.quit()
    return 1

# receiverList
receiverList = []
receiverList.append("receiver1@xxx.com")
receiverList.append("receiver2@xxx.com")

if __name__ == '__main__':
    me = 'sendmail@xxx.com'
    mail_subject = 'title'
    mail_content = 'mail_content_xxx'
    # path of attachfile
    attachfilepath = 'attachfilepath'
    # name of attachfile
    attachfilename = 'attachfilename'
    # 发送结果邮件
    print send_mail(me, receiverList, mail_content, mail_subject, attachfilepath, attachfilename)


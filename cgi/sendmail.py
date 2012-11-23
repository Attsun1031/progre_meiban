#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import smtplib
import urllib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

print "Content-Type: text/html; charset=utf-8"
print

def create_message(from_addr, to_addr, subject, body, encoding):
    msg = MIMEText(body, 'plain', encoding)
    msg['Subject'] = Header(subject, encoding)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send(from_addr, to_addr, msg):
    s = smtplib.SMTP('smtp.mail.yahoo.co.jp', 587)
    s.ehlo()
    s.login('wbc1101611016', 'henevsop')
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

form = cgi.FieldStorage()
if (form.has_key('comment')):
    from_addr = 'wbc1101611016@yahoo.co.jp'
    to_addr = 'info@progre-meiban.com'
    body = str(urllib.unquote_plus(form.getvalue('comment')))
    msg = create_message(from_addr, to_addr, u'コメント', body, 'utf-8')
    send(from_addr, to_addr, msg)

print 'Success'
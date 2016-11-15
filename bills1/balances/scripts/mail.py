#-*- coding: utf-8 -*-


import smtplib
from email.mime.text import MIMEText
from balances.models import Account_details

def send_email(receiver,message):
    acd = Account_details.objects.get(QA='bsk')
    to = receiver
    o2_user = str(acd.admin_email_login)
    o2_pwd = str(acd.admin_email_password)
    smtpserver = smtplib.SMTP("poczta.o2.pl",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(o2_user, o2_pwd)
    msg = MIMEText('\n zestawienie oplat za media dla :' + message)
    msg['Subject'] = 'oplaty'
    msg['From'] = o2_user
    msg['To'] = to
    msg['Cc'] = str(acd.admin_email)
    recievers=[]
    recievers.append(to)
    recievers.append(acd.admin_email)


    smtpserver.sendmail(o2_user, recievers, msg.as_string())

    smtpserver.close()

#send_email('sebastian_d@o2.pl','teszt żółtą jaźń')

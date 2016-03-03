# coding: utf-8

import os
import re
import requests
import time
import smtplib
from bs4 import BeautifulSoup
from account_info import *
from email.mime.text import MIMEText
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class autochkweibo:

    def __init__(self, usrid):
        self.url = 'http://weibo.cn/' + usrid
        self.relaxtime = 1000
        self.headers = {'User-Agent':'Chrome'}
        with open(os.path.expanduser('~/.weibocookie')) as f:
            self.headers['Cookie'] = f.read().strip()
        self.count = 0
        self.fst = ''

    def sm(self, con='', sub=''):
        msg = MIMEText(con, 'plain', 'utf-8')
        me = 'Auto_Check_Weibo<' + EMAIL_USER + '@' + FROM_EMAIL_HOST + '>'
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = TO_EMAIL
        for i in range(3):
            try:
                s = smtplib.SMTP()
                s.connect(FROM_EMAIL_HOST, FROM_EMAIL_PORT)
                s.login(EMAIL_USER, EMAIL_PASSWD)
                s.sendmail(me, TO_EMAIL, msg.as_string())
                s.close()
                print "Mail Sent"
                return True
            except Exception, e:
                print e
        return False        
        
    def chk(self):
        while True:
            try:
                s = requests.get(self.url, headers=self.headers)
                break
            except:
                time.sleep(100)
        soup = BeautifulSoup(s.text)
        try:
            count = int(re.search(r"微博\[(.*?)\]",soup.find('span','tc').get_text().encode('utf-8')).group(1))
        except Exception, e:
            print e
            return False
        if count > self.count:
            l = soup.find_all('div','c',id=True)
            self.count = count
            msg = "当前共有%s条微博。\n\n" % self.count
            for item in l:
                msg += item.get_text()+'\n\n'
            sub = "TA发了新微博"
            self.sm(msg, sub)
        else:
            self.count = count

    def startchk(self):
        while True:
            self.chk()
            time.sleep(self.relaxtime)

if __name__ == '__main__':
    s = raw_input("请输入TA的微博id：")
    p = autochkweibo(s)
    try:
        p.startchk()
    except KeyboardInterrupt:
        print "\nScript is terminated."
                




   

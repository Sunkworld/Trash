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
        self.usrid = usrid
        self.url = 'http://weibo.cn/' + usrid
        self.fanurl = 'http://weibo.cn/' + usrid +'/fans'
        self.followurl = 'http://weibo.cn/' + usrid + '/follow'
        self.relaxtime = RELAX_TIME
        self.headers = {'User-Agent':'Chrome'}
        with open(os.path.expanduser('~/.weibocookie')) as f:
            self.headers['Cookie'] = f.read().strip()
        self.weibocount = 0
        

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
		s.starttls()
                s.login(EMAIL_USER, EMAIL_PASSWD)
                s.sendmail(me, TO_EMAIL, msg.as_string())
                s.close()
                print "Mail Sent"
                return True
            except Exception, e:
                print e
        return False

    def getInfo(self):
        while True:
            while True:
                try:
                    s = requests.get(self.url, headers=self.headers)
                    break
                except:
                    time.sleep(60)
            self.soup = BeautifulSoup(s.text)
            self.soup_text = self.soup.prettify()
#            print self.soup_text
            try:
                tip2 = self.soup.find('div','tip2')
                tmp = re.findall(r'\[(.*?)\]', tip2.get_text().encode('utf-8'))
                self.weibocount = int(tmp[0])
                self.followcount = int(tmp[1])
                self.fanscount = int(tmp[2])
                self.name = re.search('ctt">\n *(.*?)[ \n]', self.soup_text.replace(u'\xa0',u' ').encode('utf-8')).group(1)
                self.profile = self.soup.find('span','ctt', style=True).string
                self.weibolist = []
                for item in self.soup.find_all('div','c', id=True):
                    self.weibolist.append(item['id'])
                tmp = BeautifulSoup(requests.get(self.fanurl, headers=self.headers).text)
                self.fanslist = []
                for item in tmp.find_all('td', valign='top', style=None):
                    self.fanslist.append(item.a.string)
                tmp = BeautifulSoup(requests.get(self.followurl, headers=self.headers).text)
                self.followlist = []
                for item in tmp.find_all('td', valign='top', style=None):
                    self.followlist.append(item.a.string)
                print "User Info Fetched: %s" % self.name
                break
            except Exception, e:
                self.sm(self.soup_text.encode('utf-8'), "Error in Function %s" % sys._getframe().f_code.co_name)
                print e
                time.sleep(100)
                

    def getContent(self):
        while True:
            try:
                s = requests.get(self.url, headers=self.headers)
                break
            except:
                time.sleep(100)
        self.soup = BeautifulSoup(s.text)
        self.soup_text = self.soup.prettify()
        try:
            weibocount = int(re.search(r"微博\[(.*?)\]", self.soup.find('span','tc').get_text().encode('utf-8')).group(1))
        except Exception, e:
	    self.sm(self.soup_text.encode('utf-8'), "Error in Function %s" % sys._getframe().f_code.co_name)
            print e
            return False
        return True
        


    def chk_weibo(self, d):
        weibocount = int(re.search(r"微博\[(.*?)\]", self.soup.find('span','tc').get_text().encode('utf-8')).group(1))
        msg = "当前共有%s条微博。\n\n" % self.weibocount
        weibolist = []
        for item in self.soup.find_all('div','c', id=True):
            weibolist.append(item['id'])
        if weibocount > self.weibocount or weibolist[0] not in self.weibolist:
            l = self.soup.find_all('div','c',id=True)
            for item in l:
                msg += item.get_text()+'\n\n'
            sub = "%s发了新微博" % self.name
            self.sm(msg, sub)
        elif  weibocount < self.weibocount:
            if d == 1:
                l = self.soup.find_all('div','c',id=True)
                msg = "当前共有%s条微博。\n\n" % weibocount
                for item in l:
                    msg += item.get_text()+'\n\n'
                sub = "%s删去了%s条微博" % (self.name, str(self.weibocount - weibocount))
                self.sm(msg, sub)
        self.weibocount = weibocount
        self.weibolist = weibolist


    def chk_follow(self):
        tip2 = self.soup.find('div','tip2')
        tmp = re.findall(r'\[(.*?)\]', tip2.get_text().encode('utf-8'))
        followcount = int(tmp[1])
        while True:
            try:
                tmp = BeautifulSoup(requests.get(self.followurl, headers=self.headers).text)
                break
            except Exception, e:
                sleep(100)
        if re.search('自动跳转', tmp.encode('utf-8')):
            self.sm(tmp.prettify().encode('utf-8'), "Error in Function %s" % sys._getframe().f_code.co_name)
            return False
        followlist = []
        for item in tmp.find_all('td', valign='top', style=None):
            followlist.append(item.a.string)
        newfollow = []
        for item in followlist:
            if item not in self.followlist:
                newfollow.append(item)
        if len(newfollow):
            msg = "%s当前关注了%s位用户。\n\n新关注用户有：\n" % (self.name, followcount)
            for item in newfollow:
                msg += "%s\n" % item
            msg += "\n目前关注用户列表为：\n"
            for item in followlist:
                msg += "%s\n" % item
            sub = "%s有新关注的用户" % self.name
            self.sm(msg, sub)
        self.followcount = followcount
        self.followlist = followlist
        


    def chk_fans(self):
        tip2 = self.soup.find('div','tip2')
        tmp = re.findall(r'\[(.*?)\]', tip2.get_text().encode('utf-8'))
        fanscount = int(tmp[2])
        while True:
            try:
                tmp = BeautifulSoup(requests.get(self.fanurl, headers=self.headers).text)
                break
            except Exception, e:
                sleep(100)
        if re.search('自动跳转', tmp.encode('utf-8')):
            self.sm(tmp.prettify().encode('utf-8'), "Error in Function %s" % sys._getframe().f_code.co_name)
            return False
        fanslist = []
        for item in tmp.find_all('td', valign='top', style=None):
            fanslist.append(item.a.string)
        newfan = []
        for item in fanslist:
            if item not in self.fanslist:
                newfan.append(item)
        if len(newfan):
            msg = "%s当前有%s位粉丝。\n\n新增粉丝有：\n" % (self.name, fanscount)
            for item in newfan:
                msg += "%s\n" % item
            sub = "有新用户关注了%s" % self.name
            self.sm(msg, sub)
        self.fanscount = fanscount
        self.fanslist = fanslist
    
    def chk_profile(self):
        profile = self.soup.find('span','ctt', style=True).string
        if profile != self.profile:
            msg = "新的个人简介为：\n"
            if profile:
                msg += profile
            else:
                msg = "个人简介已被清空"
            sub = "%s更新了个人简介" % self.name
            self.sm(msg, sub)
        self.profile = profile

    def auto_like(self):
        l = re.findall('"(.*?)\?uid=(.*?)&amp;rl=0&amp;st=(.*?)">\n *?赞', self.soup_text.encode('utf-8'))
        for item in l:
            requests.get(item[0]+'?uid='+item[1]+'&rl=0&st='+item[2], headers=self.headers)
            time.sleep(2)
            
            
    def chk(self):
        while True:
            if self.getContent():
                break
            else:
                sleep(500)
        if CHK_WEIBO:
            self.chk_weibo(CHK_WEIBO_DELETED)
        if CHK_FOLLOW:
            self.chk_follow()
        if CHK_FANS:
            self.chk_fans()
        if CHK_PROFILE:
            self.chk_profile()
        if AUTO_LIKE:
            self.auto_like()        

if __name__ == '__main__':
#    s = raw_input("请输入TA的微博id：")
#    s = '1197191492'
    s = DESTINATED_WEIBO
    p = []
    for item in s:
        p.append(autochkweibo(item))
        p[len(p)-1].getInfo()
        time.sleep(2)
    while True:
        try:
            for item in p:
                item.chk()
                time.sleep(5)
        except KeyboardInterrupt:
            print "\nScript is terminated."
        time.sleep(item.relaxtime)





#!/usr/bin/env python
# coding: utf-8

import requests
import re
import os
from time import sleep
import denoise
import thread

class pku_elective:
    oauthLogin = 'https://iaaa.pku.edu.cn/iaaa/oauthlogin.do'
    ssoLogin = 'http://elective.pku.edu.cn/elective2008/ssoLogin.do'
    page = []
    page.append('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do')
    page.append('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp?netui_pagesize=electableListGrid%3B20&netui_row=electableListGrid%3B20')
    page.append('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp?netui_pagesize=electableListGrid%3B20&netui_row=electableListGrid%3B40')
    page_capt = 'http://elective.pku.edu.cn/elective2008/DrawServlet?Rand=9912.118702195585'
    page_valid = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/validate.do?validCode='
    page_refresh = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/refreshLimit.do'
    page_elect = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/electSupplement.do'
    count = 0
    def __init__(self, numbers):
        self.data = []
        self.sess = requests.Session()
        self.numbers = numbers
        self.now = 0

    def getNext(self, url, params=[], referer=''):
        if referer != '':
            self.sess.headers.update({'Referer':referer})
        while True:
            try:
                r = self.sess.get(url, params=params)
                break
            except:
                print "Network Problem...1"
                sleep(30)
        return r.content
    
    def postNext(self, url, data=[], referer=''):
        if referer != '':
            self.sess.headers.update({'Referer':referer})
        while True:
#            print url, data, self.sess.headers
            try:
                r = self.sess.post(url, data)
#                print r.text
                break
            except:
                print "Network Problem...2"
                sleep(30)
        return r.content

    def getId(self):
        with open(os.path.expanduser('~/.its')) as f:
            fr = f.read().split()
            usrn = fr[0]
            pswd = fr[1]
        self.data = {'appid':'syllabus', 'userName':'%s' % usrn, 'password':'%s' % pswd, 'randCode':'验证码', 'smsCode':'短信验证码', 'redirUrl':'http://elective.pku.edu.cn:80/elective2008/agent4Iaaa.jsp/../ssoLogin.do'}
        self.sess.headers.update({'User-Agent':'Chrome'})

    def login(self):
        cont = self.postNext(pku_elective.oauthLogin, self.data)
        p = {}
        p['token'] = re.search(r'n":"(.*?)"',cont).group(1)
        p['rand'] = 0.32874243
        self.getNext(pku_elective.ssoLogin, p)

    def getContent(self):
        cont = []
        while True:
            try:
                cont.append(self.getNext(pku_elective.page[0], referer=pku_elective.ssoLogin))
                try:
                    self.now = re.search(r'总学分为：(.*?)<', cont[len(cont)-1]).group(1)
                except:
                    self.sess = requests.Session()
                    self.getStart()
                break
            except:
                print "Network Problem...3"
                sleep(30)
        try:
            cont.append(self.getNext(pku_elective.page[1], referer=pku_elective.page[0]))
        except:
            pass
        try:
            cont.append(self.getNext(pku_elective.page[2], referer=pku_elective.page[1]))
        except:
            pass
        return cont

    def decaptcha(self):
        while True:
            capt = self.getNext(pku_elective.page_capt)
            with open('1.jpg','wb+') as p:
                p.write(capt)
            denoise.process('1.jpg', '2.jpg')
            os.system('tesseract -psm 8 2.jpg outputbase 2>/dev/null')
            with open('outputbase.txt') as p:
                t = p.read().strip()
            try:
                res = self.getNext(pku_elective.page_valid+t)
            except:
                print "Network Problem...4"
                sleep(30)
            if re.search(r'<valid>2</valid>', res):
                break
            
    def getCourse(self):
        cont = self.getContent()
        courseList = []
        for i in range(len(cont)):
            fl = re.finditer(r'refreshLimit(.*?)\'\',\'(.*?)\',\'(.*?)\',\'(.*?)\'', cont[i])
            if not fl:
                continue
            for match in fl:
                for j in range(len(self.numbers)):
                    if match.group(4) == self.numbers[j]:
                        courseList.append({'index':'%s' % match.group(2),
                                           'seq':'%s' % match.group(3),
                                           'num':'%s' % self.numbers[j],
                                           'page':'%s' % i})
#        print courseList
        return courseList

    def reFresh(self, cl):        
        while True:            
            if len(cl) == 0:
                quit()
            for i in range(len(cl)):
                p = {}
                p['index'] = cl[i]['index']
                p['seq'] = cl[i]['seq']
                while True:
                    try:
                        sr1 = self.getNext(pku_elective.page_refresh, p, pku_elective.page[int(cl[i]['page'])])
                        break
                    except:
                        print "Network Problem...5"
                        sleep(30)
                try:
                    fi1 = re.search(r'Num>(.*?)</', sr1).group(1)
                except:
                    self.sess = requests.Session()
                    self.getStart()
#                print fi1
                if fi1 != cl[i]['num']:
                    self.elect(cl, i)
                sleep(5)
            pku_elective.count += 1
            print "There is no vacancy. Try time %s" % pku_elective.count
                        

    def elect(self, cl, i):
        p = {}
        p['index'] = cl[i]['index']
        p['seq'] = cl[i]['seq']
        while True:
            try:
                sr1 = self.getNext(pku_elective.page_elect, p, pku_elective.page[int(cl[i]['page'])])
                break
            except:
                print "Network Problem...6"
                sleep(30)
        c = self.getNext(pku_elective.page[0], referer=pku_elective.ssoLogin)
        s = re.search(r'总学分为：(.*?)<', c)
        if s:
            if s.group(1) != self.now:
                print "选上了人数为%s的课" % cl[i]['num']
                self.now = s.group(1)
            else:
                print "选课失败"
        else:
            print "Unknown Error"
        sess = requests.Session()
        self.getStart()
            
    
    def getStart(self):
        self.getId()        
        self.login()
        cl = self.getCourse()
        self.decaptcha()
        self.reFresh(cl)
numbers = raw_input("Please enter the maxium people of your desired course:").split()
new_elective = []
for i in range(5):
    new_elective.append(pku_elective(numbers))
    thread.start_new_thread(new_elective[len(new_elective)-1].getStart, ())
    sleep(5)
new_elective.append(pku_elective(numbers))
new_elective[len(new_elective)-1].getStart()




    
        

        
    



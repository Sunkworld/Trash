#!/usr/local/bin/python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re,os
import sys
import json
from time import sleep
from funcs import functions
class gmgard:
    url = 'http://gmgard.com'
    loginUrl = 'http://gmgard.com/Account/Login'
    captchaUrl = 'http://gmgard.com/Captcha/CaptchaImage'
    def __init__(self, cookiefile):
        self.s = requests.session()
        self.s.headers.update({'User-Agent':'Chrome',
                               'Referer':self.loginUrl})
        self.isCookie = 1
        if os.path.exists(cookiefile):
            with open(cookiefile, 'rb+') as f:
                self.s.cookies.update(json.load(f))
            res = self.s.get(self.url)
            soup = BeautifulSoup(res.content)
            if not re.search('sunkworld', res.content):
                print "Cookie expired."
            else:
                self.RVT = soup.find('input')['value']
        else:
            self.isCookie = 0
        
    def login(self):
#        self.usrn = ''#raw_input('Username: ')
#        self.pswd = ''#raw_input('Password: ')
        res = self.s.get(self.loginUrl)
        soup = BeautifulSoup(res.content)
        self.RVT = soup.find('input')['value']
        with open('captcha.jpg', 'wb+') as f:
            f.write(self.s.get(self.captchaUrl).content)
        captcha = raw_input('Captcha: ')
        data = {'__RequestVerificationToken':self.RVT,
                'UserName':self.usrn,
                'Password':self.pswd,
                'Captcha':captcha,
                'RemenberMe':'true',
                'RememberMe':'false'}
#        print self.s.cookies.get_dict()
        r = self.s.post(self.loginUrl, data=data)
        with open('1.html', 'wb+') as f:
            f.write(self.s.get(self.url).content)
        print self.s.cookies.get_dict()
        with open('cook', 'wb+') as f:
            json.dump(self.s.cookies.get_dict(), f)
    def signIn(self):
        msg = ''
        url = 'http://gmgard.com/Home/SignIn'
        data = {'__RequestVerificationToken':self.RVT,
                'ismakeup':'false'}
        r = self.s.post(url, data)
        if r.json()['success'] == True:
            msg += "Signin successful."
            print "Signin successful."
        else:
            msg += r.text
            print r.json()
        functions.send(msg, 'Auto_Signin_Gmgard')

if __name__ == '__main__':
    gm = gmgard('cook')
    gm.usrn = 'sunkworld'
    gm.pswd = ''
    if gm.isCookie == 0:
        gm.login()
    while True:
        gm.signIn()
        sleep(81000)
            

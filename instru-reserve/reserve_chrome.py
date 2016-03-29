#coding:utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import requests
import decaptcha
class Sele():
    def __init__(self):
        self.usrn = u''
        self.pswd = ''
        self.w = webdriver.Chrome()
        self.count = 0
    def openBrowser(self):
        isDone = 0
        while not isDone:
            self.w.get('http://162.105.27.251')
            cookie = [item["name"] + "=" + item["value"] for item in self.w.get_cookies()]
            cookiestr = ';'.join(item for item in cookie)
            s = requests.session()
            url = 'http://162.105.27.251'
            s.headers.update({'cookie':cookiestr})
            while True:
                try:
                    cc = decaptcha.decaptcha(s.get('http://162.105.27.251/Validate.aspx').content)
                    for i in cc:
                        if (i<='9' and i>='0') or (i<='Z' and i>='A'):
                            pass
                        else:
                            return False
                    print cc
                    break
                except:
                    time.sleep(30)

            a = self.w.find_element_by_xpath('//input[@name="ctl00$ContentPlaceHolder1$tbUsename"]')
            a.send_keys(self.usrn)
            b = self.w.find_element_by_xpath('//input[@name="ctl00$ContentPlaceHolder1$tbPassword"]')
            b.send_keys(self.pswd)
            c = self.w.find_element_by_xpath('//input[@name="ctl00$ContentPlaceHolder1$tbyzm"]')
            #        cc = raw_input('Enter the captcha:')
            c.send_keys(cc)
            self.w.find_element_by_xpath('//input[@name="ctl00$ContentPlaceHolder1$btLogin"]').click()#login
            try:
                self.w.switch_to_alert().accept()
            except:
                isDone = 1

    def changeDate(self, limit):
        for i in range(30, 32):
            e = self.w.find_element_by_name('ctl00$ContentPlaceHolder1$ddlday')
            for option in e.find_elements_by_tag_name('option'):
                if option.text == str(i):
                    option.click()
                    break
            self.checkVacancy()
        e = self.w.find_element_by_name('ctl00$ContentPlaceHolder1$ddlday')
        e.find_element_by_xpath("//option[@value='30']").click()
        e = self.w.find_element_by_name('ctl00$ContentPlaceHolder1$ddlmonth')
        e.find_element_by_xpath("//option[@value='4']").click()
#        self.w.switch_to_alert().accept()
        self.checkVacancy()
        for i in range(2, limit+1):
            e = self.w.find_element_by_name('ctl00$ContentPlaceHolder1$ddlday')
            for option in e.find_elements_by_tag_name('option'):
                if option.text == str(i):
                    option.click()
                    break
#                e.find_element_by_xpath("//option[@value='%s']" % str(i)).click()
            
            self.checkVacancy()

    def checkVacancy(self):
        self.w.find_element_by_name('ctl00$ContentPlaceHolder1$btxrq').click()
        s = self.w.page_source
        soup = BeautifulSoup(s)
        checkboxes = soup.find_all('input', type="checkbox", disabled=None)
        isVacancy = 0
        for item in checkboxes:
            try:
                h = int(re.match('(.*?):(.*?)-(.*?):(.*?)',item.parent.get_text().strip()).group(1))
            except:
                continue
            if h < 22 and h > 9:
                self.w.find_element_by_xpath("//input[@id='%s']" % item['id']).click()#select
                print "Vacancy at %s o'clock" % h
                isVacancy = 1
        if isVacancy:
            self.w.find_element_by_xpath("//input[@name='ctl00$ContentPlaceHolder1$btyy']").click()#submit
        time.sleep(2)
    def startWork(self, limit):
        self.openBrowser()
        while True:
            self.w.find_element_by_xpath('//a[@id="ctl00_lkbyyyq"]').click()#goto page(this should be moved to refresh part)
            self.changeDate(limit)
            self.count += 1
            print "Try time %s" % self.count
            


if __name__ == '__main__':
    sel = Sele()
    sel.startWork(5)

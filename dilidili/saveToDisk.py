# coding: utf-8
import requests
import requesocks
import os
import re
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
import sys
sys.path.append('..')
from funcs import functions
def login(usrn, pswd):
    w = webdriver.Chrome()
    s = requests.Session()
    url = 'http://pan.baidu.com'
    w.get(url)
    w.delete_all_cookies()
    s.get(url)
    if os.path.exists('cook'):
        with open('cook','rb+') as f:
            for item in json.load(f):
                s.cookies.update(item)
                w.add_cookie(item)
    else:
        w.add_cookie({'name':'BAIDUID', 'value':s.cookies.get_dict()['BAIDUID']})
        a = w.find_element_by_xpath('//input[@name="userName"]')
        a.send_keys(usrn)
        a = w.find_element_by_xpath('//input[@name="password"]')
        a.send_keys(pswd)
        a = w.find_element_by_xpath('//input[@type="submit"]')
        a.click()
        while True:
            a = w.find_element_by_xpath('//input[@name="verifyCode"]')
            try:
                a.clear()
            except:
                break
            soup = BeautifulSoup(w.page_source)
            u =soup('img')[-2]['src']
            isAsc = 0
            while not isAsc:
                capt = functions.decaptcha(s.get(u).content)
                isAsc = 1
                for i in capt:
                    if (i<='9' and i>='0') or (i<='Z' and i>='A'):
                        pass
                    else:
                        isAsc = 0
            a.send_keys(capt)
            a = w.find_element_by_xpath('//input[@type="submit"]')
            a.click()
        with open('cook', 'wb+') as f:
            f.write(json.dumps(w.get_cookies()))
    return w
def saveToDisk(w, url2):
    w.get(url2)
    suburl = re.search('typicalPath":"(.*?)"', w.page_source).group(1).replace('\\/','%252F')
    w.get(url2+'#path='+suburl)#+'?render-type=list-view')
    time.sleep(2)
    l = w.find_elements_by_xpath('//span[@node-type="chk"]')
    try:
        l[1].click()
    except:
        return False
    time.sleep(1)
    sub = w.find_elements_by_xpath('//a[@data-key="saveToDisk"]')
    sub[0].click()
    confirm = w.find_element_by_id("_disk_id_15")
    confirm.click()
    print "Saved: "+url2
def getUrl(animelist):
    s = requesocks.session()
    s.proxies = {'http':'socks5://127.0.0.1:1080'}
    urllist = []
    for item in animelist:
        res = s.get('http://www.dilidili.com/anime/'+item).content
        soup = BeautifulSoup(res, "lxml")
        try:
            u = soup.find('div', 'download area').a['href']
        except:
            continue
        if re.search('pan.baidu', u):
            urllist.append(u)
            print "Get Url:"+u
            continue
        res = s.get(u).content
        soup = BeautifulSoup(res, "lxml")
        for it in soup('a', href=True):
            if re.search('pan.baidu', it['href']):
                urllist.append(it['href'])
                print "Get url:"+it['href']
                break
    for item in urllist:
        os.system('echo %s >> urllist.txt' % item)
    return urllist

if __name__ == '__main__':
    usrn = u'cotton_高无'
    pswd = ''
    animelist = ['tzjzsrcld','reclks','bygyjcz','sxzyystv','wenhao','heihai','wjbanben','yaren','jibanzhe','nzcp','mijia','concreterevolutio2','chaokmacross']
    if os.path.exists('urllist.txt'):
        with open('urllist.txt','rb+') as f:
            urllist = f.read().strip().split('\n')
    else:
        urllist = getUrl(animelist)
    print urllist
    w = login(usrn, pswd)
    for item in urllist:
        saveToDisk(w, item)
    w.close()

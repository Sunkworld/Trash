#!/usr/local/bin/python
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
#reload(sys)
sys.path.append('..')
sys.path.append('/Applications/script/')
#sys.setdefaultencoding('utf-8')
from funcs import functions
wantedList = ['田中君总是如此慵懒', 'Re：从零开始的异世界生活', '薄樱鬼御伽草子', '双星之阴阳师', '文豪野犬', '黑骸', '我叫坂本我最屌', '亚人', '羁绊者', '逆转裁判', '迷家', '超人幻想 第二季', '超时空要塞 Macross Delta']

def getAnimeList():
    s = requesocks.session()
    s.proxies = {'http':'socks5://127.0.0.1:1080'}
    animelist = {}
    r = s.get('http://www.dilidili.com')
    soup = BeautifulSoup(r.content)
    for item in soup('a', href=True):
        if re.search('dilidili.com/anime', item['href']) and item.string:
            animelist[item.string] = item['href']
    return animelist
    
#animelist = ['tzjzsrcld','reclks','bygyjcz','sxzyystv','wenhao','heihai','wjbanben','yaren','jibanzhe','nzcp','mijia','concreterevolutio2','chaokmacross']
def login(usrn, pswd):
    w = webdriver.PhantomJS()
    w.set_window_size(1124, 850)
    s = requests.Session()
    url = 'http://pan.baidu.com'
    w.get(url)
    w.delete_all_cookies()
    s.get(url)
    if os.path.exists('cook'):
        with open('cook','rb+') as f:
            w.add_cookie(json.load(f)[1])
    else:
        w.add_cookie({'name':'BAIDUID', 'value':s.cookies.get_dict()['BAIDUID'], 'domain':''})
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
            print capt
            a = w.find_element_by_xpath('//input[@type="submit"]')
            a.click()
        print "Login succeeded."
        with open('cook', 'wb+') as f:
            f.write(json.dumps(w.get_cookies()))
    return w
def saveToDisk(w, index, url2):
    global wantedList
    try:
        w.get(url2)
        w.refresh()
        suburl = re.search('typicalPath":"(.*?)"', w.page_source).group(1).replace('\\/','%252F')
    except:
        print "Link for %s is lost." % wantedList[index]
        return False
    w.get(url2+'#path='+suburl)#+'?render-type=list-view')
    time.sleep(2)
    l = w.find_elements_by_xpath('//span[@node-type="chk"]')
    try:
        l[1].click()
    except:
        print "No resource for %s" % wantedList[index]
        return False
    sub = w.find_elements_by_xpath('//a[@data-key="saveToDisk"]')
    sub[0].click()
    confirm = w.find_element_by_id("_disk_id_15")
    confirm.click()
    print "Saved: " + wantedList[index]
def getUrl(animelist):
    s = requesocks.session()
    s.proxies = {'http':'socks5://127.0.0.1:1080'}
    urllist = []
    for item in animelist:
        res = s.get(item).content
        soup = BeautifulSoup(res, "lxml")

        try:
            u = soup.find('div', 'download area').a['href']
        except:
            urllist.append('')
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
    if os.path.exists('urllist.txt'):
        with open('urllist.txt','rb+') as f:
            urllist = f.read().strip().split('\n')
    else:
        indexAnime = getAnimeList()
        animelist = []
        for item in wantedList:
            try:
                animelist.append(indexAnime[item.decode('utf-8')])
            except:
                print "No such anime as %s" % item.decode('utf-8')
        urllist = getUrl(animelist)
#    print urllist
    w = login(usrn, pswd)
    for i in range(len(urllist)):
        saveToDisk(w, i, urllist[i])
    w.close()

#!/usr/local/bin/python
# coding: utf-8
import requests
import requesocks
import os
import re
import Queue
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
import sys
import argparse
from threading import Thread
#reload(sys)
sys.path.append('..')
sys.path.append('/Applications/script/')
#sys.setdefaultencoding('utf-8')
from funcs import functions
wantedList = ['Re：从零开始的异世界生活', '薄樱鬼御伽草子', '双星之阴阳师', '文豪野犬', '黑色残骸', '我叫坂本我最屌', '亚人', '羁绊者', '逆转裁判', '迷家', '超人幻想 第二季', '超时空要塞Δ Macross Delta', '甲铁城的卡巴内瑞无删减版']
urll = {}
watched = {}
def getAnimeList():
    s = requesocks.session()
    s.proxies = {'http':'socks5://127.0.0.1:1080'}
    animelist = {}
    url = 'http://www.dilidili.com'
    animeurl = url + '/anime/'
    dililist = []
    dililist.append(animeurl+'2000xq')
    dililist.append(animeurl+'2010xq')
    for i in range(2010,2017):
        dililist.append(animeurl + str(i))
    for l in dililist:
        r = s.get(l)
        soup = BeautifulSoup(r.content)
        for item in soup('a', href=re.compile('/anime/(.*?)')):
            if item.string and not re.search('dili',item['href']):
                animelist[item.string] = url+item['href']
                print item.string, url+item['href']
        print 'Get:'+l
    with open('animelist.txt', 'wb+') as f:
        json.dump(animelist, f)
    return animelist
    
def login(usrn, pswd):
    global w
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
        sc = s.cookies.get_dict()['BAIDUID']
        print sc
        c = {u'domain': u'.baidu.com', u'secure': False, u'value': u'%s' % sc, u'expiry': 1491806183.590584, u'path': u'/', u'httpOnly': False, u'name': u'BAIDUID'}
        w.add_cookie(c)#({'name':'BAIDUID', 'value':s.cookies.get_dict()['BAIDUID'], 'domain':''})
        w.get(url)
        time.sleep(5)
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
def saveToDisk(name, url):
    global w
    global watched
#    name = name.encode('utf-8')
    w.get(url)
    w.refresh()
    try:
        re.search('typicalPath":"(.*?)"', w.page_source).group(1).replace('\\/','%252F')

    except Exception, e:
        print "Link for %s is lost." % name.encode('utf-8')
        return False
    
    if not args.download:
        try:
            while not re.search('mp4', w.page_source):
                w.find_element_by_xpath('//span[@class="name-text-wrapper"]/span').click()
                time.sleep(1)
        except:
            print "No resource for %s" % name.encode('utf-8')
            return False

    soup = BeautifulSoup(w.page_source.encode('utf-8'))
    tmp = [0, 0]
    if not args.download:
        title = soup.find_all('span','name-text-wrapper')#
#        if len(title) < 2:
#            print "No resource for %s" % name.encode('utf-8')
#            return False
        for i in range(len(title)):
            try:
                c = int(re.search('[^\d]*(\d*).*\.', title[i].span['title']).group(1))
            except:
                c = 0
            if c > tmp[0]:
                tmp[0] = c
                tmp[1] = i
            
        if not tmp[0] > int(watched[name]):
            watched[name] = str(tmp[0])
#        print "New episode of %s has yet to be released" % name
            return True
        watched[name] = str(tmp[0])
    l = w.find_elements_by_xpath('//span[@node-type="chk"]')
    l[1+tmp[1]].click()
    
    sub = w.find_elements_by_xpath('//a[@data-key="saveToDisk"]')
    sub[0].click()
    if not args.download:
        time.sleep(1)
        try:
            d = w.find_element_by_xpath('//span[@node-path="dilidili"]')
            d.click()
            time.sleep(1)
        except:
            new = w.find_element_by_id("_disk_id_16")
            new.click()
            time.sleep(1)
            p = w.find_elements_by_xpath('//input')[-1]
            p.clear()
            p.send_keys('dilidili')
            p = w.find_elements_by_xpath('//span[@class="sure _disk_id_18"]')[-1]
            p.click()
        try:
            h = w.find_element_by_xpath('//span[@node-path="%s"]' % name)
            h.click()
        except:
            new = w.find_element_by_id("_disk_id_16")
            new.click()
            time.sleep(1)
            p = w.find_elements_by_xpath('//input')[-1]
            p.clear()
            p.send_keys(name)
            p = w.find_elements_by_xpath('//span[@class="sure _disk_id_18"]')[-1]
            p.click()

#    print 2
    time.sleep(1)
#    w.quit()
    confirm = w.find_element_by_id("_disk_id_15")
    confirm.click()
    print "Saved: " + name.encode('utf-8'),
    try:
        print ", episode " + str(tmp[0])
    except:
        print '\n'
def getUrl(animelist):
    global urll
    s = requesocks.session()
    s.proxies = {'http':'socks5://127.0.0.1:1080'}
    for i in range(0, len(animelist.keys())):
        print animelist.values()[i]
        res = s.get(animelist.values()[i])
        soup = BeautifulSoup(res.content, "lxml")
        try:
            u = soup.find('li', 'list_xz').a['href']
        except:
            try:
                u = soup.find('div', 'download').a['href']
            except:
                print "Error"
                urll[animelist.keys()[i]] = ''
                continue
        if re.search('pan.baidu', u):
            urll[animelist.keys()[i]] = u
            print "Get Url:"+u
            continue
        elif not re.search('thread', u):
            urll[animelist.keys()[i]] = ''
            continue
        while True:
            try:
                res = s.get(u).content
                break
            except:
                print "Network Error"
                time.sleep(10)
        soup = BeautifulSoup(res, "lxml")
        for it in soup('a', href=True):
            if re.search('pan.baidu', it['href']):
                urll[animelist.keys()[i]] = it['href']
                print "Get url:"+it['href']
                break
#        print urll
def getAnimeUrl():
    que = Queue.Queue()
    for item in list:
        que.put({item:list[item]})
    '''
    ll = []
    for i in range(10):
        ll.append({})
    for i in range(0, 10):
        print i
        for j in range(100*i, min(100*i+100, len(list))):
            ll[i][list.keys()[j]] = list.values()[j]
    threads = []
    '''
    threads = []
    def worker():
        while not que.empty():
            getUrl(que.get())
    for i in range(10):
        threads.append(Thread(target = worker))
        threads[i].start()
    for i in range(10):
        threads[i].join()
#    urllist = getUrl(list)
    with open('urll.txt','wb+') as f:
        json.dump(urll, f)
    return urll
    
def saveSpecified():
    global w
    tmplist = {}
    for k,v in urll.iteritems():
        if re.search(args.download, k.encode('utf-8')):
            tmplist[k] = v
    if not tmplist:
        print "No anime as %s" % args.download
        return False
    elif len(tmplist.keys()) > 1:
        print "There are several animes of the name you search."
        for i in range(len(tmplist.keys())):
            print str(i) + ': ' + tmplist.keys()[i]
        num = raw_input("Which one do you mean?")
        try:
            num = int(num)
            saveToDisk(tmplist.keys()[num], tmplist.values()[num])
        except:
            print "Wrong Input"
            return False
    else:
        saveToDisk(tmplist.keys()[0], tmplist.values()[0])

def autoSave():
    global watched
    while True:
        if os.path.exists('watched.txt'):
            with open('watched.txt') as f:
                watched = json.load(f)
        for item in wantedList:
            if not watched.has_key(item.decode('utf-8')):
                watched[item.decode('utf-8')] = '0'
        for item in wantedList:
            item = item.decode('utf-8')
            saveToDisk(item, urll[item])
        with open('watched.txt','wb+') as f:
            json.dump(watched, f)
        time.sleep(100000)
        
if __name__ == '__main__':
    usrn = u'cotton_高无'
    pswd = ''
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--search', help='search dilidili for animes')
    p.add_argument('-d', '--download', help='save to my disk')
    p.add_argument('-u', '--update', action='store_true', help='update the disk urls')
    args = p.parse_args()
    if os.path.exists('urll.txt') and not args.update:
        with open('urll.txt','rb+') as f:
            urll = json.load(f)
    else:
        if os.path.exists('animelist.txt'):
            with open('animelist.txt','rb+') as f:
                list = json.load(f)
        else:
            list = getAnimeList()
        urll = getAnimeUrl()
    if args.search:
        count = 0
        for k,v in urll.iteritems():
            if re.search(args.search, k.encode('utf-8')):
                print k,v
                count += 1
        if not count:
            print "There is no anime as %s" % args.download
    else:
        w = webdriver.PhantomJS()
        w = login(usrn, pswd)
        if args.download:
            saveSpecified()
        else:
            autoSave()
        w.quit()

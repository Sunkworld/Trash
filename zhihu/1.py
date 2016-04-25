#!/usr/local/bin/python
# coding: utf-8
import requests
import re
import os
import math
import json
import time
import Queue
from bs4 import BeautifulSoup as bs
from threading import Thread
import sys
sys.path.append('..')
from funcs import functions
reload(sys)
sys.setdefaultencoding('UTF-8')
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

indexUrl ='https://www.zhihu.com'
questionUrl = indexUrl + '/question/'
logUrl = questionUrl + '{}/log'
answerListUrl = indexUrl + '/node/QuestionAnswerListV2'
totalAnswer = 0
anonyAnswer = 0
totalQuestion = 0
anonyQuestion = 0
infoOrder = ('userurl', 'asknum', 'answernum', 'articlenum', 'collection', 'pubedit', 'upvoted', 'thanked', 'avervoted', 'follows', 'follower', 'gender', 'issina', 'isbio', 'isprofile', 'isavatar', 'islocation', 'isfield', 'iseducation', 'isvocation', 'zhuanlan', 'topic', 'viewed')
def login():
    s = requests.session()
    with open('cookiefile') as f:
        cookie = json.load(f)
    s.cookies.update(cookie)
    return s
def getUserInfo(usrid):
    userUrl = indexUrl + '/people/' + usrid
    list = {}
    list['userurl'] = userUrl
    while True:
        try:
            res = s.get(userUrl)
            soup = bs(res.content)
            tmp = soup.find('div','profile-navbar clearfix')('span')
            break
        except:
            print "Error in getUserinfo"
            time.sleep(5)
    list['asknum'] = tmp[1].string
    list['answernum'] = tmp[2].string
    list['articlenum'] = tmp[3].string
    list['collection'] = tmp[4].string
    list['pubedit'] = tmp[5].string
    list['upvoted'] = soup.find('span', 'zm-profile-header-user-agree').strong.string
    list['thanked'] = soup.find('span', 'zm-profile-header-user-thanks').strong.string
    if list['answernum'] != '0':
        list['avervoted'] = str(int(list['upvoted'])/int(list['answernum']))
    else:
        list['avervoted'] = '0'
    list['follows'] = soup.find('div','zm-profile-side-following zg-clear')('strong')[0].string
    list['follower'] = soup.find('div','zm-profile-side-following zg-clear')('strong')[1].string
    try:
        if soup.find('span','item gender').i['class'][1]=='icon-profile-male':
            list['gender'] = 'Male'
        else:
            list['gender'] = 'Female'
    except:
        list['gender'] = 'unset'
    if soup.find('a','zm-profile-header-user-weibo'):
        list['issina'] = '1'
    else:
        list['issina'] = '0'
    if soup.find('span','bio'):
        list['isbio'] = '1'
    else:
        list['isbio'] = '0'
    if soup.find(class_='zm-profile-header-description'):
        list['isprofile'] = '1'
    else:
        list['isprofile'] = '0'
    if soup.find('img', 'Avatar--l')['src'] == 'https://pic1.zhimg.com/da8e974dc_l.jpg':
        list['isavatar'] = '0'
    else:
        list['isavatar'] = '1'
    if soup.find('span','location item'):
        list['islocation'] = '1'
    else:
        list['islocation'] = '0'
    if soup.find('span', 'business item'):
        list['isfield'] = '1'
    else:
        list['isfield'] = '0'
    if soup.find('span', 'education item'):
        list['iseducation'] = '1'
    else:
        list['iseducation'] = '0'
    if soup.find('span', 'employment item'):
        list['isvocation'] = '1'
    else:
        list['isvocation'] = '0'
    sidebar = soup('div', 'zm-profile-side-section')
    try:
        list['zhuanlan'] = re.search('(\d*)', sidebar[0].strong.string).group(1)
        list['topic'] = re.search('(\d*)', sidebar[1].strong.string).group(1)
    except:
        list['topic'] = re.search('(\d*)', sidebar[0].strong.string).group(1)
    list['viewed'] = soup('div','zm-side-section-inner')[-1].strong.string
#    print list
    msg = ""
    for item in infoOrder:
        msg += item
        msg += ':'
        msg += list[str(item)]
        msg += '; '
    return msg
    
    
class Question:
    def __init__(self, qn):
        self.qn = qn
        self.url = questionUrl + qn
        self.exist = 1
        self.logUrl = logUrl.format(self.qn)
        if not os.path.exists(self.qn):
            if re.search('error', s.get(self.url).content):
                self.exist = 0
                return
            self.getAddDate()
            os.mkdir(self.qn)
            with open(self.qn + '/static.txt','wb+') as f:
                f.write(self.addDate + '\n' + self.asker)
        else:
            with open(self.qn + '/static.txt') as f:
                tmp = f.read().strip()
                self.addDate = tmp.split('\n')[0]
                self.asker = tmp.split('\n')[1]
        
    def check(self):
        global totalAnswer
        self.qres = s.get(self.url)
        if re.search('error', self.qres.content):
            self.exist = 0
            return False
        try:
            self.answerNum = int(re.search('data-num="(.*?)"', self.qres.content).group(1))
        except:
            self.answerNum = 0
        time.sleep(0.1)
        self.askerInfo = getUserInfo(self.asker)
        time.sleep(0.1)
        totalAnswer += self.answerNum
        self.editDate = self.getEditDate()
        time.sleep(0.1)
        self.answerList = self.getAnswerList()

        
    def getAddDate(self):
        global anonyQuestion
        res = s.get(self.logUrl)
        start = re.findall('logitem-(\d*?)\"', res.content)[-1]
        asker = re.findall('href="/people/(.*?)"', res.content)[-1]
        date = re.findall('datetime="(.*?)"', res.content)[-1]
        offset = 20
        while True:
            data = {'start': start,
                    '_xsrf': _xsrf,
                    'offset': offset}
            res = s.post(self.logUrl, data)
            if res.json()['msg'][0]:
                start = re.findall('logitem-(\d*?)"', res.json()['msg'][-1])[-1]
                try:
                    asker = re.findall('href="/people/(.*?)"', res.json()['msg'][-1])[-1]
                except:
                    asker = "Anonymous"
                    anonyQuestion += 1
                date = re.findall('datetime="(.*?)"', res.json()['msg'][-1])[-1]
                offset += 20
            else:
                break
        self.addDate = date
        self.asker = asker

    def getEditDate(self):
        while True:
            try:
                res = s.get(self.logUrl)
                date = re.findall('datetime="(.*?)"', res.content)[0]
                break
            except:
                time.sleep(10)
        return date

    def getAnswerList(self):
        global anonyAnswer
        offset = 20
        list = []
        for i in range(int(math.ceil(self.answerNum/20.0))):
            data = {'sort': 'created',
                    'page': i+1}
            res = s.get(self.url, params=data)
            soup = bs(res.content)
            tmp = soup('a', class_=re.compile('answer-date-link'))

            for item in tmp:
                answerUrl =item['href']
                answerId = answerUrl.split('/')[-1]
                lastEdit = re.search('(.*?) (.*)', item.string).group(2)
                upvote = item.find_previous('span','count').string
                t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                try:
                    answerer = item.find_previous('a','author-link')['href'].split('/')[-1]
                    answerInfo = getUserInfo(answerer)
                except:
                    answerer = "Anonymous"
                    answerInfo = " "
                    anonyAnswer += 1
                with open(self.qn + '/' + answerId + '.csv', 'ab+') as f:
                    f.write(upvote + ',' + t + ',' + lastEdit + ',' + self.addDate + ',' + indexUrl + answerUrl + ',' + self.askerInfo + ',' + answerInfo + '\n')
                print item['href']
        '''
        while offset < self.answerNum:
            print offset
            data = {'method': 'next',
                    'params': json.dumps({"url_token": int(self.qn),
                               "pagesize": 20,
                               "offset": offset}),
                    '_xsrf': _xsrf}
            res = s.post(answerListUrl, data)
            for item in res.json()['msg']:
                list.append(re.search('data-entry-url="(.*?)"', item).group(1))
            offset += 20
            print len(list)
        '''
def getList():
    qlist = []
    with open('qlist.txt') as f:
        qlist = f.read().strip().split('\n')
    for item in qlist:
        soup = bs(s.get(questionUrl + item).content)
        if soup('div','error'):
            qlist.remove(item)
        else:
            print item
    while len(qlist) < 1000:
        res = s.get('https://www.zhihu.com/topic/19776749/newest')
        soup = bs(res.content)
        for item in soup('a', 'question_link'):
            id = item['href'].split('/')[-1]
            if id not in qlist:
                soup = bs(s.get(questionUrl + id).content)
                if not soup('div', 'error'):
                    qlist.append(id)
            else:
                time.sleep(10)
                print '哼'
                break
        print len(qlist)
        time.sleep(10)
    with open('qlist.txt','wb+') as f:
        for item in qlist:
            f.write(item + '\n')
    
if __name__ == '__main__':
    functions.send('RT', 'Script started')
    s = login()
    soup = bs(s.get(indexUrl).content)
    _xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
    if os.path.exists('qlist.txt'):
        with open('qlist.txt') as f:
            qlist = f.read().strip().split('\n')
    else:
        qlist = getList()
    que = Queue.Queue()
    q = []
    def worker():
        while not que.empty():
            item = que.get()
#            print item
            tmp = Question(item)
            if tmp.exist:
                q.append(tmp)
            else:
                print item + " is deleted"
                qlist.remove(item)
#            print len(q)
    '''        
    for item in qlist:
        q.append(Question(item))
    for item in qlist:
        if not os.path.exists(item):
            print "Dismissed: "+ item
    '''

    for item in qlist:
        que.put(item)
    threads = []
    for i in range(10):
        threads.append(Thread(target = worker))
        threads[i].start()
    for i in range(10):
        threads[i].join()

    def worker():
        while not que.empty():
            item = que.get()
            tmp = item.check()
            if not item.exist:
                print item + " is deleted"
                q.remove(item)
                qlist.remove(item.qn)
            else:
                print "Checked: " + item.qn
            time.sleep(0.1)
                
    while True:
        for item in q:
            que.put(item)
        threads = []
        time.sleep(1)
        for i in range(5):
            print i
            time.sleep(1)
            threads.append(Thread(target = worker))
            threads[i].start()
        for i in range(5):
            threads[i].join()
        print "All questions checked"
        with open('qlist.txt','wb+') as f:
            for item in qlist:
                f.write(item + '\n')
        functions.send('RT', 'Script completed')
        time.sleep(100000)

#    q = Question('22097398')
#    q.check()
    

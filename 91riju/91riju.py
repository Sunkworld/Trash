#!/usr/local/bin/python
import requests
import re
import Queue
import json
import os
from threading import Thread
from bs4 import BeautifulSoup as bs
list = {}

def geturl():
    global list
    que = Queue.Queue()
    pageurl = 'http://www.91riju.com/rijuxiazai/page/{}/'
    if not os.path.exists('91riju.txt'):
        for i in range(65):
            cur_url = pageurl.format(i+1)
            soup = bs(requests.get(cur_url).content)
            for item in soup('a', itemprop='url', rel='bookmark'):
                name = item.string.split('  ')[0]
                que.put(name)
                list[name] = item['href']
                print "Page %s gotten." % str(i+1)
        with open('91riju.txt', 'wb+') as f:
            json.dump(list, f)
    else:
        with open('91riju.txt', 'rb+') as f:
            list = json.load(f)
    threads = []
    def worker():
        while not que.empty():
            tmp = que.get()
            getpanurl(tmp, list[tmp])
    for i in range(10):
        threads.append(Thread(target = worker))
        threads[i].start()
    for i in range(10):
        threads[i].join()
    with open('91rijulist.txt', 'wb+') as f:
        json.dump(list, f)
#   getpanurl()
def getpanurl(name, url):
    r = requests.get(url).content
    panurl = ''
    try:
        c = re.search('"http://pan.baidu.com/s/(.*?)"', r).group(1)
        panurl = 'http://pan.baidu.com/s/' + c
    except:
        pass
    if panurl:
        list[name] = panurl
        print name
    
if __name__ == '__main__':
    geturl()

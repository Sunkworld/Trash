#!/usr/local/bin/python
# coding: utf-8
import requests
import re
import Queue
import time
from threading import Thread
list = []
with open('cookiefile') as f:
    cookie = f.read().strip()
s = requests.session()
s.headers.update({'cookie':cookie})
url = 'http://tieba.baidu.com/i/99594746/my_reply?&pn={}'
threads = []
n = 0
que = Queue.Queue()
strg = '喜之郎菠萝味'
def search_for(purl):
    r = requests.get(purl).content
    if re.search(strg, r):
        print purl
def worker():
    global n
    while not que.empty():
        search_for(que.get())
        n += 1
        if n%10==0:
            print n/10,
def get_list():
    for i in range(1, 31):
        cont = s.get(url.format(i)).content
        patten = re.findall('/p/(\d+)\?pid=(\d+)', cont)
        if re.search(strg, cont):
            print url.format(i)
            continue
        for item in patten:
            cur_url = 'http://tieba.baidu.com/p/'+item[0]+'?pid='+item[1]
            if cur_url in list:
                continue
            else:
                que.put(cur_url)
                list.append(cur_url)
threads.append(Thread(target=get_list))
threads[0].start()
time.sleep(1)
for i in range(10):
    threads.append(Thread(target=worker))
    threads[i+1].start()
for item in threads:
    item.join()

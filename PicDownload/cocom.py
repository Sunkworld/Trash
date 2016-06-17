#!/usr/local/bin/python
import requesocks
import re
import Queue
que = Queue.Queue()
from threading import Thread
from bs4 import BeautifulSoup as bs
sess = requesocks.session()
#sess.proxies = {'http':'socks5://127.0.0.1:1080'}
def down_pic(num):
    url ='http://coco-m.co.kr/product/detail.html?product_no={}'
    res = sess.get(url.format(num)).content
    mainurl = 'http://coco-m.co.kr'
    soup = bs(res)
    cont = soup.find('div','cont')
    try:
        items = cont.find_all('img')
    except:
        print num,
        print ' Unfound.'
        return False
    for i in range(1, len(items)-1):
        s = items[i]['src'].split('/')[-1]
        if items[i]['src'][0]=='/':
            u = mainurl + items[i]['src']
        else:
            u = items[i]['src']
        try:
            with open(s, 'wb+') as f:
                f.write(sess.get(u).content)
        except:
            print num,
            print ' Something Wrong'
            continue
    print num

def run():
    global que
    threads = []
    def worker():
        while not que.empty():
            down_pic(que.get())
    for i in range(10):
        threads.append(Thread(target = worker))
        threads[i].start()
    for i in range(10):
        threads[i].join()

if __name__ == '__main__':
    for i in range(1492, 1810):
        que.put(i)
    run()

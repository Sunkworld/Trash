#!/usr/local/bin/python
import requests
import re
import Queue
que = Queue.Queue()
from threading import Thread
def down_pic(num):
    url ='http://www.mintique.co.kr/product/detail.html?product_no={}'
    res = requests.get(url.format(num)).content
    items = re.findall(r'src="/web/upload/(.*?).jpg">', res)
    for i in range(0, len(items)-1):
        s = items[i].replace('/', '_')
        with open(s + '.jpg', 'wb+') as f:
            f.write(requests.get('http://www.mintique.co.kr/web/upload/'+items[i]+'.jpg').content)
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
    for i in range(1000, 1140):
        que.put(i)
    run()

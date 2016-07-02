#!/usr/local/bin/python
import requests
import re
url = 'http://email.91dizhi.at.gmail.com.9h1.space/video.php?category=rf&page={}'
list = {}
def getList():
    global list
    for i in range(1, 80):
        print i
        cur_url = url.format(i)
        r = requests.get(cur_url).content
        for item in re.findall('view_video.php\?(.*?)"(.*?)Favorites:</span> (.*?)<br',r,re.S):
            list['http://email.91dizhi.at.gmail.com.9h1.space/view_video.php?'+item[0]] = int(item[2])
    l = sorted(list.items(), key=lambda d:d[1], reverse=True)
    for item in l:
        print item[1], item[0]
    exit(0)
    for k,v in list.iteritems():
        print k,v

if __name__ == '__main__':
    getList()

#coding:utf-8
import requests
import re
import sys
import time
from bs4 import BeautifulSoup
sys.path.append('..')
from funcs import functions
def main():
    boardlist = ['Apple']
    s = requests.session()
    soup = BeautifulSoup(s.get('http://www.bdwm.net/bbs/main0.php').content.decode('gbk'), 'lxml')
    msg = "全站十大热门话题\n"
    for item in soup.find('span',id='DefaultTopTen').find_all('a'):
        if re.search('bbsdoc',item.get('href')):
                msg += '['
                msg += item.string.encode('utf-8')
                msg += ']'
        else:
                msg += item.string.encode('utf-8')
                msg += '\n'
    for board in boardlist:
        msg += '\n%s版：\n' % board
        soup = BeautifulSoup(s.get('http://www.bdwm.net/bbs/bbstop2.php?board=%s' % board).content.decode('gbk'), 'lxml')
        l = soup.find('table','body')('tr')
        for j in range(len(l)-10, len(l))[::-1]:
            item = l[j]
            for i in range(0, len(item('td')))[::-1]:
                if item('td')[i].a:
                    msg += item('td')[i].string.encode('utf-8')
                    msg += '   '
                    msg += item('td')[i+1].string.encode('utf-8')
                    msg += '\n'
                    break

    return msg
if __name__ == '__main__':
    while True:
        t = int(time.strftime('%H',time.localtime(time.time())))
        if t>7:
            functions.send(main(),'未名bbs')
        time.sleep(7200)


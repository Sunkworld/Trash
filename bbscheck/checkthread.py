import requests
import os
from bs4 import BeautifulSoup
from time import sleep
import time
count = 0
def chk(board, threadid):
    global count
    params = {}
    params['board'] = board
    params['threadid'] = threadid
    s = requests.session()
    try:
        r = s.get('https://www.bdwm.net/bbs/bbstcon.php', params=params)
    except:
        print "Network Error"
        sleep(30)
    soup = BeautifulSoup(r.content)
    l = soup('pre')
    if count == 0:
        for item in l:
            print item.get_text()
    elif count < len(l):
        print "New reply at %s" % time.localtime(time.time())
        print l[len(l)-1].get_text()
        os.system("""osascript -e 'display notification "There is new reply" with title "bdwm bbs"'""")
    count = len(l)
if __name__ == '__main__':
    while True:
        chk('SecretGarden','15728167')
        sleep(10)

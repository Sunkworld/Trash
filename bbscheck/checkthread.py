import requests
import os
from bs4 import BeautifulSoup
from time import sleep
import time
import sys
sys.path.append('..')
from funcs import functions
count = 0
t = 0
def chk(s, board, threadid):
    global count
    global t
    params = {}
    params['board'] = board
    params['threadid'] = threadid
    try:
        r = s.get('https://www.bdwm.net/bbs/bbstcon.php', params=params)
    except:
        print "Network Error"
        sleep(30)
    soup = BeautifulSoup(r.content)
    l = soup('pre')
    if count == 0:
        msg = ""
        for item in l:
            msg += item.get_text()
        functions.send(msg,'Thread')
    elif count < len(l):
        msg = ""
        msg += l[len(l)-1].get_text()
        functions.send(msg,'New reply')
#        os.system("""osascript -e 'display notification "There is new reply" with title "bdwm bbs"'""")
    count = len(l)
if __name__ == '__main__':
    s = requests.session()
    s.headers.update({'cookie':'sid=251b5dfe5b; userlogin=yes; id2=Sunkworld; code2=%241%24mgPK%24xexbYjB'})
    while True:
        chk(s,'SecretGarden','15728167')
        sleep(30)

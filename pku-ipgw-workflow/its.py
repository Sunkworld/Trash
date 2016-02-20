# coding:utf-8
import urllib,urllib2
query = '{query}'

def connect_free():
    value1 = {'cmd':'open', 'type':'free', 'fr':'0', 'sid':'873'}
    res = opener.open('https://its.pku.edu.cn/netportal/PKUIPGW', urllib.urlencode(value1))

def connect_fee():
    value2 = {'cmd':'open', 'type':'fee', 'fr':'0', 'sid':'855'}
    res = opener.open('https://its.pku.edu.cn/netportal/PKUIPGW', urllib.urlencode(value2))

def disconnect_all():
    value3 = {'cmd':'close', 'type':'allconn', 'fr':'0', 'sid':'734'}
    opener.open('https://its.pku.edu.cn/netportal/PKUIPGW', urllib.urlencode(value3))


opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

f = open('/Applications/setting.txt')
usrn = f.readline().replace('\n','')
pswd = f.readline().replace('\n','')
f.close()
str = '|;kiDrqvfi7d$v0p5Fg72Vwbv2;|'
url = 'https://its.pku.edu.cn/cas/login'
opener.open(url)
value = {'username1':usrn, 'password':pswd, 'pwd_t':'密码', 'fwrd':'noopen', 'username':usrn+str+pswd+str+'15'}
opener.open(url, urllib.urlencode(value))

if query == '1':
    connect_free()
elif query == '2':
    connect_fee()
elif query == '3':
    disconnect_all()
quit()

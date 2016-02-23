# coding: utf-8

import re,urllib,urllib2,time,os

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
opener.open('https://iaaa.pku.edu.cn/iaaa/oauthlogin.do')
with open(os.path.expanduser('~')+'/.its') as f:
    fr = f.read().split()
    usrn = fr[0]
    pswd = fr[1]
data = {'appid':'syllabus', 'userName':'%s' % usrn, 'password':'%s' % pswd, 'randCode':'验证码', 'smsCode':'短信验证码', 'redirUrl':'http://elective.pku.edu.cn:80/elective2008/agent4Iaaa.jsp/../ssoLogin.do'}
r = opener.open('https://iaaa.pku.edu.cn/iaaa/oauthlogin.do',urllib.urlencode(data)).read()
s = {}
s['token'] = re.search(r'n":"(.*?)"',r).group(1)
s['rand'] = 0.2347834
opener.open('http://elective.pku.edu.cn/elective2008/ssoLogin.do',urllib.urlencode(s)).read()
opener.open('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do',urllib.urlencode(s)).read()

s1 = opener.open('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp?netui_pagesize=electableListGrid%3B20&netui_row=electableListGrid%3B20',urllib.urlencode(s)).read()
#    print s1
ss = re.findall(r'60">22 / (.*?)</', s1)
jishu = 0

while True:
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    opener.open('https://iaaa.pku.edu.cn/iaaa/oauthlogin.do')
    
    r = opener.open('https://iaaa.pku.edu.cn/iaaa/oauthlogin.do',urllib.urlencode(data)).read()
    s = {}
    s['token'] = re.search(r'n":"(.*?)"',r).group(1)
    s['rand'] = 0.234729834
    opener.open('http://elective.pku.edu.cn/elective2008/ssoLogin.do',urllib.urlencode(s)).read()
    opener.open('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do',urllib.urlencode(s)).read()

    s1 = opener.open('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp?netui_pagesize=electableListGrid%3B20&netui_row=electableListGrid%3B20',urllib.urlencode(s)).read()
    ss = re.findall(r'60">22 / (.*?)</', s1)
    t = 0
    jishu += 1
    for item in ss:
        if item!='22':
            os.system("""osascript -e 'display notification "有课能选了！！" with title "hey，傻逼"'""")
            for i in range(1,100):
                os.system('say "There is vacancy in the course you selected"')
            t = 1
    if t == 0:
        print "There is no vacancy. Try time %d." % jishu
        




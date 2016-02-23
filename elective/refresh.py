# coding: utf-8

import re,os,requests,time

t = 0
def notif():
    os.system("""osascript -e 'display notification "有课能选了！！" with title "hey，傻逼"'""")
    for i in range(1,100):
        os.system('say "There is vacancy in the course you selected"')
        t = 1
sess1 = requests.Session()
with open(os.path.expanduser('~')+'/.its') as f:
    fr = f.read().split()
    usrn = fr[0]
    pswd = fr[1]
data = {'appid':'syllabus', 'userName':'%s' % usrn, 'password':'%s' % pswd, 'randCode':'验证码', 'smsCode':'短信验证码', 'redirUrl':'http://elective.pku.edu.cn:80/elective2008/agent4Iaaa.jsp/../ssoLogin.do'}
cont1 = sess1.post('https://iaaa.pku.edu.cn/iaaa/oauthlogin.do', data=data)

p1 = {}
p1['token'] = re.search(r'n":"(.*?)"',cont1.text).group(1)
p1['rand'] = 0.32874243

sess1.get('http://elective.pku.edu.cn/elective2008/ssoLogin.do', params=p1)
s1 = sess1.get('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do')
fl = re.finditer(r'refreshLimit(.*?)\'\',\'(.*?)\',\'(.*?)\',\'(.*?)\'', s1.text)
fl1 = []
fl2 = []
for match in fl:
    if match.group(4) == '28':
        fl1.append({'index':'%s' % match.group(2), 'seq':'%s' % match.group(3)})

        #fl1['%s' % match.group(2)]='%s' % match.group(3)
    elif match.group(4) == '30':
        fl2.append({'index':'%s' % match.group(2), 'seq':'%s' % match.group(3)})

#        fl2['%s' % match.group(2)]='%s' % match.group(3)


        
s1 = sess1.get('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp?netui_pagesize=electableListGrid%3B20&netui_row=electableListGrid%3B20')
fl = re.finditer(r'refreshLimit(.*?)\'\',\'(.*?)\',\'(.*?)\',\'(.*?)\'', s1.text)


for match in fl:
    if match.group(4) == '28':
        fl1.append({'index':'%s' % match.group(2), 'seq':'%s' % match.group(3)})

        #fl1['%s' % match.group(2)]='%s' % match.group(3)
    elif match.group(4) == '30':
        fl2.append({'index':'%s' % match.group(2), 'seq':'%s' % match.group(3)})

#        fl2['%s' % match.group(2)]='%s' % match.group(3)

#print fl1,fl2
jishu = 0
while True:
    t = 0
    jishu += 1
    for i in range(0,len(fl1)):
        sr1 = sess1.get('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/refreshLimit.do', params=fl1[i])
#        print sr1.text
        fi1 = re.search(r'Num>(.*?)</', sr1.text).group(1)
#        print fi1
        time.sleep(5)
        if fi1 != '28':
                notif()


    for i in range(0,len(fl2)):
        sr1 = sess1.get('http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/refreshLimit.do', params=fl2[i])
#        print sr1.text
        fi2 = re.search(r'Num>(.*?)</', sr1.text).group(1)
#        print fi2

        if fi2 != '30':
            notif()
   
        time.sleep(5)
    if t == 0:
        print "There is no vacancy. Try time %d" % jishu


        




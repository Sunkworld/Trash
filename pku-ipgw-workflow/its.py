#!/usr/bin/python
# coding:utf-8
import urllib,re,os,time,subprocess
query = "{query}"
fr_time = ''
fr_desc_en = ''
connections = ''
balance = ''
subprocess.call("ps -ef | grep discon.py | grep -v grep | awk '{print $2}' | xargs kill -9", shell=True)
with open(os.path.expanduser('~')+'/.its') as f:
    fr = f.read().split()
    usrn = fr[0]
    pswd = fr[1]

try:
    if query == '1':
        res = urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=2&operation=connect&timeout=1').read()
    elif query == '2':
        res = urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=1&operation=connect&timeout=1').read()
    elif query == '3':
        res = urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=2&operation=disconnectall&timeout=1').read()
    elif query == '4':
        res = urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=2&operation=disconnectall&timeout=1').read()
        res = urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=2&operation=connect&timeout=1').read()
    elif query == '5':
        res = urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=2&operation=disconnectall&timeout=1').read()
        res = urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=1&operation=connect&timeout=1').read()
    else:
        out = '输入编号有误'
        print out
        quit()
except IOError, e:
    print e
    quit()

dict = {'1': '免费地址连接成功', '2': '收费地址连接成功', '3': '已断开所有连接', '4': '免费地址连接成功', '5': '收费地址连接成功'}
sr = re.search(r'SUCCESS=YES (.)', res)
if sr:
    out = dict[query]
    if sr.group(1)=='S':
        fr_time = str(round(float(re.search(r'TIME=(.*?) ', res).group(1)),1))
        fr_desc_en = re.search(r'FR_DESC_EN=(.*?)hours', res).group(1)
        connections = re.search(r'CONNECTIONS=(.*?) ', res).group(1)
        balance = str(round(float(re.search(r'BALANCE=(.*?) ', res).group(1)),1))
else:
    out = re.search(r'REASON=(.*?) ', res.decode('gbk')).group(1)
    print out
    quit()
print out
if fr_time:
    print '收费时间: '+fr_time+'/'+fr_desc_en+' h, 连接数: '+connections+', 余额:'+balance
if query == '2' and os.path.exists(os.path.expanduser('~/.discon')):
    subprocess.Popen(['/bin/sh',os.path.expanduser('~/.discon.sh')], stdout=subprocess.PIPE)
    quit()


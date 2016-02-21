#!/usr/bin/python
# coding:utf-8
import urllib,re,os,time
query = "{query}"
fr_time = ''
fr_desc_en = ''
connections = ''
balance = ''
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
    else:
        out = '输入编号有误'
        print out
        quit()
except IOError, e:
    print e
    quit()

dict = {'1': '免费地址连接成功', '2': '收费地址连接成功', '3': '已断开所有连接'}
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
if fr_time:
    print '收费时间: '+fr_time+'/'+fr_desc_en+' h, 连接数: '+connections+', 余额:'+balance




#!/usr/bin/python
# coding: utf-8
import urllib,os,time,re
os.system('touch ~/bukaixin')

with open(os.path.expanduser('~')+'/.its') as f:
    fr = f.read().split()
    usrn = fr[0]
    pswd = fr[1]
with open(os.path.expanduser('~')+'/.discon') as f1:
    discon = int(f1.read().strip())
if discon:
    time.sleep(discon)
    res = urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=2&operation=connect&timeout=1').read()
    out = '已自动断开收费地址'
    fr_time = str(round(float(re.search(r'TIME=(.*?) ', res).group(1)),1))
    fr_desc_en = re.search(r'FR_DESC_EN=(.*?)hours', res).group(1)
    connections = re.search(r'CONNECTIONS=(.*?) ', res).group(1)
    balance = str(round(float(re.search(r'BALANCE=(.*?) ', res).group(1)),1))
    os.system("""osascript -e 'display notification "已自动断开收费地址\n收费时间: %s/%s h, 连接数: %s, 余额: %s" with title "Alfred 2"'""" % (fr_time, fr_desc_en, connections, balance))
else:
    quit() 

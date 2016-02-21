#!/usr/bin/python
# coding:utf-8
import urllib
query = "{query}"

with open('/Applications/setting.txt') as f:
    usrn = f.readline().strip()
    pswd = f.readline().strip()

if query == '1':
    urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=2&operation=connect&timeout=1')
elif query == '2':
    urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=1&operation=connect&timeout=1')
elif query == '3':
    urllib.urlopen('https://its.pku.edu.cn:5428/ipgatewayofpku?uid='+usrn+'&password='+pswd+'&range=2&operation=disconnectall&timeout=1')

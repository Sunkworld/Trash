#!/usr/local/bin/python
# coding: utf-8

import json, re
with open('91rijulist.txt') as f:
    list = json.load(f)

for item in list:
    tmp = item.split(' ')
    for i in range(len(tmp)):
            if re.search('下载', tmp[i].encode('utf-8')) and i!=0:
                t = ''
                for j in range(i):
                    t += tmp[j]
                break
            else:
                t = item
    print t.encode('utf-8') + ' '.encode('utf-8') + list[item].encode('utf-8')

# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from operator import itemgetter
with open('www.txt') as f:
    a = f.read()
b = {}
a = a.encode('unicode-escape').decode('unicode-escape')

t = 0
for i in range(len(a)):
    if a[i]>u'\u4e00' and a[i]<u'\u9fa5':
        t += 1
        if a[i] in b.keys():
            b[a[i]] += 1
        else:
            b[a[i]] = 1
#        print i

c = sorted(b.iteritems(), key=itemgetter(1), reverse=True)
print "共有%s个中文汉字，出现频率最高的100个如下:\n" % t
for i in range(100):
    print c[i][0], c[i][1]

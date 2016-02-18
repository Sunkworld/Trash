#!/usr/local/bin/python
import urllib
import re

#num = raw_input('Enter the number: ')
def down_pic(num):
    res = urllib.urlopen('http://www.mintique.co.kr/product/detail.html?product_no='+str(num))
    page = res.read()
    items = re.findall(r'src="/web/upload/(.*?).jpg">',page)
    for i in range(0, len(items)-1):
        s = items[i].replace('/','_')
        urllib.urlretrieve('http://www.mintique.co.kr/web/upload/'+items[i]+'.jpg',s+'.jpg')

for i in range(598, 900):
    down_pic(i)
    












#!/usr/bin/env python
#coding:utf-8
import requests
from bs4 import BeautifulSoup as bs
import os
import re
from funcs import functions
from time import sleep
import traceback
class dianping:
    def __init__(self):
        self.eventid = []
        self.s = requests.session()
        self.s.headers.update({'cookie':'_hc.v=1b1a009d-820f-dfe9-ded7-605835769225.1469737748; dper=9cc2ace500df9dad615e4ce9819ab2de3e095ccc9f2c2ed0d69fd988b86c1559; ua=tm_aptx4869; PHOENIX_ID=0a031c95-157d67e8ac8-23fde0; ll=7fd06e815b796be3df069dec7836c3df; likeTips=ignored; __utma=1.830556726.1474808189.1476353905.1476772455.3; __utmc=1; __utmz=1.1474808189.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); switchcityflashtoast=1; download_banner=on; cityid=2; default_ab=index%3AA%3A1; pvhistory=6L+U5ZuePjo8L2V2ZW50L2JlaWppbmcvYzE+OjwxNDc2Nzc0OTQ1MjE3XV9b; m_flash2=1; visitflag=1; isChecked=checked; JSESSIONID=2C230B2D16575FD85E3C08B2E3EA9ECC; aburl=1; cy=2; cye=beijing'})
        self.s.headers.update({'user-agent':'chrome'})
        self.mess = ''
        self.checkedList = []
        self.appliedList = []
    def bawangcan(self):
        self.mess = ''
        self.appliedList = []
        mainUrl = 'http://s.dianping.com/event/beijing/c1'
        eventUrl = 'http://s.dianping.com/event/'
        loadUrl = 'http://s.dianping.com/ajax/json/activity/offline/loadApplyItem'
        saveUrl = 'http://s.dianping.com/ajax/json/activity/offline/saveApplyInfo'
        r = self.s.get(mainUrl).content
        sleep(0.1)
        if not re.search('tm_aptx4869',r):
            functions.send('User Info Outdated','[VPS]Dianping')
        soup = bs(r)
        data = {'offlineActivityId':''}
        data2 = data
        data2['phoneNo'] = '188****0727'
        data2['isShareSina'] = 'false'
        data2['isShareQQ'] = 'false'
        for item in soup.find_all('div','tit'):
            curid = item.a['href'].split('/')[-1]
            if curid in self.checkedList:
                continue
            r = self.s.get(eventUrl+curid).content
            sleep(0.1)
            cursoup = bs(r)
            shopUrl = cursoup.find('span','tenant').a['href']
            r = self.s.get(shopUrl).content
            sleep(0.1)
            cursoup = bs(r)
            info = cursoup.find('div','brief-info').find_all('span','item')
            try:
                ave = int(re.search('\d+',info[1].string).group(0))
                isgood = 1
                for i in range(2,4):
                    rating = float(re.search('\d+',info[i].string).group(0))
                    if rating < 8.5:
                        isgood = 0
                        break
                name = cursoup.find('span','shop').string
                if ave>200 or isgood:
                    data['offlineActivityId'] = curid
                    data2['offlineActivityId'] = curid
                    self.s.post(loadUrl, data)
                    self.s.post(saveUrl, data2)
                    print 'Applied:' + name
                    self.appliedList.append((name, curid, ave))
                else:
#                    print 'Checked:' + name
                    pass

            except:
                self.mess += eventUrl+curid+'\n'
            #    print self.mess
            self.checkedList.append(curid)

        if self.appliedList:
            self.mess += '\nThese are the restaurants applied for you:\n'
            for item in self.appliedList:
                self.mess += u'店名: ' + item[0] + u',    人均:' + str(item[2]) + u',    网址: '+ eventUrl + item[1] + '\n'
        if self.mess:
            self.mess = 'These events are available where no average expense is provided:\n' + self.mess
            functions.send(self.mess,'[VPS]Dianping')

if __name__=='__main__':
    dp = dianping()
    num = 0
    while True:
        try:
            dp.bawangcan()
            num += 1
            print "Checked %s times" % num
            sleep(1000)
        except Exception,e:
            print "Network Error"
            traceback.print_exc()
            sleep(5)

##-------------modified from http://blog.csdn.net/supercooly/article/details/51046561-----------------
from contextlib import closing
import json
import requests

file_name = '1.f4v'
cacheurl = 'http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c&tvId=534057700&vid=7ce54def96d95bff4f8e6fd7cc7323e3&vinfo=1&tm=206&qyid=2e03c831d5c9e27770baba9d01230608&puid=&authKey=f053327d19dd432973c2373078b841aa&um=0&pf=b6c13e26323c537d&thdk=&thdt=&rs=1&k_tag=1&qdv=1&vf=d75c6103f2956f057aace489b10c9f42'

class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s]%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)
        
r = requests.get(cacheurl).json()['data']['vp']['tkl'][0]['vs']
m = (0,0)
for i in range(len(r)):
    if r[i]['bifsz'] > m[0]:
        m = (r[i]['bifsz'], i)
s = r[m[1]]['fs']
list = []
for item in s:
    list.append('http://data.video.qiyi.com/videos'+item['l'])
for url in list:
    with closing(requests.get(requests.get(url).json()['l'], stream=True)) as response:
        chunk_size = 1024 # 单次请求最大值
        content_size = int(response.headers['content-length']) # 内容体总大小
        progress = ProgressBar('file', total=content_size,
                                     unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        with open(file_name, "ab+") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))

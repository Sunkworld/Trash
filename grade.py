#!/usr/local/bin/python
#------------Based on @bsnsk's code------------
import requests
import sys
sys.path.append('..')
from funcs import functions
import re
from time import sleep
import time

class Job:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.url = 'http://dean.pku.edu.cn/student'
        self.s = requests.session()
        self.init_maj_deg_list = {}
        self.add_class(self.gen_list())

    def add_class(self, items):
        for i in items:
            self.init_maj_deg_list[i[2]] = i
    
    def write_file(self, filename, content):
        f = open(filename, "w")
        f.write(content)
        f.close()
        
    def gen_list(self):
        authurl = self.url + '/authenticate.php'
        captchaurl = self.url + '/yanzheng.php?act=init'
        indexurl = self.url + '/student_index.php'
        gradeurl = self.url +'/new_grade.php'
        data = {'sno':self.username,
                'password':self.password,
                'captcha':'',
                'submit':'%B5%C7%C2%BC'}
        while True:
            capt = functions.decaptcha(self.s.get(captchaurl).content)
            capt = re.sub('[^0-9a-zA-Z]', '', capt)
            
            data['captcha'] = capt
            r = self.s.post(authurl, data).content
            try:
                sessid = re.search('parent.location.href="(.*?)"', r).group(1)
                print "Login succeeded."
                break
            except:
                pass
        params = {'PHPSESSIONID':sessid}
        self.s.get(indexurl, params=params)
        res = self.s.get(gradeurl).content
#        self.write_file('1.html', res)
        return self.parse_grades(res)

    def parse_item(self, regex_obj):
        str = regex_obj.group(0)
        str = re.sub(r"(<tr>|.?)<td>([^<]*)</td>", r"\2$", str).strip("$").split("$")
        return str

    def parse_grades(self, grades):
        results = []
        for i in re.finditer(r'<tr>(<td>[^<]*</td>){8}', grades):
            item = self.parse_item(i)
            results.append(item)
        return results

    def check_class(self, cur_list):
        news = []
        for item in cur_list:
            if not self.init_maj_deg_list.has_key(item[2]):
                news.append(item)
        return news
    
    def print_list(self, cur_list):
        print "print list"
        for item in cur_list:
            print self.gen_str(item, "Major")

    def gen_str(self, item, deg_flag="Major"):
        return "[" + deg_flag + " Degree] %s: \t\t\tCredits = %s, Grade = %s, Points = %s\n" % (item[5], item[6], item[3], item[7])

    def deliver(self, news):
        content = ""
        for item in news:
            content += self.gen_str(item, "Major")
        return functions.send(content, "New grade released")

    def run(self):
        count = 0
        while True:
            count += 1
            cur_list = self.gen_list()
#            self.print_list(cur_list)
            news = self.check_class(cur_list)
            if news != []:
                delivered = self.deliver(news)
                if delivered:
                    self.add_class(news)
            print "Round %d ..." % count
            sleep(120)

    
                
if __name__ == '__main__':
    g = Job()
    g.run()
            
    

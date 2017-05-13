import sys
import requests
import time
import threading
from bs4 import BeautifulSoup

def WorkingProxySort(x, y):
    if x.resp < y.resp:
        return -1
    elif x.resp > y.resp:
        return 1
    else:
        return 0

class WorkingProxy:
    def __init__(self, ip, port, type, ssl, resp):
        self.ip = ip
        self.port = port
        self.type = type
        self.ssl = ssl
        self.resp = resp
        self.working = False

    def __repr__(self):
        return repr((self.ip, self.port, self.type, self.ssl, self.resp, self.working))

def get_from_proxynova(wpmgr):
    req = requests.get('http://www.proxynova.com/proxy-server-list/country-bg/')
    page = req.text
    soup = BeautifulSoup(page, 'lxml')

    for row in soup('table')[0].findAll('tr'):
        if len(row)>0:
            fields = row.findAll('td')
            if len(fields)>0:
                if fields[0].span != None:
                    sp = fields[0].findAll('span')
                    ip = ''
                    for s in sp:
                        ip += s.string
                    if fields[1].a != None:
                        port = str(fields[1].a.string).strip()
                    else:
                        port = str(fields[1].string).strip()
                    age = str(fields[2].time.datetime).strip()
                    speed = float(str(fields[3].div['data-value']).strip())
                    wpmgr.add(WorkingProxy(ip, port, 'http', False, 0))

def get_from_xroxy(wpmgr):
    req = requests.get('http://www.xroxy.com/proxy-country-BG.htm')
    page = req.text
    soup = BeautifulSoup(page, 'lxml')

    for row in soup('table')[4].findAll('tr'):
        if len(row)>0:
            fields = row.findAll('td')
            if len(fields)>2:
                ip = str(fields[1].a.text).strip()
                port = str(fields[2].a.string).strip()
                ptype = str(fields[3].a.string).strip().lower()
                if ptype == 'transparent':
                    ptype = 'http'
                ssl = (str(fields[4].a.text).strip().lower() == 'true')
                speed = float(str(fields[6].text).strip())
                rel = float(str(fields[7].text).strip())
                wpmgr.add(WorkingProxy(ip, port, ptype, ssl, 0))

class XroxyThread(threading.Thread):
    def __init__(self, wp):
        threading.Thread.__init__(self)
        self.wp = wp

    def run(self):
        get_from_xroxy(self.wp)
        return

class NovaThread(threading.Thread):
    def __init__(self, wp):
        threading.Thread.__init__(self)
        self.wp = wp

    def run(self):
        get_from_proxynova(self.wp)
        return

class TestThread(threading.Thread):
    def __init__(self, pxy):
        threading.Thread.__init__(self)
        self.pxy = pxy

    def run(self):
        testsites = ['http://www.vbox7.com', 'http://www.zamunda.net']
        proxy = {}
        proxy['http'] = '{0}://{1}:{2}'.format(self.pxy.type, self.pxy.ip, self.pxy.port)
        if self.pxy.ssl:
            proxy['https'] = '{0}://{1}:{2}'.format(self.pxy.type, self.pxy.ip, self.pxy.port)
        t = 0
        cnt = 0
        for site in testsites:
            try:
                s = time.time()
                r = requests.get(site, proxies=proxy, timeout=5)
                e = time.time()
                t = t + e -s
                cnt += 1
            except requests.exceptions.Timeout:
                return
            except Exception:
                return
        self.pxy.resp = t/cnt;
        self.pxy.working = True;
        return

class WorkPx:
    def __init__(self, w):
        self.w = w
        self.__lock = threading.Lock()
    
    def add(self, element):
        self.__lock.acquire()
        self.w.append(element)
        self.__lock.release()        

workingproxy = []

def fnd_proxy_list():
    wrkpxmgr = WorkPx(workingproxy)
    t1 = XroxyThread(wrkpxmgr)
    t2 = NovaThread(wrkpxmgr)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    testthreads = []
    for w in workingproxy:
        t = TestThread(w)
        testthreads.append(t)
        t.start()
    for t in testthreads:
        t.join()
    workingproxy.sort(cmp=WorkingProxySort)

def find_bg_proxy(bgproxy):
    fnd_proxy_list()
    for w in workingproxy:
        if w.working: 
            bgproxy.append((w.ip, w.port, w.type, w.ssl))
            return True
        else:
            print(w)
    return False

def main():
    bgproxy = []
    if find_bg_proxy(bgproxy):
        print('bg proxy details: ip: {0} port: {1} type: {2} sll: {3}'.format(bgproxy[0][0], bgproxy[0][1], bgproxy[0][2], bgproxy[0][3]))
    else:
        print('Cannot find working proxy.')
         
if __name__ == "__main__":
    main();



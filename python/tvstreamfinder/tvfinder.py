import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = "username"
SMTP_PASSWORD = "password"
EMAIL_FROM = "username@yahoo.com"
EMAIL_TO = "username@gmail.com"
EMAIL_SUBJECT = "new bg tv stream"

msg_text = """
Hi Stanislav, 

There is new bg tv stream from {0}.

Best Regards,
sTa (with Python help)
"""
class bgtvfind:
    def __init__(self):
        self.__req = requests.get('http://www.tvonlinestreams.com/?s=bulgaria')
        self.__links = []


    def __parse(self):
        if self.__req.status_code != 200:
            return False
        soup = BeautifulSoup(self.__req.text, 'lxml')
        h2list = soup.find_all('footer')
        for h in h2list:
            if h.time:
                self.__links.append((h.time.get('datetime'), h.a.get('href')))


    def __process_links(self):
        s = ''
        chfname = 'lastbgtvscrap.txt'
        try:
            with open(chfname, 'r') as f:
                s = f.read()
        except Exception:
            pass
        if s != self.__links[0][0]:
            for t, u in self.__links:
                self.__make_m3u(t, u)
            self.__send_email(self.__links[0][0] + ' ' + self.__links[0][1])
            with open(chfname, 'w') as f:
                f.write(self.__links[0][0])


    def __make_m3u(self, t, url):
        print('{0} {1}'.format(t, url))
        fname = t.replace(':', '_').replace('-', '_').replace('+', '_')
        r = requests.get(url)
        if r.status_code != 200:
            return False
        soup = BeautifulSoup(r.text, 'lxml')
        cont = soup.p.text
        with open('tv_' + fname + '.m3u', 'wb') as f:
            f.write(cont.encode('utf-8'))


    def __send_email(self, t):
        mtext = msg_text.format(t)
        msg = MIMEText(mtext)
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_FROM 
        msg['To'] = EMAIL_TO
        debuglevel = False
        mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mail.set_debuglevel(debuglevel)
        mail.starttls()
        mail.login(SMTP_USERNAME, SMTP_PASSWORD)
        mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        mail.quit()


    def process(self):
        self.__parse()
        self.__process_links()


if __name__ == '__main__':
    finder = bgtvfind()
    finder.process()

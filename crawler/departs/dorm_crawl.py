from bs4 import BeautifulSoup as bs
import sys, ssl

sys.path.append('../lib')
from crawler import *
import requests
import time
import traceback

# 충남대 기숙사 크롤러
class crawl_dorm(GeneralNoNum):

    def __init__(self, url, subs_table, table, msgTitle):
        super().__init__(url, subs_table, table, msgTitle)

    def getLastFromWeb(self, n):
        html = requests.get(self.url)
        html.encoding = 'utf-8'
        soup = bs(html.text, 'html.parser')

        # data extraction
        notice = soup.findAll('td', {'class': 'title'})
        notice_title = [td.find('span', {'class': 'btxt'}).get_text() for td in notice]
        notice_link = ['https://dorm.cnu.ac.kr/_prog/_board/' + link.find('a').attrs['href'] for link in notice]

        result_title = notice_title[:n]
        result_link = notice_link[:n]

        return (result_title, result_link)


dorm = crawl_dorm('https://dorm.cnu.ac.kr/_prog/_board/?code=sub05_0501&site_dvs_cd=kr&menu_dvs_cd=0501', 'dorm', 'DORM_NOTICE', '기숙사')
def crawl_all():
    while True:
        try:
            dorm.crawl()
            time.sleep(10)
        except:
            traceback.print_exc()

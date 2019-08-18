from bs4 import BeautifulSoup as bs
import sys, ssl

sys.path.append('../../lib')
from crawler import *
import requests
import time
import traceback

# 충남대 기숙사 크롤러
class crawl_dorm(GeneralNoNum):

    def __init__(self, url, subs_table, table, msgTitle):
        super().__init__(url, subs_table, table, msgTitle)

    def getLastFromWeb(self):
        html = requests.get(self.url)
        html.encoding = 'utf-8'
        soup = bs(html.text, 'html.parser')
        result_title = []
        result_link = []

        # data extraction
        notice = soup.findAll('td', {'class': 'title'})
        for td in notice:
            title = td.find('span', {'class': 'btxt'}).get_text()
            if self.isInDB(title) != 0:
                continue
            link = 'https://dorm.cnu.ac.kr/_prog/_board/' + td.find('a').attrs['href']
            result_title.append(title)
            result_link.append(link)
        return (result_title, result_link)


dorm = crawl_dorm('https://dorm.cnu.ac.kr/_prog/_board/?code=sub05_0501&site_dvs_cd=kr&menu_dvs_cd=0501', 'dorm', 'DORM_NOTICE', '기숙사')

def crawl_all():
    while True:
        try:
            dorm.crawl()
            time.sleep(10)
        except:
            traceback.print_exc()

if __name__ == '__main__':
    crawl_all()

from bs4 import BeautifulSoup as bs
import sys, ssl

sys.path.append('../lib')
from crawler import *
import requests
import time
import traceback

# 자유전공학부 크롤러
class crawl_free(General):

    def __init__(self, url, subs_table, table, msgTitle):
        super().__init__(url, subs_table, table, msgTitle)

    def getLastFromWeb(self, n):
        html = requests.get(self.url)
        soup = bs(html.text, 'html.parser')

        # data extraction
        notice = soup.findAll('tbody')
        notice_num = soup.findAll('td', {'class': 'cont1'})
        notice_title = soup.findAll('td', {'class': 'cont2'})

        # save in list
        result_num = []
        result_title = []
        for i in notice_num:
            result_num.append(int(i.text))
        for j in notice_title:
            result_title.append(j.text)

        result_num = result_num[:n]
        result_title = result_title[:n]

        return (result_num, result_title)


free = crawl_free('http://free.pagei.gethompy.com/html/board.php?evboardNum=b51', 'free', 'FREE_NOTICE', '자유전공학부')
def crawl_all():
    while True:
        try:
            free.crawl()
            time.sleep(10)
        except:
            traceback.print_exc()


from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
sys.path.append('../../lib')
from crawler import *
import time
import pdb

class CSE_NOTICE(GeneralNoNum):
	def __init__(self, url, subs_table, table, msgTitle):
		super().__init__(url, subs_table, table, msgTitle)

	def getLastFromWeb(self):
		html=urlopen(self.url)
		bsObj=BeautifulSoup(html.read(),"html.parser")
		Num=bsObj.html.body.tbody.findAll("tr", class_='b-top-box')
		TextList = []
		linkList = []
		timeList = []
		for line in Num:
			title = line.find("td", {"class":"b-td-left"}).find('a').get_text().strip()
			title = re.sub('\s+', ' ', title).strip()
			if self.isInDB(title) != 0:
				continue
			TextList += [title]
			linkList += [self.url + line.find("div", {"class":"b-title-box"}).find('a').attrs['href']]
			timeList += [time.time()]
		return TextList, linkList, timeList

bachelor = CSE_NOTICE('https://computer.cnu.ac.kr/computer/notice/bachelor.do', 'cse', 'CSE_NOTICE_BACHELOR', '[학사공지] - 컴퓨터융합학부')
project = CSE_NOTICE('https://computer.cnu.ac.kr/computer/notice/project.do', 'cse', 'CSE_NOTICE_PROJECT', '[사업단소식] - 컴퓨터융합학부')
job = CSE_NOTICE('https://computer.cnu.ac.kr/computer/notice/job.do', 'cse', 'CSE_NOTICE_JOB', '[취업정보] - 컴퓨터융합학부')
news = CSE_NOTICE('https://computer.cnu.ac.kr/computer/notice/cse.do', 'cse', 'CSE_NOTICE_NEWS', '[학부소식] - 컴퓨터융합학부')
general = CSE_NOTICE('https://computer.cnu.ac.kr/computer/notice/notice.do', 'cse', 'CSE_NOTICE_NOTICE', '[일반소식] - 컴퓨터융합학부')

def crawl_all():
    #pdb.set_trace()
    bachelor.crawl()
    project.crawl()
    job.crawl()
    news.crawl()
    general.crawl()
    
if __name__ == '__main__':
	crawl_all()

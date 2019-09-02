import threading
import os
import sys
sys.path.append('./departs')
sys.path.append('/home/ubuntu/CNUNotifier/lib')
import cse_crawl
import free_crawl
import german_crawl
#import cse_notice_crawl
import dorm_crawl
import french_crawl
import traceback
import time

crawlers = []

crawlers.append(cse_crawl.crawl_all)
crawlers.append(free_crawl.crawl_all)
#crawlers.append(cse_notice_crawl.crawl_all)
crawlers.append(german_crawl.crawl_all)
crawlers.append(dorm_crawl.crawl_all)
crawlers.append(french_crawl.crawl_all)

#os.system('script latest.log')
while True:
    for crawl in crawlers:
        try:
            crawl()
        except:
            traceback.print_exc()
        time.sleep(5)

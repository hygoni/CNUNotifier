import threading
import os
import sys
sys.path.append('./departs')
sys.path.append('/home/ubuntu/CNUNotifier/lib')
import cse_crawl
import free_crawl
import german_crawl
import cse_notice_crawl

threads = []

threads.append(threading.Thread(target=cse_crawl.crawl_all))
threads.append(threading.Thread(target=free_crawl.crawl_all))
threads.append(threading.Thread(target=cse_notice_crawl.crawl_all))
#threads.append(threading.Thread(target=german_crawl.crawl_all))


for thread in threads:
    thread.start()

while True:
    pass



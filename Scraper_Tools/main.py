import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'GL-Test'
HOMEPAGE = 'http://labs.globus.org/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    i=1
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        print("Created Spider No.", i)
        i+=1


# Do the next job in the queue
def work():

    while True:
        url = queue.get()
        #tup = (url, )

        #print(tup) ### This print all website

        print(url, "main.work()")
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link) #TODO: want to put (SOURCE, DEST) tuple in the link.
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
### TODO: Add .txt to .csv script here.
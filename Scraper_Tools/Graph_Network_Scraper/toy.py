from spider import Spider

def crawl_page(thread_name, page_url):
    if page_url not in Spider.crawled:
        print(thread_name + ' now crawling ' + page_url)
        print('Queue size: ' + str(len(Spider.queue)) + ' | Crawled files:  ' + str(len(Spider.crawled)))

        Spider.add_links_to_queue(Spider.gather_links(page_url))
        Spider.queue.remove(page_url)
        Spider.crawled.add(page_url)
        Spider.update_files()



def tuple_cracker(tup):
    source = tup[0]
    print(source)


def add_tup_to_queue(tup):
    Spider.queue.add(tup)


def tuple_maker(url1, url2):
    print("hey")

tup = ('kitty', 'katty')

tuple_cracker(tup)
add_tup_to_queue(tup)
from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    ftp_file = ''
    queue = set()
    crawled = set()
    ftp = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.ftp_file = Spider.project_name + '/ftp.txt'
        self.boot()
        self.crawl_page('Lead Spider', Spider.base_url) #TODO: Home link instantiated

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.ftp = file_to_set(Spider.ftp_file)

    # Updates user display, fills queue and updates files
    # TODO: will input a tuple, access second element in tuple.
    @staticmethod
    def crawl_page(thread_name, page_url):

        if page_url not in Spider.crawled: #Do we take the whole

            print(thread_name + ' now crawling ' + page_url)
            print('Queue size: ' + str(len(Spider.queue)) + ' | Crawled files:  ' + str(len(Spider.crawled)))

            Spider.add_links_to_queue(Spider.gather_links(page_url), page_url)
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url) #contains base and page_url
            finder.feed(html_string)

        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links, page_url):

        ### Put all FTP links into an additional folder.
        for url in links:

            ### Added: turn into source-destination tuples.
            source = page_url
            destination = url
            tup = (source,destination)

            if "ftp://" in url:
                Spider.ftp.add(url)

            else:
                if (url in Spider.queue) or (url in Spider.crawled):
                    continue
                if Spider.domain_name != get_domain_name(url):
                    continue

                #tup = url()
                Spider.queue.add(url) #TODO: change this to add a tuple --- let debugging commence.
                print(url, "Spider.add_links_to_queue")


    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        set_to_file(Spider.ftp, Spider.ftp_file)

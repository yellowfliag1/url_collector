import requests
import sys
from queue import Queue
import threading
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}


def spider(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    urls = soup.find_all(name='a', attrs={'data-click': re.compile('.'), 'class': None})
    for url in urls:
        r_get_url = requests.get(url['href'], headers=headers, timeout=8)
        if r_get_url.status_code == 200:
            # print(r_get_url.url)
            url_para = r_get_url.url
            url_index_tmp = url_para.split('/')
            url_index = url_index_tmp[0] + url_index_tmp[1] + '//' + url_index_tmp[2]
            print(url_para)
            file1 = open('out_para.txt', 'a+')
            file1.write(str(url_para))
            file1.write('\n')
            file1.close()
            with open('out_index.txt') as f:
                if url_index not in f.read():
                    file2 = open('out_index.txt', 'a+')
                    file2.write(str(url_index))
                    file2.write('\n')
                    file2.close()


class UrlSpider(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while not self._queue.empty():
            url = self._queue.get()
            try:
                spider(url)
            except BaseException as e:
                print(e)
                pass


def main(keyword):
    url_queue = Queue()
    for i in range(0, 760, 10):
        url_queue.put(('https://www.baidu.com/s?wd=%s&pn=%s' % (keyword, str(i))))
    threads = []
    thread_count = 4
    for i in range(thread_count):
        threads.append(UrlSpider(url_queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    f1 = open('out_para.txt', 'w')
    f2 = open('out_index.txt', 'w')
    if len(sys.argv) != 2:
        print("Enter:%s keyword" % sys.argv[0])
        sys.exit(-1)
    else:
        main(sys.argv[1])


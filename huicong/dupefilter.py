import uuid
import json
import codecs

from pybloom_live import BloomFilter

from scrapy.log import logger
from huicong.settings import CRAWLED_STORE_FILE_PATH


namespace_url = lambda url: str(uuid.uuid5(uuid.NAMESPACE_URL, url.encode('utf8')))


class UrlFilter(BloomFilter):

    def __init__(self, capacity=1000000, error_rate=0.01):
        super().__init__(capacity=capacity, error_rate=error_rate)

    def init(self):
        with codecs.open(CRAWLED_STORE_FILE_PATH, 'r') as file:
            for line in file.readlines():
                try:
                    link = json.loads(line, encoding='utf8')['companyUrl'].strip()
                    self.add(namespace_url(link))
                except Exception as ex:
                    logger.info(f"[URLFILTERERROR] {line} {ex}")
        logger.info(f"[URLFILTERINIT] {self.count}")

    def exist(self, url):
        return True if namespace_url(url) in self else False

    def add_bloom_filter(self, url):
        if not self.exist(url):
            self.add(namespace_url(url))
            return True
        return False


url_dep_filter = UrlFilter()

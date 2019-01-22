# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from huicong.settings import CRAWLED_STORE_FILE_PATH


class HuiCongPipeline(object):

    def process_item(self, item, spider):
        with codecs.open(CRAWLED_STORE_FILE_PATH, mode="a", encoding="utf8") as file:
            line = json.dumps(dict(item), ensure_ascii=False, encoding="utf8") + "\n"
            file.write(line)

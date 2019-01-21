# -*- coding: utf-8 -*-
import os


BOT_NAME = 'huicong'

SPIDER_MODULES = ['huicong.spiders']
NEWSPIDER_MODULE = 'huicong.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'huicong.spiders.middlewares.useragent_middlewares.RotateUserAgentMiddleware' :400,
    # 'huicong.spiders.proxy_download_middlerware.ProxyMiddleware' :200,
}

ITEM_PIPELINES = {
   'huicong.pipelines.HuicongPipeline': 300,
}

LOG_FILE = "log.txt"
LOG_LEVEL = "INFO"

# 将爬取的链接保存到文件里边 为下次增量爬取做过滤 正式工程可以将之保存到数据库中
CRAWLED_STORE_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "huicong.json")

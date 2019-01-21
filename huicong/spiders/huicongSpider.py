# -*- coding: utf-8 -*-
import time
import re

from urllib.parse import urljoin
from bs4 import BeautifulSoup


from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.log import logger

from ..items import HuicongItem
from huicong.dupefilter import url_dep_filter


areas = [
    u'中国:江苏省:苏州市', u'中国:江苏省:无锡市', u'中国:江苏省:徐州市', u'中国:江苏省:扬州市',
    u'中国:江苏省:南京市', u'中国:江苏省:宿迁市', u'中国:江苏省:连云港市', u'中国:江苏省:盐城市',
    u'中国:江苏省:泰州市', u'中国:江苏省:南通市', u'中国:江苏省:泰州市', u'中国:江苏省:镇江市',
    u'中国:江苏省:淮安市'
]

species = [
             u"化工", u"涂料",  u"表面", u"塑料",
             u"安防", u"消防",
             u"电子", u"LED",
             u"酒店", u"家居", u"礼品",
             u"五金", u"建材", u"家装",
             u"服装", u"纺织",
             u"印刷", u"包装", u"丝印",
             u"净水器", u"饮水", u"配件",
             u"空调", u"采暖", u"热泵",
             u"汽车", u"用品", u"维修",
             u"食品", u"制药",
             u"家电",
             u"皮革", u"制鞋",
             u"工程", u"机械", u"工业",
             u"广电", u"教育",
             u"音响", u"灯光", u"LED屏",
             u"净水", u"科技", u"汽车", u"服饰"
        ]


class HuicongSpider(Spider):

    name = "huicong"
    allow_domains = ["s.hc360.com"]

    start_urls = []
    for area in areas[:]:
        for specie in species[:]:
            url = f"http://s.hc360.com/?w={area}&z={specie}&mc=enterprise"
            start_urls.append(url)

    def __init__(self):
        super(HuicongSpider, self).__init__()

    def parse(self, response):
        sel = Selector(response)

        if "&af=3" not in response.url:  # first page
            pull_down_url = f'{response.url} + "&af=3"'
            yield Request(url=pull_down_url, callback=self.parse)

            follow_urls = sel.xpath('//div[@class="s-mod-page"]//a/@href')
            for url in follow_urls[:]:
                yield Request(url = url, callback=self.parse)

        companies = sel.css('a[data-exposurelog]')

        extract_data_handler = lambda data_list: data_list[0].strip() if data_list else ""
        for company in companies[:1]:
            company_name = extract_data_handler(company.xpath('./@title').extract())
            company_url = extract_data_handler(company.xpath('./@href').extract())
            meta = {"company_name": company_name}
            if url_dep_filter.exist(company_url):
                yield Request(url=company_url, callback=self.parse_company_entrance, meta=meta)

    def parse_company_entrance(self, response):
        item = HuicongItem()
        soup = BeautifulSoup(response.body)
        detail_info = soup.select('div[class^="rBox3"] div[class^="tableCon"]')
        if len(detail_info)!= 0:
            item["companyName"] = response.meta["company_name"]
            item["companyUrl"] = response.url
            self.get_company_info(detail_info, item)

            contact_info_spans = soup.select('div[class^rBox3]  div[class^="tableCon"] div[class^="detailsinfo"]')[1].find_all("span")
            item['contactPerson'],item['cellphone'], item['phone'], item['fax'] = ["", "", "", ""]
            for index,contact_way in enumerate(contact_info_spans):
                if contact_way.text.strip(u'：') == u"联系人":
                    item['contactPerson'] = contact_info_spans[index+1].text
                if contact_way.text.strip(u'：') == u"手机":
                    item['cellphone'] = contact_info_spans[index+1].text
                if contact_way.text.strip(u'：') == u"电话":
                    item['phone'] = contact_info_spans[index+1].text
                if contact_way.text.strip(u'：') == u"传真":
                    item['fax'] = contact_info_spans[index+1].text
            item["memberInfo"] = ""
            item["MyeeigIndex"] = ""
            item["merchantGrade"]= ""
            item['collctTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            yield item
        else:
            company_url = urljoin(response.url,"shop/show.html")
            meta = {"company_name": response.meta['company_name'], 'company_url': response.url}
            yield Request(url=company_url, callback=self.parse_company_page, meta=meta)

    def get_company_info(self,detail_info,item):

        escape = lambda text: re.sub('[\t\n\r]', '', text)
        td_labels = detail_info[0].find_all('td')
        item["mainBussiness"] = escape(td_labels[1].text)
        item["mainIndustry"] = escape(td_labels[3].text)
        item['manageModel'] = escape(td_labels[7].text)
        item['employNum'] = escape(td_labels[17].text)
        item["revenue"] = escape(td_labels[19].text)
        item['band'] = escape(td_labels[21].text)
        item['customerBase'] = escape(td_labels[25].text)
        item['annualExport'] = escape(td_labels[29].text)
        try:
            item['homePage'] = escape(td_labels[57].text)
        except:
            item['homePage'] = ""
        item['mainMarket'] = escape(td_labels[27].text)
        item['annualImport'] = escape(td_labels[31].text)
        item['bankAccount'] = escape(td_labels[35].text)
        item['deptMembers'] = escape(td_labels[39].text)
        item['factoryArea'] = escape(td_labels[43].text)
        item['manageCertification'] = escape(td_labels[47].text)
        item['certificate'] = escape(td_labels[51].text)
        item['memberAssessment'] = escape(td_labels[55].text)

        if 'http' not in item['homePage']:
            item['homePage'] = ""
        else:
            item['homePage'] = re.sub( u'\xa0', ' ', item['homePage'])

    def parse_company_page(self, response):
        item = HuicongItem()
        item["companyName"] = response.meta["company_name"]
        item["companyUrl"] = response.meta['company_url']

        soup = BeautifulSoup(response.body)
        detail_info = soup.select('div[class^="contentbox"] div[class^="detailsinfo"]')
        self.get_company_info(detail_info, item)

        try:
            item['memberInfo'] = re.sub('[\t\n\r]', '', soup.select('div[class^="contentbox"] div[class^="memyear"]')[0].find("span").text.strip())
        except:
            item['memberInfo'],item['MyeeigIndex'], item['merchantGrade'] = ["", "", ""]
        else:
            if u"买卖通会员" not in item['memberInfo']:
                item['MyeeigIndex'] = ""
            else:
                item['MyeeigIndex'] = soup.select('div[class^="contentbox"] div[class^="comInfogo"] span[class^="redbold14"]')[0].a.text

            item['merchantGrade']= soup.select('div[class^="contentbox"] div[style^="color"] a[target^="_blank"]')[0].img['src'].split('/')[-1].split('.')[0]

        item['contactPerson'], item['cellphone'], item['phone'], item['fax'] = "", "", "", ""

        try:
            contact_info = soup.select('div[class^="contentbox"] div[class^="contactbox"]')[0]
        except Exception as ex:
            logger.info(f"[SPIDERCONTACT] {response.url} {ex}")
        else:
            item['contactPerson'] = ''.join([info.text.strip() for info in contact_info.find_all("li")[0].find_all("span")])
            contact_ways = contact_info.find_all("li")[2:-1]
            try:
                for contact_way in contact_ways:
                    if u'电话'in contact_way['title'].split(u"："):
                        item['phone'] = contact_way['title'].split(u"：")[1]
                    if u'手机'in contact_way['title'].split(u"："):
                        item['cellphone'] = contact_way['title'].split(u"：")[1]
                    if u'传真'in contact_way['title'].split(u"："):
                        item['fax'] = contact_way['title'].split(u"：")[1]
            except Exception as ex:
                logger.info(f"[SPIDERCONTACTWAY] {response.url} {ex}")

        item['collctTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        
        return item

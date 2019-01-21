# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuicongItem(scrapy.Item):

    company_name = scrapy.Field()         #公司名称
    company_url = scrapy.Field()          #公司在慧聪上的链接地址
    mainBussiness = scrapy.Field()       #公司主营产品和服务
    mainIndustry = scrapy.Field()        #主要营业
    manageModel = scrapy.Field()         #经营模式
    employNum = scrapy.Field()           #员工人数
    revenue = scrapy.Field()             #年度营业额
    band = scrapy.Field()                #经营品牌
    customerBase = scrapy.Field()        #客户群
    annualExport = scrapy.Field()        #年度出口额
    homePage = scrapy.Field()            #公司主页
    mainMarket = scrapy.Field()          #主要市场
    annualImport = scrapy.Field()        #年度进口额
    bankAccount= scrapy.Field()          #银行账号
    deptMembers = scrapy.Field()         #研发人数
    factoryArea = scrapy.Field()         #工厂面积
    manageCertification = scrapy.Field() #管理体系认证
    certificate = scrapy.Field()         #证书荣誉
    memberAssessment = scrapy.Field()    #会员评价
    memberInfo = scrapy.Field()          #会员信息
    MyeeigIndex = scrapy.Field()         #买卖通指数
    merchantGrade = scrapy.Field()       #商家等级
    contactPerson = scrapy.Field()       #联系人
    cellphone = scrapy.Field()           #电话
    phone = scrapy.Field()               #手机
    fax = scrapy.Field()                 #传真
    collctTime = scrapy.Field()          #采集时间

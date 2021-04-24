# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawler51JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    job_href = scrapy.Field()
    # 职位名字
    job_name = scrapy.Field()
    # 企业名称
    company_name = scrapy.Field()
    # 薪资水平
    providesalary_text = scrapy.Field()
    # 工作城市
    workarea_text = scrapy.Field()
    # 企业类型
    companytype_text = scrapy.Field()
    # 工作年限
    workyear = scrapy.Field()
    # 发布日期
    issuedate = scrapy.Field()
    # 公司规模
    companysize_text = scrapy.Field()
    # 所处行业
    companyind_text= scrapy.Field()
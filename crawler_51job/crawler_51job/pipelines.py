# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import random
import pymongo

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class Crawler51JobPipeline:
    collection_name = 'data_51job'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


class DirtyDataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 清洗providesalary_text这个field的脏数据
        if len(adapter.get('providesalary_text')) == 0:
            raise DropItem('月薪数据缺失, 丢弃本条目')
        else:
            if str(adapter.get('providesalary_text')).__contains__('-'):
                if str(adapter.get('providesalary_text')).__contains__('年'):
                    # 将年薪的范围用分隔符‘-’分割开来并取头部数据换算成月薪
                    salary_annually = str(adapter.get('providesalary_text')).split('-')[0].strip()
                    salary_monthly = round(float(salary_annually) / 12, 1)
                elif str(adapter.get('providesalary_text')).__contains__('月'):
                    salary_monthly = str(adapter.get('providesalary_text')).split('-')[0].strip()
                    if str(adapter.get('providesalary_text')).__contains__('千'):
                        salary_monthly = round(float(salary_monthly) * 0.1, 1)
                    else:
                        salary_monthly = round(float(salary_monthly), 1)
                else:
                    raise DropItem('月薪数据缺失, 丢弃本条目')
                # 统一处理月薪为float类型, 保留一位小数
                adapter['providesalary_text'] = salary_monthly
            else:
                raise DropItem('月薪数据缺失, 丢弃本条目')

        # 清洗companysize_text这个filed的脏数据
        if len(adapter.get('companysize_text')) == 0:
            raise DropItem('公司规模数据缺失, 丢弃本条目')
        else:
            company_size = str(adapter.get('companysize_text')).replace('人', '')
            if company_size.__contains__('以上'):
                adapter['companysize_text'] = 10001
            elif company_size.__contains__('-'):
                adapter['companysize_text'] = int(company_size.split('-')[0])
            elif company_size.__contains__('少于50'):
                adapter['companysize_text'] = random.randint(1, 49)
            else:
                pass

        if len(adapter.get('workyear')) == 0:
            raise DropItem('工作年限数据缺失, 丢弃本条目')
        else:
            adapter['workyear'] = int(adapter.get('workyear'))

        if len(adapter.get('workarea_text')) == 0 or str(adapter.get('workarea_text')).__contains__('异地'):
            raise DropItem('工作城市数据缺失， 丢弃本条目')
        else:
            if str(adapter.get('workarea_text')).__contains__('-'):
                adapter['workarea_text'] = str(adapter.get('workarea_text')).split('-')[0].strip()
            else:
                pass

        return item

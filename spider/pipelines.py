# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from spider import settings


class MongoPipeline(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        mongo_db = mongo_client[settings.MONGODB_DB]
        self.mongo_collection = mongo_db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        item_dict = dict(item)
        self.mongo_collection.insert(item_dict, check_keys=False)
        return item_dict

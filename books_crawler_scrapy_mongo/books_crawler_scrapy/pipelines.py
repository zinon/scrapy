# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

#deprecated since scrapy v1.7
#from scrapy.conf import settings

from scrapy.utils.project import get_project_settings


#class BooksCrawlerScrapyPipeline:
#    def process_item(self, item, spider):
#        return item

# name as in settings.py
class MongoDBPipeline(object):
    def __init__(self):
        """
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])

        db = connection(settings['MONGODB_DB'])
        coll = settings['MONGODB_COLLECTION']
        self.collection = db[coll]
        """
        self.__settings = get_project_settings()

        #connect to mongodb
        client = self.connect_db()
        #create db
        db = client[self.__settings['MONGODB_DB']]
        #create collection
        self.collection = db[self.__settings['MONGODB_COLLECTION']]
        
            

    def connect_db(self):
        print("DB:\n",
              self.__settings['MONGODB_SERVER'],
              self.__settings['MONGODB_PORT'])
        
        return MongoClient(self.__settings['MONGODB_SERVER'],
                             self.__settings['MONGODB_PORT'])     


    def process_item(self, item, spider):
        self.collection.insert( dict(item) )
        return item

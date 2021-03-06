# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from settings import MONGODB
import models
from models import scoped_session


class CnbetaMongoPipeline(object):
    def __init__(self):
        self._db = MONGODB.get('db')
        self._collection = MONGODB.get('collection')
        self._host = MONGODB.get('host')
        self._port = MONGODB.get('port')
        self._client = pymongo \
            .MongoClient(host=self._host, port=self._port) \
            .get_database(self._db) \
            .get_collection(self._collection)

    def process_item(self, item, spider):
        self._client.create_index([('title', pymongo.DESCENDING)], background=True)
        self._client.update_one(filter={'title': item['title']}, update={'$set': dict(item)}, upsert=True)
        return item


class CnbetaMysqlPipeline(object):

    def process_item(self, item, spider):
        sql_cnbeta = models.cnbeta()
        sql_cnbeta = models.map_orm_item(scrapy_item=item, sql_item=sql_cnbeta)
        with scoped_session() as session:
            session.add(sql_cnbeta)

        return item

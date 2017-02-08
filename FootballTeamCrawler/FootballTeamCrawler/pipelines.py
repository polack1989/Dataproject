# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('Transfers_All_Years.json', 'wb')
        self.dict = {}

    def close_spider(self, spider):
        json.dump(self.dict, self.file, indent=4)
        self.file.close()

    def process_item(self, item, spider):
        for key in item:
            self.dict[key] = item[key]
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import ujson
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class PickerPipeline(object):

    def __init__(self):
    	self.fp = open(settings['CACHE_FOLDER']+'/'+settings['NAMES_FILE'], 'a+')
    	self.setfp = open(settings['CACHE_FOLDER']+'/'+settings['NAMESET_FILE'], 'a+')

    def process_item(self, item, spider):
        line = ujson.dumps(dict(item)) + "\n"
        self.fp.write(line)
        self.setfp.write(str(item['userId'])+"\n")
        return item

class DuplicatesPipeline(object):

	def __init__(self):
		self.ids = set()
		if not os.path.exists(settings['CACHE_FOLDER']):
			os.mkdir(settings['CACHE_FOLDER'])

		nameset_file = settings['CACHE_FOLDER']+'/'+settings['NAMESET_FILE']

		if os.path.exists(nameset_file):
			fp = open(nameset_file)
			content = fp.read()
			self.ids = set(content.split("\n"))
			fp.close()

	def process_item(self, item, spider):
		if item['userId'] in self.ids:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.ids.add(item['userId'])
		return item

# -*- coding: utf-8 -*-
import scrapy
from picker.items import PickerItem
import ujson


class NameSpider(scrapy.Spider):
    name = "name"
    allowed_domains = ["renren.com"] 
    start_urls = ['http://name.renren.com/getRecomList']

    def parse(self, response):
        item = PickerItem()
        data = ujson.loads(response.body)
        if data['result'] == 'ok':
        	for name in data['data']:
        		item['headUrl'] = name['headUrl']
        		item['name'] = name['name']
        		item['userId'] = name['userId']
        		yield item

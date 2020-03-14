# -*- coding: utf-8 -*-
import scrapy
from wh_first.items import WhFirstItem

class FstSpider(scrapy.Spider):
    name = 'fst'
    allowed_domains = ['aliwx.com.cn']
    start_urls = ['http://www.aliwx.com.cn/']

    def parse(self, response):
        item=WhFirstItem()
        item["title"] = response.xpath("//p[@class='title']/text()").extract()
        # print(item["title"])
        yield item
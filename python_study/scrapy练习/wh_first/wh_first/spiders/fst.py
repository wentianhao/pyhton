# -*- coding: utf-8 -*-
import scrapy


class FstSpider(scrapy.Spider):
    name = 'fst'
    allowed_domains = ['aliwx.com.cn']
    start_urls = ['http://aliwx.com.cn/']

    def parse(self, response):
        pass

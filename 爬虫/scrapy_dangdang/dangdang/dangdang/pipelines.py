# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DangdangPipeline(object):
    def process_item(self, item, spider):
        coon = pymysql.connect(host="127.0.0.1",user="root",passwd="123456",db="dd")
        for j in range(0,len(item["title"])-1):
            title = item["title"][j]
            # print(str(j)+ item["title"][j])
            link = item["link"][j]
            # print(str(j)+ item["link"][j])
            comment = item["comment"][j]
            # print(str(j)+ item["comment"][j])
            # print(j)
            sql="insert into boods(title,link,comment) values('"+title+"','"+link+"','"+comment+"')"
            # print(sql)
            coon.query(sql)
            coon.commit()
        coon.close()
        return item

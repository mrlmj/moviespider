# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#电影的数据库模型
class MovieItem(scrapy.Item):
    title = scrapy.Field()
    time = scrapy.Field()
    update_time = scrapy.Field()
    introduce = scrapy.Field()
    image_url = scrapy.Field()
    types = scrapy.Field()
    countries = scrapy.Field()
    actors = scrapy.Field()
    languages = scrapy.Field()
    links = scrapy.Field()
    crawl_url = scrapy.Field()
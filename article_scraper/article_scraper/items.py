# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class hackerNewsItem(scrapy.Item):
    alertType = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    title= scrapy.Field()


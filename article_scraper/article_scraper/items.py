# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class hackerNewsItem(scrapy.Item):
    link = scrapy.Field()
    date = scrapy.Field()
    title= scrapy.Field()

class ArticleScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdTrackerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    filename = scrapy.Field()
    info = scrapy.Field()

    # headers = scrapy.Field()


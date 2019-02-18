# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

from scrapy.loader import (
    ItemLoader,
    processors,
)


class ECBItem(scrapy.Item):
    date = scrapy.Field()
    value = scrapy.Field()
    type = scrapy.Field()
    base_currency_code = scrapy.Field()
    target_currency_code = scrapy.Field()
    data = scrapy.Field(input_processor=processors.Identity())


class ECBItemData(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    country = scrapy.Field()
    language_code = scrapy.Field()
    institution_code = scrapy.Field()


class ECBItemLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()


class ECBItemDataLoader(ECBItemLoader):
    default_item_class = ECBItemData

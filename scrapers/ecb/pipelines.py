# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests


# TODO:
# add suport for bulk create in API and here or use message broker
# (or log stream) to pass scraped items to microservice to allow it
# populate data more efficiently in batches.
# Better "ready to use" architecture: https://github.com/scrapinghub/frontera
class ECBPipeline:
    def __init__(self, url):
        self.url = url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(url=crawler.settings.get('RATES_CREATE_URL'))

    def open_spider(self, spider):
        self.session = requests.Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        try:
            # TODO: add retry policy
            response = self.session.post(self.url, json=dict(item))
            response.raise_for_status()
        except requests.RequestException as exc:
            spider.logger.error(f'Item saving failed. Exception: "{exc}".')
        return item

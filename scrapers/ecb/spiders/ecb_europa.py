# -*- coding: utf-8 -*-
import scrapy

from ecb import items


class ECBEuropaSpider(scrapy.spiders.XMLFeedSpider):
    DEFAULT_NAMESPACE = 'xyz'
    name = 'ecb_europa'
    allowed_domains = ['ecb.europa.eu']
    start_urls = ['https://www.ecb.europa.eu/home/html/rss.en.html']
    # TODO: extract namespaces dynamically from feeds responses
    namespaces = (
        (DEFAULT_NAMESPACE, 'http://purl.org/rss/1.0/'),
        ('cb', 'http://www.cbwiki.net/wiki/index.php/Specification_1.1'),
        ('dc', 'http://purl.org/dc/elements/1.1/'),
        ('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
        ('xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
    )
    iterator = 'xml'
    itertag = f'{DEFAULT_NAMESPACE}:item'

    def parse(self, response):
        query = (
            '//h2[text()="Euro foreign exchange reference rates RSS links"]'
            '/following-sibling::ul//a[@class="rss"]'
        )
        for rss_link_selector in response.xpath(query):
            currency_title = rss_link_selector.xpath('text()').extract_first()
            yield scrapy.http.Request(
                response.urljoin(rss_link_selector.attrib['href']),
                meta={'currency_title': currency_title},
                callback=self.parse_feed,
            )

    def parse_feed(self, response):
        return super().parse(response)

    def parse_node(self, response, selector):
        item_loader = items.ECBItemLoader(
            item=items.ECBItem(),
            selector=selector,
        )
        item_loader.add_xpath('date', 'dc:date/text()')
        # TODO: extract information about frequency for crontab
        # TODO: extract information about value precision
        item_loader.add_xpath(
            'value',
            'cb:statistics/cb:exchangeRate/cb:value/text()',
        )
        item_loader.add_xpath(
            'type',
            'cb:statistics/cb:exchangeRate/cb:rateType/text()',
        )
        item_loader.add_xpath(
            'base_currency_code',
            'cb:statistics/cb:exchangeRate/cb:baseCurrency/text()',
        )
        item_loader.add_xpath(
            'target_currency_code',
            'cb:statistics/cb:exchangeRate/cb:targetCurrency/text()',
        )
        item_loader.add_value('data', self.parse_item_data(selector))
        return item_loader.load_item()

    def parse_item_data(self, selector):
        item_loader = items.ECBItemDataLoader(
            item=items.ECBItemData(),
            selector=selector,
        )
        item_loader.add_xpath(
            'title',
            f'{self.DEFAULT_NAMESPACE}:title/text()',
        )
        item_loader.add_xpath(
            'description',
            f'{self.DEFAULT_NAMESPACE}:description/text()',
        )
        item_loader.add_xpath('link', f'{self.DEFAULT_NAMESPACE}:link/text()')
        item_loader.add_xpath('language_code', 'dc:language/text()')
        item_loader.add_xpath('country', 'cb:statistics/cb:country/text()')
        item_loader.add_xpath(
            'institution_code',
            'cb:statistics/cb:institutionAbbrev/text()',
        )
        return dict(item_loader.load_item())

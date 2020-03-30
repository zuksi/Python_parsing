# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroy_parser.items import LeroyParserItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/samorezy/']

    def parse(self, response):
        ads_links = response.xpath('//a[@class="black-link product-name-inner"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyParserItem(), response=response)
        loader.add_xpath('photos',
                         '//div[@class="container detailed-view-inner container--fronton"]//source[@media=" only screen and (min-width: 1024px)"]/@data-origin')
        loader.add_css('name', 'h1.header-2::text')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('parameters_names', '//dt[@class="def-list__term"]/text()')
        loader.add_xpath('parameters_values', '//dd[@class="def-list__definition"]/text()')
        yield loader.load_item()

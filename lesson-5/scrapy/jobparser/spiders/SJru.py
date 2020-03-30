# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

class SJruSpider(scrapy.Spider):
    name = 'SJru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        if next_page is None:
            yield
        yield response.follow(next_page, callback=self.parse)

        vac_list = response.xpath("//a[contains(@class, 'icMQ_ _1QIBo f-test-link')]/@href").extract()

        for link in vac_list:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_xpath('name',"//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()")
        loader.add_xpath('salary', "//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()")
        loader.add_value('link',response.request.url)
        loader.add_value('site', 'superjob.ru')
        yield loader.load_item()

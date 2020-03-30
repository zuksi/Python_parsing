# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        # next_page = response.css("a.HH-Pager-Controls-Next::attr(href)")
        if next_page is None:
            yield
        yield response.follow(next_page, callback=self.parse)

        vac_list = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()

        for link in vac_list:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_xpath('name',"//h1[@class='bloko-header-1']/text()")
        loader.add_xpath('salary', "//span[@class='bloko-header-2 bloko-header-2_lite']/text()")
        loader.add_value('link',response.request.url)
        loader.add_value('site', 'HH.ru')
        yield loader.load_item()

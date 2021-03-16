# -*- coding: utf-8 -*-
import scrapy
import json
import re


class EbayCheckSpider(scrapy.Spider):
    name = 'ebay_check'
    allowed_domains = ['www.ebay.co.uk']
    start_urls = ['https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=panathinaikos&_sacat=0&_sop=10&rt=nc&LH_PrefLoc=2']

    def parse(self, response):
        items = dict()
        listing_titles = response.css('.s-item__title::text').extract()
        listing_links = response.css('.s-item .s-item__link::attr(href)').extract()
        listing_time = response.css('.s-item .s-item__listingDate ::text').extract()
        for i in range(len(listing_titles)):
            items["Title"] = listing_titles[i]
            items["Link"] = listing_links[i]
            items["Listing Time"] = listing_time[i]
            yield items
        # for title in listing_titles:
        #     items["Title"] = title
        #     yield items
        # next_page = response.css('.pagination__next::attr(href)').extract_first()
        # if next_page:
        #     self.logger.debug(f"Going to next page {next_page}")
        #     url = response.urljoin(next_page)
        #     yield scrapy.Request(url=url, callback=self.parse)


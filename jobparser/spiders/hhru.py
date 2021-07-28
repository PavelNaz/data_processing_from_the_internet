import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [f'https://hh.ru/search/vacancy?text=python']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        job_links = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in job_links:
            yield response.follow(link, callback=self.vacancy_parce)

        yield response.follow(next_page, callback=self.parse)


    def vacancy_parce(self, response:HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        company_name = response.xpath("//a[@data-qa='vacancy-company-name']/span/text() | //a[@data-qa='vacancy-company-name']/span/span/text()").extract()
        company_address = response.xpath("//p[@data-qa='vacancy-view-location']/text() | //p[@data-qa='vacancy-view-location']/span/text()").extract()
        yield JobparserItem(name=name, salary=salary, company_name=company_name, company_address=company_address, link=link)


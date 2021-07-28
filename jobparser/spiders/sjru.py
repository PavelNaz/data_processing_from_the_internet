import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    start_urls = ['https://russia.superjob.ru/vakansii/razrabotchik-python.html']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[contains(@class,' f-test-link-Dalshe')]/@href").extract_first()
        job_links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9 f-test-link')]/@href").extract()
        for link in job_links:
            link = link.split('?')[0]
            yield response.follow(link, callback=self.vacancy_parce)

        yield response.follow(next_page, callback=self.parse)


    def vacancy_parce(self, response:HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span[@class='_1OuF_ ZON4b']/text()").extract()
        company_name = response.xpath("//div[@class='_1h3Zg _3Fsn4 f-test-text-vacancy-item-company-name]/a/@href").extract()
        company_address = response.xpath("//div[@class='_1h3Zg f-test-text-company-item-location]/a/@href").extract_first()
        yield JobparserItem(name=name, salary=salary, company_name=company_name, company_address=company_address, link=link)

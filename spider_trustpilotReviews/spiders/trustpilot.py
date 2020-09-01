import scrapy
from scrapy_splash import SplashRequest


class TrustpilotSpider(scrapy.Spider):
    name = 'trustpilot'
    allowed_domains = ['uk.trustpilot.com']
    start_urls = ['https://uk.trustpilot.com/review/www.getblys.com.au']

    def parse(self, response):
        names = response.xpath('//*[@class="consumer-information__name"]/text()').extract()
        titles = response.xpath('//*[@class="review-content__title"]/a/text()').extract()
        descriptions = response.xpath('//*[@class="review-content__text"]/text()').extract()

        for name, title, description in zip(names, titles, descriptions):
            yield {
                "Customer Name": name.strip(),
                "Title": title,
                "Comments": description.strip()
            }

        next_page = response.xpath('//*[@data-page-number="next-page"]/@href').extract_first()
        next_page = response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)



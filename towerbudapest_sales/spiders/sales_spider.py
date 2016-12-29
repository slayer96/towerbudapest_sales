import scrapy
import logging

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from towerbudapest_sales.items import TowerbudapestSalesItem


logger = logging.getLogger('logger')


class RentalsScrapy(CrawlSpider):
    name = 'towerbudapest_sales'
    start_urls = [r'http://www.towerbudapest.com/en/sales/']

    rules = (
        Rule(LinkExtractor(allow=('en/sales/\d$')),  follow=True),
        Rule(LinkExtractor(allow=('budapest_property'))),
    )

    def parse(self, response):
        urls = response.xpath('.//a[@class="button"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)
        logging.info(type(response))
        next_page = response.xpath(
            '//button[@class="btn btn-lg btn-default btn-paginate-control" and text()="Next "]/@onclick').extract_first()

        if next_page:
            next_page_url = next_page.split('=')[1]
            logging.warning(next_page_url[1:-1])
            yield scrapy.Request(next_page_url[1:-1], callback=self.parse)

    def parse_item(self, response):
        item = TowerbudapestSalesItem()
        item['url'] = response.url
        item['reference_number'] = response.xpath('.//span[@class="refnumber pull-right"]/text()')[0].extract()
        item['street_name'] = response.xpath('.//h1[@class="property-content-title clearfix"]/text()')[0].extract()
        item['district'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[1].extract()
        item['rooms'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[3].extract()
        item['size'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[5].extract()
        item['image_urls'] = response.xpath('.//a[@class="galimg nch-lightbox galleryimg"]/@href').extract()
        item['description'] = response.xpath('.//p[@class="kill-margin-bottom"]/text()').extract_first()
        item['floor'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[8].extract()
        item['parking'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[10].extract()
        item['view'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[12].extract()
        item['furnished'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[14].extract()
        item['elevator'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[16].extract()
        item['air_conditioner'] = response.xpath('.//ul[@class="list-unstyled"]/li//text()')[18].extract()
        item['sales_price'] = response.xpath('.//li[@class="property-price"]/text()').extract()
        item['phone_number'] = response.xpath('.//li[@class="property-tel"]/text()')[0].extract()
        return item

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'https://webscraper.io/test-sites/e-commerce/allinone',
    ]

    def parse(self, response):
        all_thumbs = response.xpath('//*[@class="thumbnail"]')[0]
        items = all_thumbs.xpath('//a[@class="title"]/text()').getall()
        prices = all_thumbs.xpath('//h4[contains(concat(" ",normalize-space(@class)," ")," price ")]/text()').getall()
        descriptions = all_thumbs.xpath('//p[@class="description"]/text()').getall()

        for i in range(len(items)):
            yield {
                'item': items[i],
                'price': prices[i],
                'description': descriptions[i],
            }

        next_page = response\
            .xpath('//a[contains(concat(" ",normalize-space(@class)," ")," category-link ")]/@href').get()
        next_sub = response\
            .xpath('//a[contains(concat(" ",normalize-space(@class)," ")," subcategory-link ")]/@href').get()
        if next_sub is not None:
            yield response.follow(next_sub, callback=self.parse)
        elif next_page is not None:
            yield response.follow(next_page, callback=self.parse)

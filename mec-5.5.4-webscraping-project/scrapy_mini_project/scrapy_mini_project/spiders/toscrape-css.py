import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'https://webscraper.io/test-sites/e-commerce/allinone',
    ]

    def parse(self, response):
        for item in response.css('div.thumbnail'):
            yield {
                'item': item.css('a.title::text').get(),
                'price': item.css('h4.price::text').get(),
                'description': item.css('p.description::text').getall(),
            }

        next_page = response.css('a.category-link::attr(href)').get()
        next_sub = response.css('a.subcategory-link::attr(href)').get()
        if next_sub is not None:
            yield response.follow(next_sub, callback=self.parse)
        elif next_page is not None:
            yield response.follow(next_page, callback=self.parse)
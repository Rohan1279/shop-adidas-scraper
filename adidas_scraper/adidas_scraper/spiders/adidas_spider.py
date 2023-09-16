import scrapy


class AdidasSpiderSpider(scrapy.Spider):
    name = "adidas_spider"
    allowed_domains = ["www.adidas.com"]
    start_urls = ["https://www.adidas.com/us/men-athletic_sneakers"]

    def parse(self, response):
        product_cards = response.css('div.glass-product-card')

        for product_card in product_cards:
            relative_url  = product_card.css('a[data-auto-id="glass-hockeycard-link"]').attrib['href']
              
           
            product_url =  "https://www.adidas.com" + relative_url
            yield response.follow(product_url, callback=self.parse_product_page)

        
        next_page = response.css('a[data-auto-id="plp-pagination-next"]').attrib['href']
        if next_page is not None:
                next_page_url =  "https://www.adidas.com" + next_page
                yield response.follow(next_page_url, callback=self.parse)

    def parse_product_page(self, response):
        
        yield {
            "img" : response.css('picture[data-testid="pdp-gallery-picture"] img::attr(src)').get(),
            "name" : response.css('h1[data-auto-id="product-title"] span::text').get(),
            "price" : response.css('div.gl-price-item::text').get()
        }

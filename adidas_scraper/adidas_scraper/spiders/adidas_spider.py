import scrapy
import re  # to extract data from script tag using regex
import json  # to convert string to json froms script tag
from adidas_scraper.items import AddidasProductItem


class AdidasSpiderSpider(scrapy.Spider):
    name = "adidas_spider"
    allowed_domains = ["www.adidas.com"]
    start_urls = ["https://www.adidas.com/us/men-athletic_sneakers"]  # SNEAKERS
    # start_urls = ["https://www.adidas.com/us/men-tops"]  # TOPS

    def parse(self, response):
        product_cards = response.css('div.glass-product-card')

        # print("\n******************\n" + "PRODUCTS COUNT", len(product_cards))
        for product_card in product_cards:
            relative_url = product_card.css(
                'a[data-auto-id="glass-hockeycard-link"]').attrib['href']

            product_url = "https://www.adidas.com" + relative_url
            yield response.follow(product_url, callback=self.parse_product_page)

        next_page = response.css(
            'a[data-auto-id="plp-pagination-next"]').attrib['href']
        if next_page is not None:
            next_page_url = "https://www.adidas.com" + next_page
            print("\n******************\n" + "NEXT PAGE" +
                  "\n******************\n", next_page_url)
            yield response.follow(next_page_url, callback=self.parse)

# using splash
# import scrapy
# from scrapy_splash import SplashRequest


# class AdidasSpiderSpider(scrapy.Spider):
#     name = "adidas_spider"
#     allowed_domains = ["www.adidas.com"]
#     start_urls = ["https://www.adidas.com/us/men-athletic_sneakers"]

#     def parse(self, response):
#         product_cards = response.css('div.glass-product-card')

#         print("\n******************\n" + "PRODUCTS COUNT", len(product_cards))
#         for product_card in product_cards:
#             relative_url = product_card.css(
#                 'a[data-auto-id="glass-hockeycard-link"]').attrib['href']
#             product_url = "https://www.adidas.com" + relative_url

#             yield SplashRequest(url=product_url, callback=self.parse_product_page, args={'wait': 10, "resource_timeout": 20, "timeout": 20})

#         next_page = response.css(
#             'a[data-auto-id="plp-pagination-next"]').attrib['href']
#         if next_page is not None:
#             next_page_url = "https://www.adidas.com" + next_page
#             print("\n******************\n" + "NEXT PAGE" +
#                   "\n******************\n", next_page_url)
#             yield SplashRequest(url=next_page_url, callback=self.parse, args={'wait': 10,  "resource_timeout": 20, "timeout": 20})

    def parse_product_page(self, response):
        script = response.xpath(
            '//script[contains(text(), "Product")]/text()').get()
        data = json.loads(script)
        adidas_product = AddidasProductItem()

        adidas_product['category'] = "Men's Sneaker"
        adidas_product['category_id'] = "63bc18eb473f136f0720ce0a"
        adidas_product['seller'] = "Adidas"
        adidas_product['description'] = re.search(
            r'"description":\s*"([^"]+)"', script).group(1)
        adidas_product['reviewsCount'] = data['aggregateRating']['reviewCount']
        adidas_product['ratings'] = data['aggregateRating']['ratingValue']
        adidas_product['img'] = response.css(
            'picture[data-testid="pdp-gallery-picture"] img::attr(src)').get()
        adidas_product['name'] = response.css(
            'h1[data-auto-id="product-title"] span::text').get(),
        adidas_product['price'] = response.css('div.gl-price-item::text').get()
        adidas_product['color'] = response.css(
            'div[data-auto-id="color-label"]::text').get()
        adidas_product['seller_email'] = "adidas@adidas.com"
        adidas_product['seller_id'] = ""
        adidas_product['seller_name'] = "adidas"
        adidas_product['seller_phone'] = ""
        adidas_product['isAdvertised'] = ""
        adidas_product['isReported'] = ""
        adidas_product['inStock'] = ""
        adidas_product['brand'] = "Adidas"
        # adidas_product['sizes'] = [{"id": "1", "name": "29", "stock": "", "price": ""}, {"id": "2", "name": "30", "stock": "", "price": ""}, {
        #     "id": "3", "name": "31", "stock": "", "price": ""}, {"id": "4", "name": "32", "stock": "", "price": ""}, {"id": "5", "name": "34", "stock": "", "price": ""}]
        # print("\n******************\n" + "PRODUCT" +
        #       "\n******************\n", adidas_product)
        yield adidas_product

        # yield {
        #     "category": "Men's Sneaker",
        #     "category_id": "63bc18eb473f136f0720ce0a",
        #     "seller": "Adidas",
        #     "img": response.css('picture[data-testid="pdp-gallery-picture"] img::attr(src)').get(),
        #     "name": response.css('h1[data-auto-id="product-title"] span::text').get(),
        #     "price": response.css('div.gl-price-item::text').get(),
        #     "color": response.css('div[data-auto-id="color-label"] ::text').get(),
        #     "seller_email": "adidas@adidas.com",
        #     "seller_id": "",
        #     "seller_name": "adidas",
        #     "description": re.search(r'"description":\s*"([^"]+)"', script).group(1),
        #     "reviewsCount": data['aggregateRating']['reviewCount'],
        #     "ratings": data['aggregateRating']['ratingValue'],
        #     "img": response.css('picture[data-testid="pdp-gallery-picture"] img::attr(src)').get(),
        #     "name": response.css('h1[data-auto-id="product-title"] span::text').get(),
        #     "price": response.css('div.gl-price-item::text').get(),
        #     "color": response.css('div[data-auto-id="color-label"] ::text').get(),
        #     "brand": "Adidas",
        #     "sizes": [{"id": "1", "name": "29", "stock": "", "price": ""}, {"id": "2", "name": "30", "stock": "", "price": ""}, {"id": "3", "name": "31", "stock": "", "price": ""}, {"id": "4", "name": "32", "stock": "", "price": ""}, {"id": "5", "name": "34", "stock": "", "price": ""}],
        # }

# {"_id":{"$oid":"63c417a57229a7dca8c2095e"},
#  "category":"Men's Pants",
#  "category_id":"63bc18eb473f136f0720ce0a",
#  "seller":"Adidas",
#  "name":"Primegreen Essentials Warm-Up Open Hem 3-Stripes Track Pants",
#  "price":{"$numberInt":"100"},
#  "description":"",
#  "reviewsCount":{"$numberInt":"263"},
#  "ratings":{"$numberDouble":"4.6"},
#  "img":"",
#  "color":"",
#  "productLinkHref":"https://www.adidas.com/us/primegreen-essentials-warm-up-open-hem-3-stripes-track-pants/H48429.html",
#  "seller_default_image":"https://static.vecteezy.com/system/resources/thumbnails/009/312/919/small/3d-render-cute-girl-sit-crossed-legs-hold-laptop-studying-at-home-png.png",
#  "seller_email":"adidas@adidas.com",
#  "seller_id":"",
#  "seller_name":"adidas",
#  "seller_phone":"",
#  "isAdvertised":false,
#  "isReported":false,
#  "inStock":true,
#  "brand":"Adidas",
#  "sizes":[{"id":"1","name":"29","stock":"","price":""},{"id":"2","name":"30","stock":"","price":""},{"id":"3","name":"31","stock":"","price":""},{"id":"4","name":"32","stock":"","price":""},{"id":"5","name":"34","stock":"","price":""}]}

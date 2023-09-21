# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdidasScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AddidasProductItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    category_id = scrapy.Field()
    seller = scrapy.Field()
    description = scrapy.Field()
    reviewsCount = scrapy.Field()
    ratings = scrapy.Field()
    img = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    color = scrapy.Field()
    seller_email = scrapy.Field()
    seller_id = scrapy.Field()
    seller_name = scrapy.Field()
    seller_phone = scrapy.Field()
    isAdvertised = scrapy.Field()
    isReported = scrapy.Field()
    inStock = scrapy.Field()
    brand = scrapy.Field()
    sizes = scrapy.Field()

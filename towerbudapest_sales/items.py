# -*- coding: utf-8 -*-

# De fine here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Field, Item


class TowerbudapestSalesItem(Item):
    url = Field()
    reference_number = Field()
    number = Field()
    street_name = Field()
    district = Field()
    rooms = Field()
    size = Field()
    image_urls = Field()
    description = Field()
    floor = Field()
    parking = Field()
    view = Field()
    furnished = Field()
    elevator = Field()
    air_conditioner = Field()
    # conditioner = Field()
    sales_price = Field()
    phone_number = Field()


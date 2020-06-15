import scrapy


class ResultItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()